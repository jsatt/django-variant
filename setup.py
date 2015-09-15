#!/usr/bin/env python

from setuptools import setup

setup(
    name='django-variant',
    version='0.1.1',
    description='Django variant testing framework',
    author='Jeremy Sattefield',
    author_email='jsatt@jsatt.com',
    url='https://github.com/jsatt/django-variant',
    packages=[
        'variant', 'variant.migrations'],
    install_requires=[
        'Django>=1.5', 'six'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Site Management'],
)
