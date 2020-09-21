# -*- coding: utf-8 -*-

import abc
import argparse
import datetime
import itertools
import json
import os

from safari import Safari
from safari.utils import copy_to_clipboard


class Exporter(object):
    @abc.abstractmethod
    def to_string(self, results):
        raise NotImplementedError()

    @abc.abstractmethod
    def export_to_file(self, filename):
        raise NotImplementedError()

    def export_to_clipboard(self, results):
        string = self.to_string(results)
        copy_to_clipboard(string)


class OrgExporter(Exporter):
    def format_org_link(self, title, url):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %a %H:%M")

        return f"* [[{url}][{title}]]\n[{timestamp}]"

    def to_string(self, results):
        return "".join(
            f"{self.format_org_link(**item)}\n\n"
            for item in itertools.chain.from_iterable(results.values())
        )

    def export_to_file(self, results, filename):
        with open(filename, mode="w") as f:
            f.writelines(self.to_string(results))


class JsonExporter(Exporter):
    def to_string(self, results):
        return json.dumps(results)

    def export_to_file(self, results, filename):
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
        default=None,
        help=(
            "Output file name. None means clipboard, "
            "org format will be used. (default: None)"
        ),
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
    if not args.target:
        exporter = OrgExporter()
        exporter.export_to_clipboard(results)
        return

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
    exporter.export_to_file(results, args.target)


if __name__ == "__main__":
    main()
