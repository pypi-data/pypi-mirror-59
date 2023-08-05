import copy
import json
import logging
import os
from typing import Any, Dict, Generic, List, Optional, Tuple, TypeVar, cast

import attr
from mypy_extensions import TypedDict
from semantic_version import SimpleSpec, Version
from toposort import CircularDependencyError, toposort_flatten

from r2c.lib.analyzer import AnalyzerName, SpecifiedAnalyzer, VersionedAnalyzer
from r2c.lib.manifest import (
    AnalyzerManifest,
    IncompatibleManifestException,
    InvalidLocalPathException,
    InvalidManifestException,
    ManifestNotFoundException,
)

Node = TypeVar("Node")


@attr.s(auto_attribs=True)
class Graph(Generic[Node]):
    nodes: List[Node]
    edges: List[Tuple[Node, Node]]

    def topo_sorted(self) -> List[Node]:
        """
            If the graph is a DAG, return a topologically sorted list of nodes.
            Otherwise throws CircularDependencyError.
        """
        adjacency_dict = {
            n: set([e[1] for e in self.edges if e[0] == n]) for n in self.nodes
        }

        return list(reversed(toposort_flatten(adjacency_dict, sort=False)))

    def to_json(self):
        return {"nodes": self.nodes, "edges": self.edges}


ManifestWithStateJson = TypedDict(
    "ManifestWithStateJson", {"manifest": Dict["str", Any], "pending": bool}
)


@attr.s(auto_attribs=True)
class ManifestWithState:
    manifest: AnalyzerManifest
    pending: bool = True

    def set_not_pending(self):
        self.pending = False

    @classmethod
    def from_json(cls, json_obj: ManifestWithStateJson) -> "ManifestWithState":
        manifest_json = cast(Dict[str, Any], json_obj.get("manifest"))
        pending = json_obj.get("pending")
        if not manifest_json or pending is None or type(pending) != bool:
            raise Exception(f"Unable to parse ManifestWithState from {json_obj}")
        return cls(AnalyzerManifest.from_json(manifest_json), pending)

    def to_json(self) -> ManifestWithStateJson:
        return {"manifest": self.manifest.to_json(), "pending": self.pending}

    def __str__(self) -> str:
        return json.dumps(self.to_json())


AnalyzerDataJson = TypedDict(
    "AnalyzerDataJson", {"versions": Dict[str, ManifestWithStateJson], "public": bool}
)


@attr.s(auto_attribs=True)
class AnalyzerData:
    versions: Dict[Version, ManifestWithState]
    public: bool

    def set_public(self):
        self.public = True

    def to_json(self) -> AnalyzerDataJson:
        return {
            "versions": {
                str(version): manifest.to_json()
                for version, manifest in self.versions.items()
            },
            "public": self.public,
        }

    @classmethod
    def from_json(cls, json_obj: AnalyzerDataJson) -> "AnalyzerData":
        versions_json = json_obj.get("versions")
        public = json_obj.get("public")
        if versions_json is None or public is None or type(public) != bool:
            raise Exception(f"Unable to parse AnalyzerData from {json_obj}")

        version_to_manifest = {}
        for version, manifest_with_state_json in versions_json.items():
            try:
                manifest_with_state = ManifestWithState.from_json(
                    manifest_with_state_json
                )
                version_to_manifest[Version(version)] = manifest_with_state
            except IncompatibleManifestException:
                logging.warning(f"Skipping this manifest: {manifest_with_state_json}")
        return cls(version_to_manifest, public)


RegistryDataJson = Dict[str, AnalyzerDataJson]


@attr.s(auto_attribs=True)
class RegistryData:
    data: Dict[AnalyzerName, AnalyzerData]

    @classmethod
    def from_json(cls, data_json: RegistryDataJson) -> "RegistryData":
        return cls(
            {
                AnalyzerName(name): AnalyzerData.from_json(analyzer_data_json)
                for name, analyzer_data_json in data_json.items()
            }
        )

    def to_json(self) -> RegistryDataJson:
        return {
            str(name): analyzer_data.to_json()
            for name, analyzer_data in self.data.items()
        }

    def deepcopy(self):
        return RegistryData(copy.deepcopy(self.data))

    def analyzer_for(self, analyzer_name: AnalyzerName) -> AnalyzerData:
        return self.data[analyzer_name]

    def manifest_for(self, va: VersionedAnalyzer) -> AnalyzerManifest:
        manifest_with_state = self.manifest_with_state_for(va)
        if not manifest_with_state:
            raise ManifestNotFoundException(
                f"Manifest could not be found for {va.name} in registry"
            )
        return manifest_with_state.manifest

    def manifest_with_state_for(self, va: VersionedAnalyzer) -> ManifestWithState:
        analyzer_data = self.data.get(va.name)
        if not analyzer_data:
            raise ManifestNotFoundException(
                f"Manifest could not be found for {va.name} in registry"
            )
        manifest_with_state = analyzer_data.versions.get(va.version)
        if not manifest_with_state:
            raise ManifestNotFoundException(
                f"Manifest could not be found for {va.name} at version {va.version} in registry"
            )
        return manifest_with_state

    def public_data(self) -> "RegistryData":
        return self.__class__(
            {key: value for key, value in self.data.items() if value.public}
        )

    def org_data(self) -> "RegistryData":
        return self.__class__(
            {key: value for key, value in self.data.items() if not value.public}
        )

    def merge_with(self, other: "RegistryData") -> "RegistryData":
        """
            Combine the two registry data objects into one and return that new object
            Disallow analyzer name clashes
        """

        if set(self.data.keys()).intersection(set(other.data.keys())):
            raise Exception(
                "Can't merge two registries with overlapping analyzer names"
            )

        new_reg = self.deepcopy()
        new_reg.data.update(other.data)
        return new_reg

    def add_pending_manifest(
        self,
        manifest: AnalyzerManifest,
        force: bool = False,
        overwrite_pending: bool = False,
    ) -> "RegistryData":
        """
            Add this manifest into the current registry data as pending upload.
            This method first verifies that:
            1. Name conforms to org/name
            2. This is not a duplicate versioned analyzer
            3. It's dependencies can be resolved
            4. It doesn't cause circular dependencies

            Arguments:
                manifest: The manifest of the analyzer we want to add to the registry
                force: Force overwrite into registry if manifest already exists with matching name and version.
                    This flag nullifies the InvalidManifestException thrown for manifest that already exists

            Returns:
                A new RegistryData object with manifest added in.

            Throws:
                An InvalidManifestException if the manifest can't be added
        """
        name = manifest.analyzer_name
        version = manifest.version
        va = VersionedAnalyzer(name, version)
        # check that name looks like org/name
        # don't do this check for now until we change analyzer naming everywhere else
        # TODO: Actually get the current org's name current_org
        # if not is_analyzer_of_org(name, current_org):
        #     raise Exception(f"Analyzer name must be of the form {org_name}/name")

        # create here and return at the end because it comes in handy
        new_reg = self.UNSAFE_add_manifest(manifest)
        # check that we can resolve its dependencies
        for dep in manifest.dependencies:
            # Check that it doesn't depend on itself
            if dep.name == name:
                raise InvalidManifestException(
                    f"Resolving this dependency: {dep} But analyzer can't depend on itself."
                )
            resolved_version = new_reg._resolve(
                AnalyzerName(dep.name), dep.wildcard_version
            )

            if dep.path:
                if not os.path.isdir(dep.path) or not os.path.exists(dep.path):
                    raise InvalidLocalPathException(
                        f"A dependency in this manifest cannot be resolved: {dep}"
                    )
            else:
                if resolved_version is None:
                    raise InvalidManifestException(
                        f"A dependency in this manifest cannot be resolved: {dep}"
                    )

        # Check that we don't already have a manifest for it.
        # i.e. don't allow a new manifest without changing analyzer version.
        # TODO: check that it's increased
        analyzer_data = self.data.get(name)
        if analyzer_data:
            if version in analyzer_data.versions.keys():
                pending = analyzer_data.versions[version].pending
                if not force:
                    if not (overwrite_pending and pending):
                        print(f"overwrite: {overwrite_pending}, pending: {pending}")
                        raise InvalidManifestException(
                            f"A manifest for this analyzer and version already exists: {va}"
                        )

        # and see if it can be topologically sorted
        deps_graph = new_reg._dependency_graph()
        try:
            deps_graph.topo_sorted()
        except CircularDependencyError:
            raise InvalidManifestException(
                f"This manifest would cause a cycle in the dependendency graph"
            )

        # all is well? return the new registry
        return new_reg

    def UNSAFE_add_manifest(self, manifest: AnalyzerManifest) -> "RegistryData":
        name = manifest.analyzer_name
        pending_manifest = ManifestWithState(manifest)
        new_reg = self.deepcopy()

        if name not in new_reg.data:
            new_reg.data[name] = AnalyzerData({}, False)

        new_reg.data[name].versions[manifest.version] = pending_manifest
        return new_reg

    def mark_uploaded(self, va: VersionedAnalyzer) -> "RegistryData":
        """
            Marks a pending versioned analyzer's manifest as uploaded. This should be called after
            checking that the versioned analyzer image has in fact been uploaded to docker repository.

            Returns:
                The new RegistryData object.
        """
        new_reg = self.deepcopy()
        manifest_with_state = new_reg.manifest_with_state_for(va)

        if not manifest_with_state:
            raise ManifestNotFoundException(
                f"Analyzer {va.name} does not exist in registry"
            )
        manifest_with_state.set_not_pending()
        return new_reg

    def mark_public(self, name: AnalyzerName) -> "RegistryData":
        """
            mark a private analyzer as public and return a new RegistryData.
        """
        new_reg = self.deepcopy()

        analyzer_data = new_reg.get(name)
        if not analyzer_data:
            raise ManifestNotFoundException(
                f"Analyzer {name} does not exist in registry"
            )

        analyzer_data.set_public()
        return new_reg

    def exclude_pending(self) -> "RegistryData":
        return RegistryData(
            {
                analyzer_name: AnalyzerData(
                    {
                        version: manifest_with_state
                        for version, manifest_with_state in analyzer_data.versions.items()
                        if not manifest_with_state.pending
                    },
                    analyzer_data.public,
                )
                for analyzer_name, analyzer_data in self.data.items()
            }
        )

    def get_direct_dependencies(self, va: VersionedAnalyzer) -> List[SpecifiedAnalyzer]:
        """
            Returns direct dependencies of an analyzer
        """
        manifest = self.manifest_for(va)
        if manifest is None:
            raise ManifestNotFoundException(f"manifest not found for {va}.")

        resolved_values = []
        for dep in manifest.dependencies:
            resolved_version = self._resolve(
                AnalyzerName(dep.name), dep.wildcard_version
            )
            if resolved_version is not None:
                resolved_values.append(
                    SpecifiedAnalyzer(
                        AnalyzerName(dep.name), resolved_version, dep.parameters
                    )
                )

        return resolved_values

    def only_latest(self) -> "RegistryData":
        new_registry_data = {}
        for analyzer_name in self.data.keys():
            if self.data[analyzer_name].versions.keys():
                latest_version = sorted(self.data[analyzer_name].versions.keys())[-1]
                new_registry_data[analyzer_name] = AnalyzerData(
                    {latest_version: self.data[analyzer_name].versions[latest_version]},
                    self.data[analyzer_name].public,
                )
        return RegistryData(new_registry_data)

    def sorted_deps(
        self, specified_analyzer: SpecifiedAnalyzer
    ) -> List[SpecifiedAnalyzer]:
        """
            DAG of all recursive dependencies for this analyzer version.
            Resolution of ranges to pinned versions also happens here.

            Resolution of parameters also happens here
        """
        deps_graph = self._dependency_graph(subgraph_from_node=specified_analyzer)
        topo_sorted = deps_graph.topo_sorted()
        return list(reversed(topo_sorted))

    @property
    def versioned_analyzers(self) -> List[VersionedAnalyzer]:
        return [
            VersionedAnalyzer(analyzer_name, version)
            for analyzer_name, analyzer_data in self.data.items()
            for version in analyzer_data.versions.keys()
        ]

    def _resolve(
        self, analyzer_name: AnalyzerName, spec_string: str
    ) -> Optional[Version]:

        if analyzer_name not in self.data:
            return None
        all_versions = [version for version in self.data[analyzer_name].versions.keys()]

        return SimpleSpec(spec_string).select(all_versions)

    def _dependency_graph(
        self, subgraph_from_node: SpecifiedAnalyzer = None
    ) -> Graph[SpecifiedAnalyzer]:
        edges = set()
        nodes = set()

        if subgraph_from_node:
            to_explore = set([subgraph_from_node])
        else:
            to_explore = set(
                SpecifiedAnalyzer(va.name, va.version)
                for va in self.versioned_analyzers
            )

        # this loop terminates after at most sum(len(deps)) because we always pop values off
        # `to_explore` and add them to `nodes`, and only add values to `to_explore` if
        # they're not in `nodes`.
        while to_explore:
            sa = to_explore.pop()
            next_manifest = self.manifest_for(sa.versioned_analyzer)
            if not next_manifest:
                raise ManifestNotFoundException(
                    f"manifest not found for analyzer {sa.versioned_analyzer.name} at version {sa.versioned_analyzer.version}. Registry data: {self.to_json()}"
                )

            deps = next_manifest.dependencies

            nodes.add(sa)
            for dep in deps:
                resolved_version = self._resolve(
                    AnalyzerName(dep.name), dep.wildcard_version
                )
                if resolved_version is None:
                    raise Exception(f"Can't resolve dependency {dep} of {sa}")

                specified_dep = SpecifiedAnalyzer(
                    dep.name, resolved_version, dep.parameters
                )

                edges.add((sa, specified_dep))
                if specified_dep not in nodes:
                    to_explore.add(specified_dep)

        return Graph(list(nodes), list(edges))


def is_analyzer_of_org(analyzer_name: str, org_name: str) -> bool:
    # check that the name is in the form org/name
    parts = analyzer_name.split("/")
    if not len(parts) > 1:
        return False

    # make sure analyzer org name matches the org adding the manifest
    if not parts[0] == org_name:
        return False
    return True
