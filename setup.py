from setuptools import setup

setup(
  name='relib',
  version='0.1',
  packages=['relib'],
  install_requires=[
    'numpy',
    'bcolz',
    'pyodbc',
    'pymongo',
    'termcolor'
  ],
  zip_safe=False
)
