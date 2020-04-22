#!/usr/bin/env python3

from setuptools import setup, find_packages


setup(
    name="recsystem",
    version='0.0.0',
    author='Jan Seifert',
    author_email="jan.seifert@fotkyzcest.net",
    description="Simple recommendation system based on Shelter",
    packages=find_packages(include=['recsystem*']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'cached-property',
        'feedparser',
        'mako',
        'shelter',
    ],
    entry_points={
        'console_scripts': [
            'manage-recsystem = recsystem:main',
        ]
    },
)
