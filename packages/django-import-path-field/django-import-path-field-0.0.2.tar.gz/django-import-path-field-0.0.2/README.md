[![PyPi](https://img.shields.io/pypi/v/django-import-path-field.svg)](https://pypi.python.org/pypi/django-import-path-field)
[![Build Status](https://travis-ci.org/Apkawa/django-import-path-field.svg?branch=master)](https://travis-ci.org/Apkawa/django-import-path-field)
[![codecov](https://codecov.io/gh/Apkawa/django-import-path-field/branch/master/graph/badge.svg)](https://codecov.io/gh/Apkawa/django-import-path-field)
[![Requirements Status](https://requires.io/github/Apkawa/django-import-path-field/requirements.svg?branch=master)](https://requires.io/github/Apkawa/django-import-path-field/requirements/?branch=master)
[![PyUP](https://pyup.io/repos/github/Apkawa/django-import-path-field/shield.svg)](https://pyup.io/repos/github/Apkawa/django-import-path-field)
[![PyPI](https://img.shields.io/pypi/pyversions/django-import-path-field.svg)](https://pypi.python.org/pypi/django-import-path-field)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)


# Installation

```bash
pip install django-import-path-field

```

or from git

```bash
pip install -e git+https://githib.com/Apkawa/django-import-path-field.git#egg=django-import-path-field
```

## Django and python version

| Python<br/>Django | 3.5 | 3.6 | 3.7 | 3.8 |
|:-----------------:|-----|-----|-----|-----|
| 1.8               |  ✘  |  ✘  |  ✘  |  ✘  |
| 1.11              |  ✔  |  ✔  |  ✔  |  ✘  |
| 2.2               |  ✔  |  ✔  |  ✔  |  ✔  |
| 3.0               |  ✘  |  ✔  |  ✔  |  ✔  |


# Usage
models.py
```python

from django.db import models
from importpath_field import ImportPathField, ImportPathChoices


class DescriptionClassStrategy:
    # Description for class
    short_description = 'Strategy description'

    @classmethod
    def class_method(cls):
        return 1

    @classmethod
    def class_method_description(cls):
        """Class method description"""
        return 1

    def method(self):
        return 3


def example_function_description():
    return 1

# Can description for choice
example_function_description.short_description = 'Function description'


IMPORT_CHOICES = ImportPathChoices(
    DescriptionClassStrategy, 
    example_function_description,
)

# Also may add to choice 
@IMPORT_CHOICES.register("Example description")
def example_function():
    return 1


class ExampleModel(models.Model):
    example_class = ImportPathField()
    example_class_choices = ImportPathField(choices=IMPORT_CHOICES)
    example_class_null = ImportPathField(null=True, blank=True)

```

```python
```


# Contributing

## run example app

```bash
pip install -r requirements-dev.txt
./test/manage.py migrate
./test/manage.py runserver
```

## run tests

```bash
pip install -r requirements-dev.txt
pytest
tox
```

## Update version

```bash
python setup.py bumpversion
```

## publish pypi

```bash
python setup.py publish
```






