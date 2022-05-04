import re
from django.test import RequestFactory

from pypiuma import piuma_url
from pypiuma.templatetags.pypiuma_tags import (
    piuma,
    piuma_img,
    piuma_img_static,
    piuma_static,
    piuma_picture,
    piuma_picture_static,
)


def test_piuma_url(settings, client):
    piumaurl = piuma_url(
        "http://mypiumahost", "http://myhost/static/img/a.png", 200, 200, 80
    )
    assert piumaurl == "http://mypiumahost/200_200_80/http://myhost/static/img/a.png"
    piumaurl = piuma_url("http://mypiumahost", "/static/img/a.png", 200, 200, 80)
    assert piumaurl == "http://mypiumahost/200_200_80//static/img/a.png"
    piumaurl = piuma_url(
        "http://mypiumahost", "/static/img/a.png", 200, 200, 80, adaptive_quality=True
    )
    assert piumaurl == "http://mypiumahost/200_200_80a//static/img/a.png"
    piumaurl = piuma_url(
        "http://mypiumahost",
        "/static/img/a.png",
        200,
        200,
        80,
        adaptive_quality=True,
        convert_to="auto",
    )
    assert piumaurl == "http://mypiumahost/200_200_80a:auto//static/img/a.png"


def test_piuma_tag_without_request(settings, client):
    context = {}
    piumaurl = piuma(context, "img/a.png")
    assert piumaurl == "/piuma/0_0_100//img/a.png"
    settings.PIUMA_DISABLED = True
    piumaurl = piuma(context, "img/a.png")
    assert piumaurl == "img/a.png"


def test_piuma_tag(settings, client):
    context = {"request": RequestFactory(HTTP_HOST="localhost:8000").get("/")}
    piumaurl = piuma(context, "img/a.png")
    assert piumaurl == "/piuma/0_0_100/http://localhost:8000/img/a.png"
    settings.PIUMA_DISABLED = True
    piumaurl = piuma(context, "img/a.png")
    assert piumaurl == "img/a.png"


def test_static_piuma_tag(settings, client):
    context = {"request": RequestFactory(HTTP_HOST="localhost:8000").get("/")}
    piumaurl = piuma_static(context, "img/a.png")
    assert piumaurl == "/piuma/0_0_100/http://localhost:8000/static/img/a.png"
    settings.PIUMA_DISABLED = True
    piumaurl = piuma_static(context, "img/a.png")
    assert piumaurl == "/static/img/a.png"


def test_piuma_picture(settings, client):
    context = {"request": RequestFactory(HTTP_HOST="localhost:8000").get("/")}
    piuma_picture(
        context,
        "http://localhost:8000/img/a.png",
        "(max-width: 576px),(max-width: 768px)",
    )

    test_picture = piuma_picture(
        context,
        "http://localhost:8000/img/a.png",
        width=500,
        image_width=1000,
        image_height=600,
    )
    assert re.search(r"width=\"(\d+)\"", test_picture).group(1) == "500"
    assert re.search(r"height=\"(\d+)\"", test_picture).group(1) == str(
        int((600 * 500) / 1000)
    )

    test_picture = piuma_picture(
        context,
        "http://localhost:8000/img/a.png",
        height=500,
        image_width=1000,
        image_height=600,
    )
    assert re.search(r"height=\"(\d+)\"", test_picture).group(1) == "500"
    assert re.search(r"width=\"(\d+)\"", test_picture).group(1) == str(
        int((1000 * 500) / 600)
    )

    test_picture = piuma_picture(
        context,
        "http://localhost:8000/img/a.png",
        height=500,
        image_width=1000,
        image_height=600,
    )
    assert re.search(r"height=\"(\d+)\"", test_picture).group(1) == "500"
    assert re.search(r"width=\"(\d+)\"", test_picture).group(1) == str(
        int((1000 * 500) / 600)
    )

    settings.PIUMA_SIZES = {"medium": {"width": 500, "convert_to": "auto"}}
    test_picture = piuma_picture(
        context,
        "http://localhost:8000/img/a.png",
        size="medium",
        image_width=1000,
        image_height=600,
    )
    assert re.search(r"media=\"\(max-width: 576px\)\"", test_picture) == None
    assert re.search(r"media=\"\(max-width: 500px\)\"", test_picture) != None
    assert (
        re.search(
            r"srcset=\"/piuma/500_0_100:auto/http://localhost:8000/img/a.png\"",
            test_picture,
        )
        != None
    )

    piuma_picture_static(context, "img/a.png")


def test_piuma_img(settings, client):
    context = {"request": RequestFactory(HTTP_HOST="localhost:8000").get("/")}

    piuma_img(context, "http://localhost:8000/img/a.png")

    piuma_img(context, "http://localhost:8000/img/a.png", 500)

    test_img = piuma_img(
        context,
        "http://localhost:8000/img/a.png",
        width=500,
        image_width=1000,
        image_height=600,
    )
    assert re.search(r"width=\"(\d+)\"", test_img).group(1) == "500"
    assert re.search(r"height=\"(\d+)\"", test_img).group(1) == str(
        int((600 * 500) / 1000)
    )

    test_img = piuma_img(
        context,
        "http://localhost:8000/img/a.png",
        height=500,
        image_width=1000,
        image_height=600,
    )
    assert re.search(r"height=\"(\d+)\"", test_img).group(1) == "500"
    assert re.search(r"width=\"(\d+)\"", test_img).group(1) == str(
        int((1000 * 500) / 600)
    )

    test_img = piuma_img(
        context, "http://localhost:8000/img/a.png", height=500, alt="test image"
    )
    assert re.search(r"height=\"(\d+)\"", test_img).group(1) == "500"
    assert re.search(r"width=\"(\d+)\"", test_img) == None
    assert re.search(r"alt=\"test image\"", test_img) != None

    test_img = piuma_img(
        context, "http://localhost:8000/img/a.png", image_width=1000, image_height=600
    )
    assert re.search(r"height=\"(\d+)\"", test_img).group(1) == "600"
    assert re.search(r"width=\"(\d+)\"", test_img).group(1) == "1000"
    assert (
        re.search(r"src=\"/piuma/0_0_100/http://localhost:8000/img/a.png\"", test_img)
        != None
    )

    test_img = piuma_img_static(context, "img/a.png")
    assert (
        re.search(
            r"src=\"/piuma/0_0_100/http://localhost:8000/static/img/a.png\"", test_img
        )
        != None
    )

    test_img = piuma_img(
        context,
        "http://localhost:8000/img/a.png",
        width=300,
        height=100,
        image_width=1000,
        image_height=600,
    )
    assert re.search(r"height=\"(\d+)\"", test_img).group(1) == "100"
    assert re.search(r"width=\"(\d+)\"", test_img).group(1) == "300"
    assert (
        re.search(
            r"src=\"/piuma/300_100_100/http://localhost:8000/img/a.png\"", test_img
        )
        != None
    )

    settings.PIUMA_SIZES = {"*": {"width": 500, "convert_to": "auto"}}
    test_img = piuma_img(
        context,
        "http://localhost:8000/img/a.png",
        image_width=1000,
        image_height=600,
    )

    assert (
        re.search(
            r"src=\"/piuma/500_0_100:auto/http://localhost:8000/img/a.png\"", test_img
        )
        != None
    )
    assert re.search(r"width=\"(\d+)\"", test_img).group(1) == "500"
    assert re.search(r"height=\"(\d+)\"", test_img).group(1) == str(
        int((600 * 500) / 1000)
    )

    settings.PIUMA_DISABLED = True
    test_img = piuma_img(
        context,
        "http://localhost:8000/img/a.png",
        image_width=1000,
        image_height=600,
    )
    assert re.search(r"piuma", test_img) == None
    assert re.search(r"width=\"1000\"", test_img) != None
