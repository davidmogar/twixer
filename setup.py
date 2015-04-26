#!/user/bin/env python

from setuptools import setup, find_packages

setup(name='twixer',
      version='0.1',
      description='Simple Twitter gender recognition tool',
      author='David Moreno García',
      author_email='david.mogar@gmail.com',
      license='MIT',
      url='https://github.com/davidmogar/twixer',
      packages=find_packages(exclude=['tests'])
      )
