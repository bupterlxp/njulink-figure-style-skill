#!/usr/bin/env python3
"""Copy a bundled upstream recipe and its CSV, then render in a working directory."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent


def render(ident: str, output: Path) -> None:
    if Path(ident).name != ident:
        raise ValueError("Use a gallery id, not a path.")
    source = ROOT / "gallery" / f"{ident}.py"
    if not source.is_file():
        raise ValueError(f"No bundled Python recipe for {ident}")
    output = output.resolve()
    if output == (ROOT / "gallery").resolve():
        raise ValueError("Choose a working directory so the bundled reference is preserved.")
    output.mkdir(parents=True, exist_ok=True)
    target = output / source.name
    companion = source.with_suffix(".csv")
    destinations = [target, *( [output / companion.name] if companion.exists() else [])]
    destinations += [target.with_suffix("." + ext) for ext in ("png", "pdf", "svg")]
    if any(path.exists() for path in destinations):
        raise FileExistsError(f"{ident}: output already exists; choose a fresh output directory.")
    # The source stays runnable, including any relative CSV path. Retain its
    # original code and add vector exports for recipes that only save PNG.
    extra = '\n# Added by NJU-LINK integration: companion vector exports.\n'
    extra += 'fig.savefig(Path(__file__).with_suffix(".pdf"))\n'
    extra += 'fig.savefig(Path(__file__).with_suffix(".svg"))\n'
    license_text = (ROOT / "licenses" / "plot-is-all-you-need-MIT.txt").read_text(encoding="utf-8")
    attribution = "# Upstream: https://github.com/liouhai/plot-is-all-you-need\n"
    attribution += "\n".join("# " + line for line in license_text.splitlines()) + "\n\n"
    target.write_text(attribution + source.read_text(encoding="utf-8") + extra, encoding="utf-8")
    if companion.exists():
        shutil.copyfile(companion, output / companion.name)
    env = dict(os.environ, MPLBACKEND="Agg")
    subprocess.run([sys.executable, str(target)], env=env, cwd=output, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ids", nargs="+", help="one or more ids from gallery/INDEX.md")
    parser.add_argument("--out", type=Path, default=Path("figures"))
    args = parser.parse_args()
    for ident in args.ids:
        render(ident, args.out)


if __name__ == "__main__":
    main()
