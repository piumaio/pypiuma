from django.test import RequestFactory

from pypiuma import piuma_url
from pypiuma.templatetags.pypiuma_tags import piuma, piuma_static, piuma_picture, piuma_picture_static


def test_piuma_url(settings, client):
    piumaurl = piuma_url('http://mypiumahost', 'http://myhost/static/img/a.png', 200, 200, 80)
    assert piumaurl == 'http://mypiumahost/200_200_80/http://myhost/static/img/a.png'
    piumaurl = piuma_url('http://mypiumahost', '/static/img/a.png', 200, 200, 80)
    assert piumaurl == 'http://mypiumahost/200_200_80//static/img/a.png'


def test_piuma_tag_without_request(settings, client):
    context = {}
    piumaurl = piuma(context, 'img/a.png')
    assert piumaurl == '/piuma/0_0_100//img/a.png'
    settings.PIUMA_DISABLED = True
    piumaurl = piuma(context, 'img/a.png')
    assert piumaurl == 'img/a.png'


def test_piuma_tag(settings, client):
    context = {
        'request' : RequestFactory(HTTP_HOST='localhost:8000').get('/')
    }
    piumaurl = piuma(context, 'img/a.png')
    assert piumaurl == '/piuma/0_0_100/http://localhost:8000/img/a.png'
    settings.PIUMA_DISABLED = True
    piumaurl = piuma(context, 'img/a.png')
    assert piumaurl == 'img/a.png'


def test_static_piuma_tag(settings, client):
    context = {
        'request' : RequestFactory(HTTP_HOST='localhost:8000').get('/')
    }
    piumaurl = piuma_static(context, 'img/a.png')
    assert piumaurl == '/piuma/0_0_100/http://localhost:8000/static/img/a.png'
    settings.PIUMA_DISABLED = True
    piumaurl = piuma_static(context, 'img/a.png')
    assert piumaurl == '/static/img/a.png'


def test_piuma_picture(settings, client):
    context = {
        'request' : RequestFactory(HTTP_HOST='localhost:8000').get('/')
    }
    print (
        piuma_picture(
            context,
            "http://localhost:8000/img/a.png",
            "(max-width: 576px),(max-width: 768px)"
        )
    )

    print (
        piuma_picture(
            context,
            "http://localhost:8000/img/a.png"
        )
    )

    print (
        piuma_picture_static(
            context,
            "img/a.png"
        )
    )
