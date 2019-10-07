import os
from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag
def piuma(url, width=0, height=0, quality=80):
    piuma_host = getattr(settings, 'PIUMA_HOST', '/piuma/')
    return os.path.join(
        piuma_host,
        '{0}_{1}_{2}'.format(width, height, quality),
        url
    )
