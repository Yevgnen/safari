#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

from safari import Safari
from safari.exporter import JSONExporter, TOMLExporter, YAMLExporter


def add_arguments(parser):
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        default="all",
        help=(
            "Resource types ('cloud_tabs', 'readings', 'bookmarks', 'all') "
            "(default: 'all')"
        ),
    )
    parser.add_argument(
        "-t",
        "--target",
        type=str,
        required=True,
        help="Output file name.",
    )
    library = os.path.join(os.getenv("HOME"), "Library", "Safari")
    parser.add_argument(
        "-l",
        "--library",
        type=str,
        default=library,
        help=f"Safari library location (default: {library!r})",
    )

    return parser


def parse_args():
    # pylint: disable=redefined-outer-name
    parser = argparse.ArgumentParser()
    parser = add_arguments(parser)
    args = parser.parse_args()

    return args


def export(source: str, target: str, library: str) -> None:
    export_factory = {
        ".yml": YAMLExporter,
        ".yaml": YAMLExporter,
        ".toml": TOMLExporter,
        ".json": JSONExporter,
    }
    file_type = os.path.splitext(target)[1]
    exporter_class = export_factory.get(file_type)
    if exporter_class is None:
        raise ValueError(f"Unsupported file type: {file_type}")
    exporter = exporter_class()

    records = Safari(library=library).export(source)

    exporter.export_to_file(records, target)


def main():
    args = parse_args()
    export(args.source, args.target, args.library)
