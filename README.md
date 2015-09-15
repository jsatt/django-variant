Django Variant
=====================

Variant is an AB/variant/split testing framework for Django which allows for easy setup and flexible goal tracking. Variant provides an optional basic goal tacking system for reviewing results, but also allows for simple use of Google Analytics custom variables, custom ad channels or most other reporting system you choose.

[![Build Status](https://travis-ci.org/jsatt/django-variant.svg?branch=master)](https://travis-ci.org/jsatt/django-variant)
[![Coverage Status](https://coveralls.io/repos/jsatt/django-variant/badge.png?branch=master)](https://coveralls.io/r/jsatt/django-variant?branch=master)

Installing
----------

    pip install django-variant

Using Variant
-------------


Developing
----------
Install requirements

    pip install -r requirements.txt

Setup db

    fab syncdb
    fab migrate

Start server

    fab serve

Using the Python shell

    fab shell

Running tests

    fab test

Creating South schema migrations

    fab schema
    fab migrate

All pull requests should pass pep8 and pyflakes validation and have 100% test coverage and be developed in a separate feature branch.


License
-------

Django Variant
Copyright (C) Jeremy Satterfield and individual contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
