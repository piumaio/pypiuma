PyPiuma
=======

|Latest Version| |CI| |codecov| |License: MIT|

A library to use Piuma with Python and Django

Install
-------

::

   pip install pypiuma

Usage
-----

.. code:: py

   from pypiuma import piuma_url

   piuma_url("http://mypiumahost", "http://myimagehost/static/img/a.png", 200, 200, 80)

Usage with Django
-----------------

.. code:: html

   {% load pypiuma_tags %}

   <img src="{% piuma 'http://myimagehost/static/img/a.png' width=200 convert_to="auto" %}">
   <img src="{% piuma_static 'img/mylogo.png' width=200 %}">

Picture tags
------------

.. code:: html

   {% load pypiuma_tags %}

   {% piuma_picture 'http://myimagehost/static/img/a.png'%}
   {% piuma_picture_static 'img/a.png' %}

Settings
--------

PIUMA_DISABLED
~~~~~~~~~~~~~~

Disable Piuma core, useful in development.

Default: ``False``

PIUMA_HOST
~~~~~~~~~~

The host of your Piuma instance.

Default: ``/piuma/``

PIUMA_MEDIA_RULES
~~~~~~~~~~~~~~~~~

Media rules for picture tags.

Default:
``(max-width: 576px),(max-width: 768px),(max-width: 992px),(max-width: 1366px)``

PIUMA_SIZES
-----------

Fast configurations for your images. These can be handy if you want to
define different sizes like ``small``, ``medium``, ``full`` to serve the
best optimized version of the image for your needs. The ``*`` size, if
defined, is applied to all images imported with a tag that do not
specify a size.

Default: ``{}``

Example:

.. code:: python

   {
     "*": {
       "convert_to": "auto",
       "quality": 80
     },
     "small": {
       "width": 300,
       "convert_to": "auto",
       "quality": 80
     },
     "medium": {
       "width": 500,
       "convert_to": "auto",
       "quality": 80
     },
     "large": {
       "width": 1000,
       "convert_to": "auto",
       "quality": 80
     }
   }

Run tests
---------

::

   pip install -r requirements-dev.txt
   make test

.. |Latest Version| image:: https://img.shields.io/pypi/v/pypiuma.svg
   :target: https://pypi.python.org/pypi/pypiuma/
.. |CI| image:: https://github.com/piumaio/pypiuma/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/piumaio/pypiuma
.. |codecov| image:: https://codecov.io/gh/piumaio/pypiuma/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/piumaio/pypiuma
.. |License: MIT| image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://github.com/piumaio/pypiuma/blob/master/LICENSE
