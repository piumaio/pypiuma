import os
from django import template
from django.conf import settings


register = template.Library()


def get_host_url(request):
    if request:
        return '{0}://{1}'.format(
            request.scheme, request.META['HTTP_HOST']
        )
    return ''


@register.simple_tag(takes_context=True)
def piuma(context, url, width=0, height=0, quality=80):
    if getattr(settings, 'PIUMA_DISABLED', False):
        return url
    piuma_host = getattr(settings, 'PIUMA_HOST', '/piuma/')
    piuma_url = '/'.join(i.strip('/') for i in [
        '{0}_{1}_{2}'.format(width, height, quality),
        url
    ])
    piuma_url = '/'.join(i.rstrip('/') for i in [piuma_host, piuma_url])
    if not piuma_url.startswith('http'):
        piuma_url = get_host_url(context['request']) + piuma_url
    return piuma_url
