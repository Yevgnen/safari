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
    def _get_bookmarks_folders(self):
        with sqlite3.connect(self.history_file) as conn:
            sql = """
            SELECT id, type, parent, title
            FROM moz_bookmarks
            WHERE type=2;
            """
            columns = ["id", "type", "parent", "title"]

            return [dict(zip(columns, r)) for r in conn.cursor().execute(sql)]

    def get_bookmarks(self, flatten: bool = True) -> Union[Iterable[URLItem], Dict]:
        bookmark_folders = self._get_bookmarks_folders()
        bookmark_folders = {x["id"]: x for x in bookmark_folders}

        def _get_bookmark_folders(parent):
            folders = []
            folder = bookmark_folders[parent]
            while folder["parent"] > 0:
                folders += [folder["title"]]
                folder = bookmark_folders[folder["parent"]]

            return list(reversed(folders))

        with sqlite3.connect(self.history_file) as conn:
            sql = """
            SELECT type, parent, moz_bookmarks.title, moz_places.url
            FROM moz_bookmarks
            INNER JOIN moz_places on moz_bookmarks.fk=moz_places.id
            WHERE type=1
            ORDER BY dateAdded desc;
            """

            for type, parent, title, url in conn.cursor().execute(sql):
                yield {
                    "title": title,
                    "url": url,
                    "folders": _get_bookmark_folders(parent),
                }


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
