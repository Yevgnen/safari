# -*- coding: utf-8 -*-

import os
import sqlite3
from typing import Dict, Iterable, Union

from resworb.base import (
    BookmarkMixin,
    CloudTabMixin,
    HistoryMixin,
    ReadingMixin,
    URLItem,
)
from resworb.exporter import ExportMixin


class ChromeCloudTabs(CloudTabMixin):
    def get_cloud_tabs(self) -> Iterable[URLItem]:
        raise NotImplementedError()


class ChromeReadings(ReadingMixin):
    def get_readings(self) -> Iterable[URLItem]:
        raise NotImplementedError()


class ChromeBookmarks(BookmarkMixin):
    def get_bookmarks(self, flatten: bool = True) -> Union[Iterable[URLItem], Dict]:
        raise NotImplementedError()


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
    ExportMixin, ChromeCloudTabs, ChromeReadings, ChromeBookmarks, ChromeHistories
):
    def __init__(self, library: str = DEFAULT_LIBRARY_PATH):
        super().__init__()

        self.library = library
        self.history_file = os.path.join(library, "History")
