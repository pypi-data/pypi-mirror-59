#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

install_requires = \
['docopt >=0.6.2', 'stomp.py >=4.1.22', 'xmltodict >=0.12.0']

setup(name='bmrs',
      version='1.2.81',
      description='This package enables you receive BMRS data as json instead of the default XML',
      author='Edison Abahurire',
      author_email='abahedison@gmail.com',
      url='https://github.com/SimiCode/bmrs-json-api',
      py_modules=['bmrs'],
      install_requires=install_requires,
      python_requires='>=3.6',
     )
