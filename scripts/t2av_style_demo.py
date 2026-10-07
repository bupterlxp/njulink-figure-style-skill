#!/usr/bin/env python3
"""Render the compact T2AV-inspired overview using shared measured panels."""
from __future__ import annotations
import argparse
from pathlib import Path
from compass_panels import build_figure, export
import matplotlib.pyplot as plt


def build_demo(font='reference'):
    return build_figure(include_pipeline=False, font=font)[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=Path('demo-output'))
    parser.add_argument('--font', choices=['reference', 'portable'], default='reference')
    args = parser.parse_args()
    fig, metadata = build_figure(include_pipeline=False, font=args.font)
    for path in export(fig, metadata, args.output_dir/'t2av-compass-style-demo'):
        print(path)
    plt.close(fig)


if __name__ == '__main__':
    main()
