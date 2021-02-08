# -*- coding: utf-8 -*-

import abc
import json
from typing import Any, Mapping, Optional

import pytoml
import yaml


class Exporter(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def export_to_file(
        self,
        data: Any,
        filename: str,
        file_kwargs: Optional[Mapping] = None,
        dump_kwargs: Optional[Mapping] = None,
    ) -> None:
        raise NotImplementedError()


class YAMLExporter(Exporter):
    def export_to_file(
        self,
        data: Any,
        filename: str,
        file_kwargs: Optional[Mapping] = None,
        dump_kwargs: Optional[Mapping] = None,
    ) -> None:
        if not file_kwargs:
            file_kwargs = {"mode": "w"}

        if not dump_kwargs:
            dump_kwargs = {
                "allow_unicode": True,
                "explicit_start": True,
                "indent": 2,
            }

        with open(filename, **file_kwargs) as f:
            yaml.safe_dump(data, f, **dump_kwargs)


class TOMLExporter(Exporter):
    def export_to_file(
        self,
        data: Any,
        filename: str,
        file_kwargs: Optional[Mapping] = None,
        dump_kwargs: Optional[Mapping] = None,
    ) -> None:
        if not file_kwargs:
            file_kwargs = {"mode": "w"}

        if not dump_kwargs:
            dump_kwargs = {}

        with open(filename, **file_kwargs) as f:
            pytoml.dump(data, f, **dump_kwargs)


class JSONExporter(Exporter):
    def export_to_file(
        self,
        data: Any,
        filename: str,
        file_kwargs: Optional[Mapping] = None,
        dump_kwargs: Optional[Mapping] = None,
    ) -> None:
        if not file_kwargs:
            file_kwargs = {"mode": "w"}

        if not dump_kwargs:
            dump_kwargs = {
                "ensure_ascii": False,
                "indent": 4,
            }

        with open(filename, **file_kwargs) as f:
            json.dump(data, f, **dump_kwargs)
