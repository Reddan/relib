from setuptools import setup

setup(
  name='relib',
  packages=['relib'],
  version='0.1.1',
  author='Hampus Hallman',
  author_email='me@hampushallman.com',
  url='https://github.com/Reddan/relib',
  license='MIT',
  install_requires=[
    'termcolor',
    'numpy',
    'sklearn',
  ],
  python_requires='~=3.5',
)
