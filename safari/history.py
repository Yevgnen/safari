# -*- coding: utf-8 -*-

import os
import sqlite3
from typing import Dict, Iterable

from safari.resource import DEFAULT_LIBRARY_PATH, SafariResource


class SafariHistories(SafariResource):
    def __init__(self, library: str = DEFAULT_LIBRARY_PATH):
        super().__init__(library=library)
        self.history_file = os.path.join(self.library, "History.db")

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
