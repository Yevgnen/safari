# -*- coding: utf-8 -*-

import abc
import datetime

from safari.resource import URLItem


class Formater(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def format(self, url_item: URLItem) -> str:
        raise NotImplementedError()


class OrgFormater(Formater):
    def __init__(
        self, capture_template: str = "* [[{{url}}][{{title}}]]\n[{{timestamp}}]"
    ):
        self.capture_template = capture_template

    def format(self, url_item: URLItem) -> str:
        return self.capture_template.format(
            url=url_item["url"],
            title=url_item["title"],
            timestamp=datetime.datetime.now().strftime("%Y-%m-%d %a %H:%M"),
        )
