pypiuma
=======

A library to use Piuma with Python and Django

Install
-------

::

    pip install pypiuma

Usage
-----

::

    from pypiuma import piuma_url

    piuma_url("http://mypiumahost", "http://myimagehost/static/img/a.png", 200, 200, 80)

Usage with Django
-----------------

::

    {% load pypiuma_tags %}

    <img src="{% piuma 'http://myimagehost/static/img/a.png' width=200 %}">
    <img src="{% piuma_static 'img/mylogo.png' width=200 %}">

Run tests
---------

::

    pip install -r requirements-dev.txt
    make test
