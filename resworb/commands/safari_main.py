# -*- coding: utf-8 -*-

import argparse

from resworb.commands import safari_export


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        dest="command",
        help="sub-command help",
        required=True,
    )
    export_parser = subparsers.add_parser("export", help="Export Safari data")
    safari_export.add_arguments(export_parser)
    args = parser.parse_args()

    return args


def main():
    args = parse_args()

    if args.command == "export":
        safari_export.export(args.source, args.target, args.library)
