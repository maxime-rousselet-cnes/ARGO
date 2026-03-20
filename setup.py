"""
To install via pip install -e . in the root of the repository. This will make the package available
in the current environment.
"""

from setuptools import find_packages, setup

setup(
    name="argo",
    packages=find_packages(),
    version="0.0.1",
    description="To download and process ARGO profile files from NOAA.",
    author="Maxime Rousselet",
)
