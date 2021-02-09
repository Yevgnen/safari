# Table of Contents <span class="tag" tag-name="TOC"><span class="smallcaps">TOC</span></span>

-   [Introduction](#introduction)
-   [Installation](#installation)
    -   [From pip](#from-pip)
    -   [From source](#from-source)
-   [Usages](#usages)
    -   [Exporting user data (reading list, cloud tabs, bookmarks, histories)](#exporting-user-data-reading-list-cloud-tabs-bookmarks-histories)
    -   [Using scripts](#using-scripts)
-   [Contribution](#contribution)
    -   [Formatting Code](#formatting-code)
-   [References](#references)

# Introduction

`resworb` is a Python library for manipulating browser data.

# Installation

## From pip

``` bash
pip install resworb
```

## From source

``` bash
pip install git+https://github.com/Yevgnen/resworb.git
```

# Usages

## Exporting user data (reading list, cloud tabs, bookmarks, histories)

``` Python
# -*- coding: utf-8 -*-

from resworb.browsers.safari import Safari

safari = Safari()

print(safari.export(kind="cloud_tabs"))
print(safari.export(kind="readings"))
print(safari.export(kind="bookmarks"))
print(safari.export(kind="histories"))
print(safari.export(kind="all"))
```

## Using scripts

``` bash
safari export -s all -t output.yaml
```

# Contribution

## Formatting Code

To ensure the codebase complies with a style guide, please use [flake8](https://github.com/PyCQA/flake8), [black](https://github.com/psf/black) and [isort](https://github.com/PyCQA/isort) tools to format and check codebase for compliance with PEP8.

# References

-   [GitHub - kcp18/browserhistory: A simple Python module that extracts browser history](https://github.com/kcp18/browserhistory)
-   [Parse Safari Reading List using Python · GitHub](https://gist.github.com/ghutchis/f7362256064e3ad82aaf583511fca503)
-   [helper/SafariBookmarkEditor at master · jedetaste/helper · GitHub](https://github.com/jedetaste/helper/blob/master/bin/SafariBookmarkEditor)
