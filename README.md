# PyPiuma

[![Latest Version](https://img.shields.io/pypi/v/pypiuma.svg)](https://pypi.python.org/pypi/pypiuma/)
[![codecov](https://codecov.io/gh/piumaio/pypiuma/branch/master/graph/badge.svg)](https://codecov.io/gh/piumaio/pypiuma)
[![Build Status](https://travis-ci.org/piumaio/pypiuma.svg?branch=master)](https://travis-ci.org/piumaio/pypiuma)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/piumaio/pypiuma/blob/master/LICENSE)

A library to use Piuma with Python and Django

## Install

    pip install pypiuma

## Usage

    from pypiuma import piuma_url

    piuma_url("http://mypiumahost", "http://myimagehost/static/img/a.png", 200, 200, 80)

## Usage with Django

    {% load pypiuma_tags %}

    <img src="{% piuma 'http://myimagehost/static/img/a.png' width=200 %}">
    <img src="{% piuma_static 'img/mylogo.png' width=200 %}">

## Picture tags

    {% load pypiuma_tags %}

    {% piuma_picture 'http://myimagehost/static/img/a.png'%}
    {% piuma_picture_static 'img/a.png' width=200 %}

## Settings

### PIUMA_DISABLED

Disable Piuma core, useful in development.

Default: `False`

### PIUMA_HOST

The host of your Piuma instance.

Default:  `/piuma/`

### PIUMA_MEDIA_RULES

Media rules for picture tags.

Default: `(max-width: 576px),(max-width: 768px),(max-width: 992px),(max-width: 1366px)`

## Run tests

    pip install -r requirements-dev.txt
    make test
