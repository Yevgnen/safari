# -*- coding: utf-8 -*-

import os
import plistlib
import sqlite3
import subprocess
import tempfile
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
        # References & credits:
        # https://gist.github.com/kshiteesh/b72e93d31d65008fcd11
        #
        # Modifications:
        # 1. Don't activate Safari.
        # 2. Don't use markdown format when output.
        # 3. Write to temp file instead of prompting for a filename.

        temp = tempfile.mkstemp(text=True)[1]

        script = f"""
        -- NAME OF REPORT TITLE
        property report_Title : "URL List from Safari"

        -- PREPARE THE LIST
        set url_list to {{}}

        -- GET TABS FROM SAFARI
        set window_count to 1
        tell application "Safari"
                set safariWindow to windows
                repeat with w in safariWindow
                        try
                                repeat with t in (tabs of w)
                                        set TabInfo to (URL of t & "\t" & NAME of t)
                                        copy TabInfo to the end of url_list
                                end repeat
                        end try
                        set window_count to window_count + 1
                end repeat
        end tell

        -- CONVERT URL_LIST TO TEXT
        set old_delim to AppleScript's text item delimiters
        set AppleScript's text item delimiters to return
        set url_list to url_list as text
        set AppleScript's text item delimiters to old_delim

        --WRITE THE FILE
        tell application "System Events"
                set save_File to open for access ("{temp}" as string) with write permission
                try
                        write url_list to save_File as «class utf8»
                end try
                close access save_File
        end tell
        """
        subprocess.run(["osascript", "-e", script], check=True)

        with open(temp, mode="r") as f:
            for line in f:
                url, title = line.split("\t")
                yield {
                    "title": title.rstrip(),
                    "url": url,
                }


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
