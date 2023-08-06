#!/usr/bin/env python3

import sys
from setuptools import find_packages, setup  # type: ignore

if sys.version_info < (3, 6, 0):
    sys.exit(
        "Python 3.6 or later is required. "
        "See https://github.com/pipxproject/pipx "
        "for installation instructions."
    )

import io  # noqa E402
import os  # noqa E402
from pathlib import Path  # noqa E402
from typing import List  # noqa E402
import ast  # noqa E402
import re  # noqa E402

CURDIR = Path(__file__).parent

REQUIRED = ["userpath", "argcomplete>=1.9.4, <2.0"]  # type: List[str]

with io.open(os.path.join(CURDIR, "README.md"), "r", encoding="utf-8") as f:
    README = f.read()


def get_version():
    main_file = CURDIR / "src" / "pipx" / "main.py"
    _version_re = re.compile(r"__version__\s+=\s+(?P<version>.*)")
    with open(main_file, "r", encoding="utf8") as f:
        match = _version_re.search(f.read())
        version = match.group("version") if match is not None else '"unknown"'
    return str(ast.literal_eval(version))


setup(
    name="pipx",
    version=get_version(),
    author="Chad Smith",
    author_email="grassfedcode@gmail.com",
    description="Install and Run Python Applications in Isolated Environments",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/pipxproject/pipx",
    license="License :: OSI Approved :: MIT License",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    keywords=["pip", "install", "cli", "workflow", "Virtual Environment"],
    scripts=[],
    entry_points={"console_scripts": ["pipx = pipx.main:cli"]},
    zip_safe=False,
    install_requires=REQUIRED,
    test_suite="tests.test_pipx",
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
    project_urls={
        "Documentation": "https://pipxproject.github.io/pipx/",
        "Source Code": "https://github.com/pipxproject/pipx",
        "Bug Tracker": "https://github.com/pipxproject/pipx/issues",
    },
)
