import os
import logging
import sys
from setuptools import setup

def read(fname):
    '''Utility function to read the README file.'''
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# figure out what the install will need
install_requires = ["setuptools >=0.5"]

setup(
    name = "xvfb",
    version = "1.0.0",
    author = "Graff Haley and Jonathan Ultis",
    author_email = "graffh@zillow.com, jonathanu@zillow.com",
    description = "Start and stop Xvfb as a subprocess reliably",
    license = "(C) Zillow, Inc. 2012-",
    keywords = "zillow",
    url = "http://zwiki.zillow.local/",
    packages = ['xvfb'],
    long_description = read('README.md'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires = install_requires,
    )
