#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import os

from resworb.browsers.safari import Safari
from resworb.exporter import JSONExporter, PickleExporter, TOMLExporter, YAMLExporter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_arguments(parser):
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        default="all",
        help=(
            "Resource types ('opened_tabs', 'cloud_tabs', 'readings', 'bookmarks', 'all') "
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
        ".pkl": PickleExporter,
        ".pickle": PickleExporter,
    }
    file_type = os.path.splitext(target)[1]
    exporter_class = export_factory.get(file_type)
    if exporter_class is None:
        raise ValueError(f"Unsupported file type: {file_type}")
    exporter = exporter_class()

    records = Safari(library=library).export(source)

    exporter.export_to_file(records, target)

    logger.info("Export statistics:")
    for source, data in records.items():
        if source == "cloud_tabs":
            logger.info("%s\t%d", source, sum(len(x["tabs"]) for x in data))
        else:
            logger.info("%s\t%d", source, len(data))


def main():
    args = parse_args()
    export(args.source, args.target, args.library)
