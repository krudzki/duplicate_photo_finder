#!/usr/bin/env python3
"""
Setup script for Duplicate Photo Finder
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='duplicate-photo-finder',
    version='1.0.0',
    author='Krzysztof Rudzki',
    author_email='krudzki.dev@gmail.com',
    description='A powerful tool to find and manage duplicate photos and videos',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/krudzki/duplicate_photo_finder',
    py_modules=['duplicate_finder'],
    python_requires='>=3.8',
    install_requires=[
        'Pillow>=10.0.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Graphics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    keywords='photos videos duplicates cleanup management',
    project_urls={
        'Bug Reports': 'https://github.com/krudzki/duplicate_photo_finder/issues',
        'Source': 'https://github.com/krudzki/duplicate_photo_finder',
    },
)
