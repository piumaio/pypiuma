from django import template
from django.conf import settings
from django.templatetags.static import static
from pypiuma import piuma_url


register = template.Library()


def get_host_url(request):
    if request:
        return '{0}://{1}'.format(
            request.scheme, request.META['HTTP_HOST']
        )
    return ''


@register.simple_tag(takes_context=True)
def piuma(context, image_url, width=0, height=0, quality=80):
    if getattr(settings, 'PIUMA_DISABLED', False):
        return image_url
    if not image_url.startswith('http'):
        image_url = get_host_url(
            context.get('request', None)
        ).rstrip('/') + '/' + image_url.lstrip('/')
    return piuma_url(
        getattr(settings, 'PIUMA_HOST', '/piuma/'),
        image_url, width, height, quality
    )


@register.simple_tag(takes_context=True)
def piuma_static(context, image_url, width=0, height=0, quality=80):
    return piuma(context, static(image_url), width, height, quality)
