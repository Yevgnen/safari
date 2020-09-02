# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name="safari",
    description="Python utilities for Safari.",
    version="1.1.0",
    url="https://github.com/Yevgnen/safari",
    author="Yevgnen Koh",
    author_email="wherejoystarts@gmail.com",
    packages=find_packages(),
    entry_points={"console_scripts": ["safari_export=safari.safari_export:main"]},
    include_package_data=True,
    install_requires=[],
    zip_safe=False,
)
