# -*- coding: utf-8 -*-

import os
import plistlib
import sqlite3


class Safari(object):
    def __init__(self, library=os.path.join(os.environ["HOME"], "Library/Safari/")):
        self.bookmark_file = os.path.join(library, "Bookmarks.plist")
        self.db_file = os.path.join(library, "CloudTabs.db")

    @property
    def readings(self):
        with open(self.bookmark_file, mode="rb") as plist_file:
            plist = plistlib.load(plist_file)

        bookmarks = None
        for child in plist["Children"]:
            if child.get("Title", None) == "com.apple.ReadingList":
                bookmarks = child
                break

        if not bookmarks:
            return

        for bookmark in bookmarks["Children"]:
            yield {
                "title": bookmark["URIDictionary"]["title"],
                "url": bookmark["URLString"],
            }

    @property
    def bookmarks(self):
        with sqlite3.connect(self.db_file) as conn:
            c = conn.cursor()

            sql_iphone_device = (
                'select device_uuid from cloud_tab_devices where device_name="iPhone";'
            )
            iphone_id = next((x[0] for x in c.execute(sql_iphone_device)), None,)
            if not iphone_id:
                raise RuntimeError("iPhone device_id not found")

            sql_links = (
                f'select title, url from cloud_tabs where device_uuid="{iphone_id}";'
            )
            tabs = c.execute(sql_links)

            for tab in tabs:
                yield {
                    "title": tab[0],
                    "url": tab[1],
                }
