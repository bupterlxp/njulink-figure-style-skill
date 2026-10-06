#!/usr/bin/env python3
"""Fetch pinned T2AV-Compass image references into an ignored cache.

The public skill stores metadata and links, rather than redistributing the
source figures. This helper is opt-in: it downloads the exact files listed in
``references/t2av-compass-assets.json`` and verifies their SHA-256 digests.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "references" / "t2av-compass-assets.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch(*, output: Path, timeout: int = 30) -> list[Path]:
    manifest = json.loads(MANIFEST.read_text())
    commit = manifest["commit"]
    base = f"https://raw.githubusercontent.com/NJU-LINK/T2AV-Compass/{commit}/docs/static/images"
    output.mkdir(parents=True, exist_ok=True)
    downloaded: list[Path] = []
    for asset in manifest["assets"]:
        destination = output / asset["file"]
        url = f"{base}/{asset['file']}"
        request = Request(url, headers={"User-Agent": "njulink-figure-style-reference-fetcher"})
        with urlopen(request, timeout=timeout) as response:
            destination.write_bytes(response.read())
        actual = sha256(destination)
        expected = asset["sha256"]
        if actual != expected:
            destination.unlink(missing_ok=True)
            raise RuntimeError(f"checksum mismatch for {asset['file']}: {actual} != {expected}")
        downloaded.append(destination)
    return downloaded


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reference-cache" / "t2av-compass",
        help="ignored directory for downloaded references",
    )
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()
    for path in fetch(output=args.output, timeout=args.timeout):
        print(path)


if __name__ == "__main__":
    main()
