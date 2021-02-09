# -*- coding: utf-8 -*-

import json
import os
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


class ChromeOpenedTabs(OpenedTabMixin):
    def get_opened_tabs(self) -> Iterable[URLItem]:
        raise NotImplementedError()


class ChromeCloudTabs(CloudTabMixin):
    def get_cloud_tabs(self) -> Iterable[URLItem]:
        raise NotImplementedError()


class ChromeReadings(ReadingMixin):
    def get_readings(self) -> Iterable[URLItem]:
        raise NotImplementedError()


class ChromeBookmarks(BookmarkMixin):
    def get_bookmarks(self, flatten: bool = True) -> Union[Iterable[URLItem], Dict]:
        def _get_bookmarks(node, folders):
            children = node.get("children")
            if children is not None:
                for child in children:
                    yield from _get_bookmarks(child, folders + [node["name"]])
            else:
                yield {
                    "title": node["name"],
                    "url": node["url"],
                    "folders": folders,
                }

        with open(self.bookmark_file, mode="r") as f:
            data = json.load(f)

        roots = data.get("roots", {})
        for root_key, root_value in roots.items():
            yield from _get_bookmarks(root_value, [root_value["name"]])


class ChromeHistories(HistoryMixin):
    def get_histories(self) -> Iterable[Dict]:
        with sqlite3.connect(self.history_file) as conn:
            sql = """
            SELECT url, title, datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime')
            AS last_visit_time FROM urls ORDER BY last_visit_time DESC"""

            for url, title, visit_time in conn.cursor().execute(sql):
                yield {
                    "id": None,
                    "url": url,
                    "title": title,
                    "visit_time": visit_time,
                }


DEFAULT_LIBRARY_PATH = os.path.join(
    os.environ["HOME"], "Library", "Application Support", "Google", "Chrome", "Default"
)


class Chrome(
    ExportMixin,
    ChromeOpenedTabs,
    ChromeCloudTabs,
    ChromeReadings,
    ChromeBookmarks,
    ChromeHistories,
):
    def __init__(self, library: str = DEFAULT_LIBRARY_PATH):
        super().__init__()

        self.library = library
        self.bookmark_file = os.path.join(library, "Bookmarks")
        self.history_file = os.path.join(library, "History")
