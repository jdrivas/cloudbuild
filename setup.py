from setuptools import setup

setup(
  name='cloudbuild',
  version='0.0.2',
  py_modules=['cloudbuild'],
  install_requires=[
    'click',
  ],
  entry_points='''
  [console_scripts]
  cloudbuild=cloudbuild:cli
  ''',
)