# -*- coding: utf-8 -*-

import os
import plistlib
from typing import Dict, Iterable, Union

URLItem = Dict[str, str]


class SafariBookmarks(object):
    def __init__(
        self, library: str = os.path.join(os.environ["HOME"], "Library", "Safari")
    ):
        self.bookmark_file = os.path.join(library, "Bookmarks.plist")
        self.bookmark_plist = None

    def _load_bookmarks(self):
        if self.bookmark_plist is None:
            with open(self.bookmark_file, mode="rb") as plist_file:
                self.bookmark_plist = plistlib.load(plist_file)

    def get_bookmarks(self, flatten: bool = True) -> Union[Iterable[URLItem], Dict]:
        self._load_bookmarks()

        def _get_bookmarks(node):
            if isinstance(node, list):
                return [_get_bookmarks(x) for x in node]

            if isinstance(node, dict):
                if node["WebBookmarkType"] == "WebBookmarkTypeList":
                    return {
                        "folder": node["Title"],
                        "children": [
                            _get_bookmarks(x) for x in node.get("Children", [])
                        ],
                    }

                if node["WebBookmarkType"] == "WebBookmarkTypeLeaf":
                    children = node.get("Children")
                    if children is not None:
                        return {
                            "folder": node["Title"],
                            "children": [_get_bookmarks(x) for x in children],
                        }

                    return {
                        "title": node["URIDictionary"]["title"],
                        "url": node["URLString"],
                    }

            raise ValueError(f"Unknow node type: {node.__class__}")

        def _get_bookmarks_flatten(node, folders):
            if isinstance(node, list):
                for x in node:
                    yield from _get_bookmarks_flatten(x, folders)

            if isinstance(node, dict):
                if node["WebBookmarkType"] == "WebBookmarkTypeList":
                    for x in node.get("Children", []):
                        yield from _get_bookmarks_flatten(x, folders + [node["Title"]])

                if node["WebBookmarkType"] == "WebBookmarkTypeLeaf":
                    children = node.get("Children")
                    if children is not None:
                        for x in children:
                            yield from _get_bookmarks_flatten(
                                x, folders + [node["Title"]]
                            )

                    yield {
                        "title": node["URIDictionary"]["title"],
                        "url": node["URLString"],
                        "folders": folders,
                    }

        bookmarks = self.bookmark_plist["Children"][1]["Children"]
        if flatten:
            return _get_bookmarks_flatten(bookmarks, [])

        return _get_bookmarks(bookmarks)

    def get_readings(self) -> Iterable[URLItem]:
        self._load_bookmarks()

        bookmarks = None
        for child in self.bookmark_plist["Children"]:
            if child.get("Title", None) == "com.apple.ReadingList":
                bookmarks = child
                break

        if not bookmarks:
            return

        for bookmark in bookmarks.get("Children", []):
            yield {
                "title": bookmark["URIDictionary"]["title"],
                "url": bookmark["URLString"],
            }
