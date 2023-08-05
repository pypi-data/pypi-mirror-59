#!/usr/bin/env python3

from setuptools import setup, find_packages

readme = open('README.rst').read()

with open('njactb.py') as f:
    for line in f:
        if line.startswith('__version__ = '):
            version = eval(line.strip().split(' = ')[-1])
            break

if version is None:
    raise Exception("version not found")

setup(
    name='njactb',
    version=version,
    description='Python wrapper for njactb.',
    long_description=readme,
    author='Al Johri',
    author_email='al.johri@gmail.com',
    url='https://github.com/AlJohri/njactb',
    license='MIT',
    py_modules=['njactb'],
    install_requires=['requests', 'cssselect', 'lxml', 'usaddress'],
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
    ]
)
