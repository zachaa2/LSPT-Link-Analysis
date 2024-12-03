# setup.py
from setuptools import setup, find_packages

setup(
    name='webgraph',  # package name
    version='0.1',    # version
    packages=find_packages(where='src'),  # package location: 'src'
    package_dir={'': 'src'},
)
