from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from pypiuma import piuma_url


register = template.Library()


def get_host_url(request):
    if request:
        return '{0}://{1}'.format(
            request.scheme, request.META['HTTP_HOST']
        )
    return ''


@register.simple_tag(takes_context=True)
def piuma(context, image_url, width=0, height=0, quality=100):
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
def piuma_static(context, image_url, width=0, height=0, quality=100):
    return piuma(context, static(image_url), width, height, quality)


def _generate_srcset(context, image_url, media_rule, size):
    return "<source media='{0}' srcset='{1}'>".format(
        media_rule,
        piuma(context, image_url, width=size)
    )


def _generate_media_rules_sizes(context, media_rules):
    generated_media_rules = []
    media_rules = media_rules.split(',')
    for media_rule in media_rules:
        sanitized_media_rule = media_rule.replace(
            ' ', ''
        ).replace(
            '(', ''
        ).replace(
            ')', ''
        ).replace(
            'px', ''
        )
        generated_media_rules.append([
            media_rule, sanitized_media_rule.split(':')[1]
        ])
    return generated_media_rules


def _generate_picture_tag(picture_id, picture_class):
    picture_tag = "<picture "
    if picture_id:
        picture_tag += "id='{0}' ".format(picture_id)
    if picture_class:
        picture_tag += "class='{0}'".format(picture_class)
    picture_tag += ">"
    return picture_tag


def _generate_picture_img(context, image_url, img_alt, img_id, img_class):
    picture_img = "<img src='{0}' alt='{1}' ".format(
        piuma(context, image_url), img_alt
    )
    if img_id:
        picture_img += "id='{0}' ".format(img_id)
    if img_class:
        picture_img += "class='{0}' ".format(img_class)
    picture_img += ">"
    return picture_img


@register.simple_tag(takes_context=True)
def piuma_picture(context, image_url, media_rules=None, picture_id="", img_id="", picture_class="", img_class="", img_alt=""):
    if not media_rules:
        media_rules = getattr(
            settings,
            'PIUMA_MEDIA_RULES',
            '(max-width: 576px),(max-width: 768px),(max-width: 992px),(max-width: 1366px)'
        )
    html = _generate_picture_tag(picture_id, picture_class)
    for media_rule_size in _generate_media_rules_sizes(context, media_rules):
        html += _generate_srcset(
            context, image_url,
            media_rule_size[0], media_rule_size[1]
        )
    html += _generate_picture_img(context, image_url, img_alt, img_id, img_class)
    html += "</picture>"
    return mark_safe(html)


@register.simple_tag(takes_context=True)
def piuma_picture_static(context, image_url, media_rules=None, picture_id="", img_id="", picture_class="", img_class="", img_alt=""):
    print(static(image_url))
    return piuma_picture(
        context, static(image_url), media_rules,
        picture_id, img_id, picture_class,
        img_class, img_alt
    )
