# -*- coding: utf-8 -*-

import os

DEFAULT_LIBRARY_PATH = os.path.join(os.environ["HOME"], "Library", "Safari")


class SafariResource(object):
    def __init__(self, library: str = DEFAULT_LIBRARY_PATH):
        self.library = library
