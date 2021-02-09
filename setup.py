# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name="resworb",
    description="Manage browser data in Python.",
    version="1.2.0",
    url="https://github.com/Yevgnen/resworb",
    author="Yevgnen Koh",
    author_email="wherejoystarts@gmail.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "safari=resworb.commands.safari_main:main",
            "safari-export=resworb.commands.safari_export:main",
        ],
    },
    include_package_data=True,
    install_requires=[
        "lz4",
        "pyyaml",
        "pytoml",
    ],
    zip_safe=False,
)
