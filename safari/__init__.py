# -*- coding: utf-8 -*-

import os
from typing import Dict, Iterable, List, Union

from safari import bookmark, cloudtab, commands, exporter, formater
from safari.bookmark import SafariBookmarks, URLItem
from safari.cloudtab import SafariCloudTabs


class Safari(object):
    def __init__(
        self, library: str = os.path.join(os.environ["HOME"], "Library", "Safari")
    ):
        self.cloudtab = SafariCloudTabs(library=library)
        self.bookmark = SafariBookmarks(library=library)

    def get_cloud_tabs(self) -> Iterable[URLItem]:
        return self.cloudtab.get_cloud_tabs()

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
    "cloudtab",
]
