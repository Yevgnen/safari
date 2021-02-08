# -*- coding: utf-8 -*-

from safari import Safari

safari = Safari()

print(safari.export(kind="cloud_tabs"))
print(safari.export(kind="readings"))
print(safari.export(kind="bookmarks"))
print(safari.export(kind="all"))
