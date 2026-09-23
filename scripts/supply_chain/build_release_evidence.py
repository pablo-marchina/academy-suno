#!/usr/bin/env python3
"""Build a deterministic source release bundle, SPDX SBOM, and local provenance.

The GitHub-native attestation is added by CI after this script binds the artifact,
lockfile and SBOM by SHA-256.
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


def lock_packages(lock_path: Path) -> list[dict[str, Any]]:
    payload = tomllib.loads(lock_path.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for package in payload.get("package", []):
        name = str(package.get("name", "")).strip()
        version = str(package.get("version", "")).strip()
        if not name or not version or (name, version) in seen:
            continue
        seen.add((name, version))
        rows.append({
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
        })
    return sorted(rows, key=lambda row: (row["name"].lower(), row["versionInfo"]))


def build_sbom(artifact: Path, lock_path: Path, output: Path) -> None:
    artifact_sha = digest(artifact)
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
    dependencies = lock_packages(lock_path)
    relationships = [
        {
            "spdxElementId": "SPDXRef-DOCUMENT",
            "relationshipType": "DESCRIBES",
            "relatedSpdxElement": artifact_package["SPDXID"],
        }
    ]
    relationships.extend(
        {
            "spdxElementId": artifact_package["SPDXID"],
            "relationshipType": "DEPENDS_ON",
            "relatedSpdxElement": package["SPDXID"],
        }
        for package in dependencies
        if package["SPDXID"] != artifact_package["SPDXID"]
    )
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
    build_sbom(artifact, lock_path, sbom)
    build_provenance(artifact, sbom, lock_path, provenance)

    summary = {
        "artifact": str(artifact),
        "artifact_sha256": digest(artifact),
        "sbom": str(sbom),
        "sbom_sha256": digest(sbom),
        "provenance": str(provenance),
        "locked_package_count": len(lock_packages(lock_path)),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
