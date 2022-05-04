def piuma_url(
    piuma_host,
    image_url,
    width=0,
    height=0,
    quality=100,
    adaptive_quality=False,
    convert_to="",
):
    piuma_host = piuma_host.rstrip("/")
    piuma_url = "{0}/{1}/{2}".format(
        piuma_host,
        "{0}_{1}_{2}{3}{4}".format(
            width,
            height,
            quality,
            "a" if adaptive_quality else "",
            ":" + convert_to if convert_to else "",
        ),
        image_url,
    )
    return piuma_url
