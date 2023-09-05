from setuptools import setup

setup(
  name='relib',
  packages=['relib'],
  version='1.0.3',
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
