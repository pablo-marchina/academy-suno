#!/usr/bin/env python3
"""Build a deterministic source release bundle, SPDX SBOM, and local provenance.

The SPDX graph follows only the root project's production dependencies and their
transitive closure from uv.lock. Test and benchmark-only groups remain locked for
repository reproducibility but are intentionally excluded from the releasable
artifact's runtime dependency graph.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import tarfile
import tomllib
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
INCLUDE_DIRS = (
    Path("src"),
    Path("app"),
    Path("docs/production/contracts/v1"),
)
INCLUDE_FILES = (
    Path("pyproject.toml"),
    Path("uv.lock"),
    Path(".python-version"),
    Path("toolchain.lock.json"),
)
ROOT_PACKAGE = "academy-suno"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def release_files() -> list[Path]:
    files: list[Path] = []
    for relative in INCLUDE_FILES:
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(f"required release input missing: {relative}")
        files.append(relative)
    for relative in INCLUDE_DIRS:
        directory = ROOT / relative
        if not directory.is_dir():
            raise FileNotFoundError(f"required release input directory missing: {relative}")
        for path in directory.rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts:
                files.append(path.relative_to(ROOT))
    return sorted(set(files), key=lambda item: item.as_posix())


def build_tar_gz(output: Path, files: list[Path]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
            with tarfile.open(fileobj=zipped, mode="w", format=tarfile.PAX_FORMAT) as archive:
                for relative in files:
                    source = ROOT / relative
                    info = archive.gettarinfo(str(source), arcname=relative.as_posix())
                    info.uid = 0
                    info.gid = 0
                    info.uname = ""
                    info.gname = ""
                    info.mtime = 0
                    info.mode = 0o755 if os.access(source, os.X_OK) else 0o644
                    with source.open("rb") as handle:
                        archive.addfile(info, handle)


def spdx_id(name: str, version: str) -> str:
    token = re.sub(r"[^A-Za-z0-9.-]+", "-", f"{name}-{version}")
    return f"SPDXRef-Package-{token.strip('-') or 'unknown'}"


def dependency_names(package: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for dependency in package.get("dependencies", []):
        if isinstance(dependency, dict) and dependency.get("name"):
            names.append(str(dependency["name"]))
    return names


def production_lock_graph(lock_path: Path) -> tuple[dict[str, dict[str, Any]], list[str]]:
    payload = tomllib.loads(lock_path.read_text(encoding="utf-8"))
    packages = payload.get("package", [])
    by_name: dict[str, dict[str, Any]] = {}
    for package in packages:
        name = str(package.get("name", "")).strip()
        if not name:
            continue
        if name in by_name:
            raise ValueError(f"ambiguous duplicate locked package name: {name}")
        by_name[name] = package

    root = by_name.get(ROOT_PACKAGE)
    if root is None:
        raise ValueError(f"root package {ROOT_PACKAGE!r} missing from uv.lock")
    direct = dependency_names(root)
    selected: dict[str, dict[str, Any]] = {}
    stack = list(direct)
    while stack:
        name = stack.pop()
        if name in selected:
            continue
        package = by_name.get(name)
        if package is None:
            raise ValueError(f"locked dependency {name!r} referenced but not defined")
        selected[name] = package
        stack.extend(dependency_names(package))
    return selected, sorted(direct)


def package_to_spdx(package: dict[str, Any]) -> dict[str, Any]:
    name = str(package["name"])
    version = str(package["version"])
    return {
        "SPDXID": spdx_id(name, version),
        "name": name,
        "versionInfo": version,
        "downloadLocation": "NOASSERTION",
        "filesAnalyzed": False,
        "licenseConcluded": "NOASSERTION",
        "licenseDeclared": "NOASSERTION",
        "externalRefs": [{
            "referenceCategory": "PACKAGE-MANAGER",
            "referenceType": "purl",
            "referenceLocator": f"pkg:pypi/{name}@{version}",
        }],
    }


def build_sbom(artifact: Path, lock_path: Path, output: Path) -> int:
    artifact_sha = digest(artifact)
    graph, direct = production_lock_graph(lock_path)
    artifact_package = {
        "SPDXID": "SPDXRef-Package-academy-suno",
        "name": "academy-suno-release-bundle",
        "versionInfo": "0.0.0",
        "downloadLocation": "NOASSERTION",
        "filesAnalyzed": False,
        "licenseConcluded": "NOASSERTION",
        "licenseDeclared": "NOASSERTION",
        "checksums": [{"algorithm": "SHA256", "checksumValue": artifact_sha}],
    }
    dependencies = [package_to_spdx(graph[name]) for name in sorted(graph)]
    relationships: list[dict[str, str]] = [{
        "spdxElementId": "SPDXRef-DOCUMENT",
        "relationshipType": "DESCRIBES",
        "relatedSpdxElement": artifact_package["SPDXID"],
    }]
    for name in direct:
        package = graph[name]
        relationships.append({
            "spdxElementId": artifact_package["SPDXID"],
            "relationshipType": "DEPENDS_ON",
            "relatedSpdxElement": spdx_id(name, str(package["version"])),
        })
    for name, package in sorted(graph.items()):
        source_id = spdx_id(name, str(package["version"]))
        for target_name in dependency_names(package):
            target = graph.get(target_name)
            if target is None:
                continue
            relationships.append({
                "spdxElementId": source_id,
                "relationshipType": "DEPENDS_ON",
                "relatedSpdxElement": spdx_id(target_name, str(target["version"])),
            })
    document = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": f"academy-suno-{artifact_sha[:12]}",
        "documentNamespace": f"https://github.com/pablo-marchina/academy-suno/spdx/{artifact_sha}",
        "creationInfo": {
            "created": "1970-01-01T00:00:00Z",
            "creators": ["Tool: scripts/supply_chain/build_release_evidence.py"],
        },
        "packages": [artifact_package, *dependencies],
        "relationships": relationships,
    }
    output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return len(dependencies)


def build_provenance(artifact: Path, sbom: Path, lock_path: Path, output: Path) -> None:
    payload = {
        "schema_version": "academy-suno-local-provenance.v1",
        "artifact": {"path": artifact.name, "sha256": digest(artifact)},
        "sbom": {"path": sbom.name, "sha256": digest(sbom), "format": "SPDX-2.3"},
        "lockfile": {"path": lock_path.name, "sha256": digest(lock_path)},
        "repository": os.environ.get("GITHUB_REPOSITORY", "pablo-marchina/academy-suno"),
        "commit_sha": os.environ.get("GITHUB_SHA", "UNKNOWN"),
        "ref": os.environ.get("GITHUB_REF", "UNKNOWN"),
        "workflow": os.environ.get("GITHUB_WORKFLOW", "LOCAL"),
        "run_id": os.environ.get("GITHUB_RUN_ID", "LOCAL"),
        "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT", "LOCAL"),
        "builder": "github-actions" if os.environ.get("GITHUB_ACTIONS") == "true" else "local",
        "production_ready_claim": False,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--artifact-name", default="academy-suno-source.tar.gz")
    args = parser.parse_args()

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    artifact = output_dir / args.artifact_name
    sbom = output_dir / f"{args.artifact_name}.spdx.json"
    provenance = output_dir / f"{args.artifact_name}.provenance.json"
    lock_path = ROOT / "uv.lock"

    build_tar_gz(artifact, release_files())
    production_dependency_count = build_sbom(artifact, lock_path, sbom)
    build_provenance(artifact, sbom, lock_path, provenance)

    summary = {
        "artifact": str(artifact),
        "artifact_sha256": digest(artifact),
        "sbom": str(sbom),
        "sbom_sha256": digest(sbom),
        "provenance": str(provenance),
        "production_dependency_count": production_dependency_count,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
