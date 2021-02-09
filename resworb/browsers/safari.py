# -*- coding: utf-8 -*-

import os
import plistlib
import sqlite3
from typing import Dict, Iterable, Union

from resworb.base import (
    BookmarkMixin,
    CloudTabMixin,
    HistoryMixin,
    OpenedTabMixin,
    ReadingMixin,
    URLItem,
)
from resworb.exporter import ExportMixin


class SafariOpenedTabs(OpenedTabMixin):
    def get_opened_tabs(self) -> Iterable[URLItem]:
        raise NotImplementedError()


class SafariCloudTabs(CloudTabMixin):
    def get_devices(self) -> Iterable[Dict[str, str]]:
        with sqlite3.connect(self.cloud_tab_file) as conn:
            sql = "SELECT device_uuid, device_name FROM cloud_tab_devices;"

            for id_, name in conn.cursor().execute(sql):
                yield {
                    "id": id_,
                    "name": name,
                }

    def get_device_cloud_tabs(self, device_id: str) -> Iterable[URLItem]:
        with sqlite3.connect(self.cloud_tab_file) as conn:
            sql = f'SELECT title, url FROM cloud_tabs WHERE device_uuid="{device_id}";'
            for tab in conn.cursor().execute(sql):
                yield {
                    "title": tab[0],
                    "url": tab[1],
                }

    def get_cloud_tabs(self) -> Iterable[URLItem]:
        for device in self.get_devices():
            yield {**device, "tabs": list(self.get_device_cloud_tabs(device["id"]))}


class SafariReadings(ReadingMixin):
    def get_readings(self) -> Iterable[URLItem]:

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


class SafariBookmarks(BookmarkMixin):
    def get_bookmarks(self, flatten: bool = True) -> Union[Iterable[URLItem], Dict]:
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


class SafariHistories(HistoryMixin):
    def get_histories(self) -> Iterable[Dict]:
        with sqlite3.connect(self.history_file) as conn:
            sql = """
            SELECT history_item, url, title, datetime(visit_time + 978307200, 'unixepoch', 'localtime')
            FROM history_visits INNER JOIN history_items ON history_items.id = history_visits.history_item
            ORDER BY visit_time DESC
            """

            for id_, url, title, visit_time in conn.cursor().execute(sql):
                yield {
                    "id": id_,
                    "url": url,
                    "title": title,
                    "visit_time": visit_time,
                }


DEFAULT_LIBRARY_PATH = os.path.join(os.environ["HOME"], "Library", "Safari")


class Safari(
    ExportMixin,
    SafariOpenedTabs,
    SafariCloudTabs,
    SafariReadings,
    SafariBookmarks,
    SafariHistories,
):
    def __init__(self, library: str = DEFAULT_LIBRARY_PATH):
        super().__init__()

        self.library = library
        self.cloud_tab_file = os.path.join(library, "CloudTabs.db")
        self.history_file = os.path.join(library, "History.db")

        self.bookmark_file = os.path.join(library, "Bookmarks.plist")
        with open(self.bookmark_file, mode="rb") as plist_file:
            self.bookmark_plist = plistlib.load(plist_file)
