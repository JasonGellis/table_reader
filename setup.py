""" App setup file. """

from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    REQUIRED_PACKAGES = f.read().splitlines()

setup(
    name="Table Reader",
    version="1.0",
    description="A python app for extracting data from images",
    download_url="https://github.com/JasonGellis/table_reader",
    author="Jason Jacob Gellis",
    author_email="jg760@cam.ac.uk",
    license="MIT",
    keywords=['data extraction', 'data analysis', \
        'optical character recognition', 'computer vision'],
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
)
