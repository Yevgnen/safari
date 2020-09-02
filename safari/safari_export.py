# -*- coding: utf-8 -*-

import argparse
import json
import os

from safari import Safari


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        default="bookmarks",
        help="Bookmark types ('bookmarks', 'readings', 'all') (default: 'bookmarks')",
    )
    parser.add_argument(
        "-t",
        "--target",
        type=str,
        default="safari_exported.json",
        help="Output file name. (default 'safari_exported.json')",
    )
    parser.add_argument(
        "-l",
        "--library",
        type=str,
        default="~/Library/Safari/",
        help="Safari library location (default: '~/Library/Safari/')",
    )
    args = parser.parse_args()

    return args


def main():
    args = parse_args()
    safari = Safari(os.path.abspath(os.path.expanduser(args.library)))

    sources = {"bookmarks", "readings"}
    if args.source != "all":
        sources = {args.source}

    results = {source: list(getattr(safari, source)) for source in sources}

    with open(args.target, mode="w") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
