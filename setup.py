#!/user/bin/env python

import re

from setuptools import setup, find_packages

version = re.search(
    '^__version__\s*=\s*\'(.*)\'',
    open('bootstrap/bootstrap.py').read(),
    re.M).group(1)

with open("README.md", "rb") as f:
    long_description = f.read().decode("utf-8")

setup(name='twixer',
      version=version,
      description='Simple Twitter gender recognition tool',
      long_description=long_description,
      author='David Moreno-Garcia',
      author_email='david.mogar@gmail.com',
      license='MIT',
      url='https://github.com/davidmogar/twixer',
      packages=find_packages(exclude=['tests']),
      entry_points={'console_scripts': ['twixer = twixer.twixer:main']}
      )
