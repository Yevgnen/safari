# -*- coding: utf-8 -*-

from resworb.browsers.safari import Safari

safari = Safari()

print(safari.export(kind="cloud_tabs"))
print(safari.export(kind="readings"))
print(safari.export(kind="bookmarks"))
print(safari.export(kind="histories"))
print(safari.export(kind="all"))
