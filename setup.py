from setuptools import setup

setup(
  name='relib',
  version='0.1',
  packages=['relib'],
  install_requires=[
    'pymssql',
    'pymongo',
    'termcolor'
  ],
  zip_safe=False
)
