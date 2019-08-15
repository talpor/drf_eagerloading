#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = []

setup_requirements = ["pytest-runner", "Django>=2.0", "djangorestframework>=3.9"]

test_requirements = ["pytest"]

setup(
    author="Pedro Piñango",
    author_email="ppinango@talpor.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="Calculate prefetch_related and select_related recursively based on the definition on the serializers.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="drf_eagerloading",
    name="drf_eagerloading",
    packages=find_packages(include=["drf_eagerloading"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/talpor/drf_eagerloading",
    version="0.0.2",
    zip_safe=False,
    python_requires=">=3.6",
)
