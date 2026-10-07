#!/usr/bin/env python3
"""Render a complete multimodal benchmark figure using simulated data.

Layout references: T2AV-Compass overview and prompt pipeline. The artwork is
independently drawn. Exports PNG/PDF/SVG and a font/data manifest together.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from compass_panels import build_figure, export
import matplotlib.pyplot as plt


def build_demo(font='reference'):
    return build_figure(include_pipeline=True, font=font)[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=Path('demo-output'))
    parser.add_argument('--font', choices=['reference', 'portable'], default='reference',
                        help='reference: installed Chalkboard, else bundled Comic Neue; portable: Comic Neue')
    args = parser.parse_args()
    fig, metadata = build_figure(include_pipeline=True, font=args.font)
    for path in export(fig, metadata, args.output_dir/'njulink-style-demo'):
        print(path)
    plt.close(fig)


if __name__ == '__main__':
    main()
