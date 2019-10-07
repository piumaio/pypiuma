import os
from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag
def piuma(url, width=0, height=0, quality=80):
    if getattr(settings, 'PIUMA_DISABLED', False):
        return url
    piuma_host = getattr(settings, 'PIUMA_HOST', '/piuma/')
    piuma_url = '/'.join(i.strip('/') for i in [
        '{0}_{1}_{2}'.format(width, height, quality),
        url
    ])
    return '/'.join(i.rstrip('/') for i in [piuma_host, piuma_url])
