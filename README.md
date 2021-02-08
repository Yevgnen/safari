# Table of Contents <span class="tag" tag-name="TOC"><span class="smallcaps">TOC</span></span>

-   [Introduction](#introduction)
-   [Installation](#installation)
    -   [From pip](#from-pip)
    -   [From source](#from-source)
-   [Usages](#usages)
    -   [Exporting reading list/cloud tabs](#exporting-reading-listcloud-tabs)
    -   [Using the `safari` script](#using-the-safari-script)
-   [Contribution](#contribution)
    -   [Formatting Code](#formatting-code)

# Introduction

`safari` is a Python library for manipulating Safari data.

# Installation

## From pip

``` bash
pip install safari
```

## From source

``` bash
pip install git+https://github.com/Yevgnen/safari.git
```

# Usages

## Exporting reading list/cloud tabs

``` Python
# -*- coding: utf-8 -*-

from safari import Safari

safari = Safari()

print(safari.export(kind="cloud_tabs"))
print(safari.export(kind="readings"))
print(safari.export(kind="bookmarks"))
print(safari.export(kind="all"))
```

## Using the `safari` script

``` bash
safari export -s all -t output.yaml
```

# Contribution

## Formatting Code

To ensure the codebase complies with a style guide, please use [flake8](https://github.com/PyCQA/flake8), [black](https://github.com/psf/black) and [isort](https://github.com/PyCQA/isort) tools to format and check codebase for compliance with PEP8.
