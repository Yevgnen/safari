# -*- coding: utf-8 -*-

from typing import Dict, Iterable, List, Union

from safari import bookmark, cloudtab, commands, exporter, formater, history, resource
from safari.bookmark import SafariBookmarks
from safari.cloudtab import SafariCloudTabs
from safari.history import SafariHistories
from safari.resource import URLItem


class Safari(object):
    def __init__(self, library: str = resource.DEFAULT_LIBRARY_PATH):
        self.cloudtab = SafariCloudTabs(library=library)
        self.bookmark = SafariBookmarks(library=library)
        self.history = SafariHistories(library=library)

    def get_cloud_tabs(self) -> Iterable[URLItem]:
        return self.cloudtab.get_cloud_tabs()

    def get_readings(self) -> Iterable[URLItem]:
        return self.bookmark.get_readings()

    def get_bookmarks(self, flatten: bool = True) -> Union[Iterable[URLItem], Dict]:
        return self.bookmark.get_bookmarks(flatten=flatten)

    def get_histories(self) -> Iterable[Dict]:
        return self.history.get_histories()

    def export(self, kind: str = "all") -> Dict[str, List]:
        factory = {
            "cloud_tabs": self.get_cloud_tabs,
            "readings": self.get_readings,
            "bookmarks": self.get_bookmarks,
            "histories": self.get_histories,
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
    "cloudtab",
    "history",
    "resource",
]
