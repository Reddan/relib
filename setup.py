from setuptools import setup

setup(
  name='relib',
  packages=['relib'],
  version='0.1',
  author='Hampus Hallman',
  install_requires=[
    'numpy',
    'bcolz',
    'termcolor'
  ],
  zip_safe=False,
  url='https://github.com/Reddan/relib',
)
