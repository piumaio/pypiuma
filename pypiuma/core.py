
def piuma_url(piuma_host, image_url, width=0, height=0, quality=100):
    piuma_host = piuma_host.rstrip('/')
    piuma_url = '{0}/{1}/{2}'.format(
        piuma_host,
        '{0}_{1}_{2}'.format(width, height, quality),
        image_url
    )
    return piuma_url
