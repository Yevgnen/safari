# -*- coding: utf-8 -*-

import glob
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


class FirefoxCloudTabs(CloudTabMixin):
    def get_cloud_tabs(self) -> Iterable[URLItem]:
        raise NotImplementedError()


class FirefoxReadings(ReadingMixin):
    def get_readings(self) -> Iterable[URLItem]:
        raise NotImplementedError()


class FirefoxBookmarks(BookmarkMixin):
    def get_bookmarks(self, flatten: bool = True) -> Union[Iterable[URLItem], Dict]:
        raise NotImplementedError()


class FirefoxHistories(HistoryMixin):
    def get_histories(self) -> Iterable[Dict]:
        with sqlite3.connect(self.history_file) as conn:
            sql = """
            SELECT place_id, url, title, datetime((visit_date/1000000), 'unixepoch', 'localtime') AS visit_date
            FROM moz_places INNER JOIN moz_historyvisits on moz_historyvisits.place_id = moz_places.id
            ORDER BY visit_date DESC
            """

            for id_, url, title, visit_time in conn.cursor().execute(sql):
                yield {
                    "id": id_,
                    "url": url,
                    "title": title,
                    "visit_time": visit_time,
                }


DEFAULT_LIBRARY_PATH = os.path.join(
    os.environ["HOME"], "Library", "Application Support", "Firefox", "Profiles"
)


class Firefox(
    ExportMixin, FirefoxCloudTabs, FirefoxReadings, FirefoxBookmarks, FirefoxHistories
):
    def __init__(self, library: str = DEFAULT_LIBRARY_PATH):
        super().__init__()

        self.library = library

        files = glob.glob(
            os.path.join(self.library, "*.default*", "places.sqlite"), recursive=True
        )
        if not files:
            raise RuntimeError(f"History file not found in {self.library}")
        self.history_file = files[0]
