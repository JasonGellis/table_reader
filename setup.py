"""
Setup script for the Table Reader application.

This script uses setuptools to package the Table Reader Python application,
making it easy to install and use as a command-line tool. The script defines
metadata about the package, its dependencies, and the entry point for the CLI.

To install the package, run:

    pip install .

After installation, you can use the 'tablereader' command from the terminal to
run the application.
"""

from setuptools import setup, find_packages

with open("requirements.txt", "r", encoding="utf-8") as f:
    REQUIRED_PACKAGES = f.read().splitlines()

setup(
    name="table_reader",
    version="1.0.0",
    description="A Python app for extracting data from images",
    download_url="https://github.com/JasonGellis/table_reader",
    author="Jason Jacob Gellis",
    author_email="jg760@cam.ac.uk",
    license="MIT",
    keywords=[
        'data extraction', 'data analysis',
        'optical character recognition', 'computer vision'
    ],
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tablereader=app:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
