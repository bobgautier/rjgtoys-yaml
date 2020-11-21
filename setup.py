#!/usr/bin/python3

try:
    from rjgtoys.projects import setup
except ImportError:
    from setuptools import setup

setup(
    name = "rjgtoys-yaml",
    version = "0.0.1",
    author = "Robert J. Gautier",
    author_email = "bob.gautier@gmail.com",
    url = "https://github.com/bobgautier/rjgtoys-Yaml",
    description = ("Reading and writing YAML"),
    namespace_packages=['rjgtoys'],
    packages = ['rjgtoys','rjgtoys.yaml'],
    install_requires = [
      'rjgtoys-thing',
      'rjgtoys-xc',
      'ruamel.yaml',
    ],
    extras_require = {
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
