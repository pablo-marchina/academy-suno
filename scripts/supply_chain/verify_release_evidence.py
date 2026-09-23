#!/usr/bin/env python3
"""Fail-closed verifier for the W006-T008 release artifact, SPDX SBOM and provenance."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"verification failed: {message}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--sbom", type=Path, required=True)
    parser.add_argument("--provenance", type=Path, required=True)
    parser.add_argument("--lockfile", type=Path, default=Path("uv.lock"))
    args = parser.parse_args()

    for path in (args.artifact, args.sbom, args.provenance, args.lockfile):
        if not path.is_file():
            fail(f"missing {path}")

    artifact_sha = digest(args.artifact)
    sbom_sha = digest(args.sbom)
    lock_sha = digest(args.lockfile)
    sbom = json.loads(args.sbom.read_text(encoding="utf-8"))
    provenance = json.loads(args.provenance.read_text(encoding="utf-8"))

    if sbom.get("spdxVersion") != "SPDX-2.3":
        fail("SBOM is not SPDX-2.3")
    packages = sbom.get("packages")
    if not isinstance(packages, list) or len(packages) < 2:
        fail("SBOM does not enumerate the release plus locked dependencies")
    release = next(
        (row for row in packages if row.get("SPDXID") == "SPDXRef-Package-academy-suno"),
        None,
    )
    if release is None:
        fail("release package missing from SBOM")
    checksums = release.get("checksums", [])
    if not any(
        row.get("algorithm") == "SHA256" and row.get("checksumValue") == artifact_sha
        for row in checksums
    ):
        fail("SBOM artifact SHA-256 mismatch")

    relationships = sbom.get("relationships", [])
    dependency_edges = [
        row
        for row in relationships
        if row.get("spdxElementId") == "SPDXRef-Package-academy-suno"
        and row.get("relationshipType") == "DEPENDS_ON"
    ]
    if not dependency_edges:
        fail("SBOM dependency relationships missing")

    if provenance.get("artifact", {}).get("sha256") != artifact_sha:
        fail("provenance artifact SHA-256 mismatch")
    if provenance.get("sbom", {}).get("sha256") != sbom_sha:
        fail("provenance SBOM SHA-256 mismatch")
    if provenance.get("lockfile", {}).get("sha256") != lock_sha:
        fail("provenance lockfile SHA-256 mismatch")
    if provenance.get("production_ready_claim") is not False:
        fail("provenance must not claim production readiness")

    result = {
        "status": "PASS",
        "artifact_sha256": artifact_sha,
        "sbom_sha256": sbom_sha,
        "lockfile_sha256": lock_sha,
        "sbom_package_count": len(packages),
        "dependency_edge_count": len(dependency_edges),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"verification failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1)
