# -*- coding: utf-8 -*-

import abc
import argparse
import datetime
import itertools
import json
import os

from safari import Safari


class Exporter(object):
    @abc.abstractmethod
    def export(self, filename):
        raise NotImplementedError()


class OrgExporter(Exporter):
    def format_org_link(self, title, url):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %a %H:%M")

        return f"* [[{url}][{title}]]\n[{timestamp}]"

    def export(self, results, filename):
        with open(filename, mode="w") as f:
            f.writelines(
                f"{self.format_org_link(**item)}\n\n"
                for item in itertools.chain.from_iterable(results.values())
            )


class JsonExporter(Exporter):
    def export(self, results, filename):
        with open(filename, mode="w") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)


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

    # Fetch bookmarks.
    safari = Safari(os.path.abspath(os.path.expanduser(args.library)))
    sources = {"bookmarks", "readings"}
    if args.source != "all":
        sources = {args.source}
    results = {source: list(getattr(safari, source)) for source in sources}

    # Export bookmarks.
    exporters = {
        ".org": OrgExporter(),
        ".json": JsonExporter(),
    }
    ext = os.path.splitext(args.target)[1]
    if not ext:
        ext = ".org"
    exporter = exporters.get(ext)
    if not exporter:
        raise TypeError(f"Unsupported file type: {ext}")
    exporter.export(results, args.target)


if __name__ == "__main__":
    main()
