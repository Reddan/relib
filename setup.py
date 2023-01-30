from setuptools import setup

setup(
  name='relib',
  packages=['relib'],
  version='0.2.1',
  author='Hampus Hallman',
  author_email='me@hampushallman.com',
  url='https://github.com/Reddan/relib',
  license='MIT',
  install_requires=[
    'termcolor',
    'numpy',
  ],
  python_requires='~=3.10',
)
