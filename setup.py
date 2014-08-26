#!/usr/bin/env python

from setuptools import setup

setup(
    name='django-variant',
    version='0.0.1',
    description='Django variant testing framework',
    author='Jeremy Sattefield',
    author_email='jsatt22@gmail.com',
    url='https://github.com/jsatt/django-variant',
    #license='',
    packages=[
        'variant', 'variant.migrations'],
    install_requires=[
        'Django>=1.5'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Site Management'],
)
