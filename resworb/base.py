# -*- coding: utf-8 -*-

from typing import Dict, Iterable, Union

URLItem = Dict[str, str]


class OpenedTabMixin(object):
    def get_opened_tabs(self) -> Iterable[URLItem]:
        raise NotImplementedError()


class CloudTabMixin(object):
    def get_cloud_tabs(self) -> Iterable[URLItem]:
        raise NotImplementedError()


class ReadingMixin(object):
    def get_readings(self) -> Iterable[URLItem]:
        raise NotImplementedError()


class BookmarkMixin(object):
    def get_bookmarks(self, flatten: bool = True) -> Union[Iterable[URLItem], Dict]:
        raise NotImplementedError()


class HistoryMixin(object):
    def get_histories(self) -> Iterable[Dict]:
        raise NotImplementedError()
