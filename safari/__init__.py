# -*- coding: utf-8 -*-

import os
import sqlite3
from typing import Dict, Iterable, List, Union

from safari import bookmark, commands, exporter, formater
from safari.bookmark import SafariBookmarks, URLItem


class Safari(object):
    def __init__(
        self, library: str = os.path.join(os.environ["HOME"], "Library", "Safari")
    ):
        self.bookmark = SafariBookmarks(library=library)
        self.cloud_tab_file = os.path.join(library, "CloudTabs.db")

    def get_devices(self) -> Iterable[Dict[str, str]]:
        with sqlite3.connect(self.cloud_tab_file) as conn:
            sql = "select device_uuid, device_name from cloud_tab_devices;"

            for id_, name in conn.cursor().execute(sql):
                yield {
                    "id": id_,
                    "name": name,
                }

    def get_device_cloud_tabs(self, device_id: str) -> Iterable[URLItem]:
        with sqlite3.connect(self.cloud_tab_file) as conn:
            sql = f'select title, url from cloud_tabs where device_uuid="{device_id}";'
            for tab in conn.cursor().execute(sql):
                yield {
                    "title": tab[0],
                    "url": tab[1],
                }

    def get_cloud_tabs(self) -> Iterable[URLItem]:
        for device in self.get_devices():
            yield {**device, "tabs": list(self.get_device_cloud_tabs(device["id"]))}

    def get_readings(self) -> Iterable[URLItem]:
        return self.bookmark.get_readings()

    def get_bookmarks(self, flatten: bool = True) -> Union[Iterable[URLItem], Dict]:
        return self.bookmark.get_bookmarks(flatten=flatten)

    def export(self, kind: str = "all") -> Dict[str, List]:
        factory = {
            "cloud_tabs": self.get_cloud_tabs,
            "readings": self.get_readings,
            "bookmarks": self.get_bookmarks,
        }
        if kind != "all":
            factory = {kind: factory[kind]}

        return {k: list(v()) for k, v in factory.items()}


__all__ = [
    "Safari",
    "exporter",
    "formater",
    "commands",
    "bookmark",
]
