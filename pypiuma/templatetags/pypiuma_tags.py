import re

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from pypiuma import piuma_url


exclude_regex = r".+\.(svg)$"
register = template.Library()


def get_host_url(request):
    if request:
        return "{0}://{1}".format(request.scheme, request.META["HTTP_HOST"])
    return ""


def piuma_size(size, **params):
    if getattr(settings, "PIUMA_SIZES", {}).get(size):
        params = {**params, **settings.PIUMA_SIZES[size]}
    elif not size and "*" in getattr(settings, "PIUMA_SIZES", {}):
        params = {**params, **settings.PIUMA_SIZES["*"]}

    return params


def piuma_media_rules(image_width=None):
    return (
        getattr(
            settings,
            "PIUMA_MEDIA_RULES",
            "(max-width: 576px),(max-width: 768px),(max-width: 992px),(max-width: 1366px)",
        )
        + (",(max-width: {0}px)".format(image_width) if image_width else "")
    )


@register.simple_tag(takes_context=True)
def piuma(
    context,
    image_url,
    width=0,
    height=0,
    quality=100,
    adaptive_quality=False,
    convert_to="",
    size="",
):
    if getattr(settings, "PIUMA_DISABLED", False) or re.match(exclude_regex, image_url):
        return image_url
    if not image_url.startswith("http"):
        image_url = (
            get_host_url(context.get("request", None)).rstrip("/")
            + "/"
            + image_url.lstrip("/")
        )
    return piuma_url(
        getattr(settings, "PIUMA_HOST", "/piuma/"),
        image_url,
        **piuma_size(
            size,
            width=width,
            height=height,
            quality=quality,
            adaptive_quality=adaptive_quality,
            convert_to=convert_to,
        ),
    )


@register.simple_tag(takes_context=True)
def piuma_static(
    context,
    image_url,
    width=0,
    height=0,
    quality=100,
    adaptive_quality=False,
    convert_to="",
    size="",
):
    return piuma(
        context,
        static(image_url),
        width,
        height,
        quality,
        adaptive_quality,
        convert_to,
        size,
    )


@register.simple_tag(takes_context=True)
def piuma_img(
    context,
    image_url,
    width=0,
    height=0,
    quality=100,
    adaptive_quality=False,
    convert_to="",
    size="",
    image_width=0,
    image_height=0,
    **img_attributes
):
    def generate_img(url, attrs):
        return mark_safe(
            '<img src="{0}" {1}>'.format(
                image_url,
                " ".join(['{0}="{1}"'.format(k, v) for k, v in img_attributes.items()]),
            )
        )

    if getattr(settings, "PIUMA_DISABLED", False):
        tag_width, tag_height = _calculate_image_sizes({}, image_width, image_height)
        if tag_width:
            img_attributes["width"] = tag_width
        if tag_height:
            img_attributes["height"] = tag_height
        return generate_img(image_url, img_attributes)

    params = piuma_size(
        size,
        width=width,
        height=height,
        quality=quality,
        adaptive_quality=adaptive_quality,
        convert_to=convert_to,
    )
    media_rules = _generate_media_rules_sizes(
        context,
        piuma_media_rules(int(params.get("width") or 0) or image_width or 0),
        int(params.get("width") or 0) or image_width or 0,
    )
    img_attributes["sizes"] = ",".join(
        ["{0} {1}px".format(*media_rule) for media_rule in media_rules]
    )
    img_attributes["srcset"] = ",".join(
        [
            "{0} {1}".format(
                piuma(context, image_url, **{**params, "width": w, "height": 0}),
                "{0}w".format(w),
            )
            for _, w in media_rules
        ]
    )
    image_url = piuma(context, image_url, **params)

    tag_width, tag_height = _calculate_image_sizes(params, image_width, image_height)
    if tag_width:
        img_attributes["width"] = tag_width
    if tag_height:
        img_attributes["height"] = tag_height

    return generate_img(image_url, img_attributes)


@register.simple_tag(takes_context=True)
def piuma_img_static(
    context,
    image_url,
    width=0,
    height=0,
    quality=100,
    adaptive_quality=False,
    convert_to="",
    size="",
    image_width=0,
    image_height=0,
    **img_attributes
):
    return piuma_img(
        context,
        static(image_url),
        width,
        height,
        quality,
        adaptive_quality,
        convert_to,
        size,
        image_width,
        image_height,
        **img_attributes,
    )


def _generate_srcset(context, image_url, media_rule, size, **params):
    return "<source media=\"{0}\" srcset=\"{1}\">".format(
        media_rule, piuma(context, image_url, **{**params, "width": size, "height": 0})
    )


def _generate_media_rules_sizes(context, media_rules, size_limit=0):
    generated_media_rules = []
    media_rules = media_rules.split(",")
    for media_rule in media_rules:
        sanitized_media_rule = (
            media_rule.replace(" ", "")
            .replace("(", "")
            .replace(")", "")
            .replace("px", "")
        )
        size = sanitized_media_rule.split(":")[1]

        if int(size_limit) <= 0 or (int(size) <= int(size_limit)):
            generated_media_rules.append((media_rule, size))
    return generated_media_rules


def _generate_picture_tag(**picture_attributes):
    return "<picture {0}>".format(
        " ".join(['{0}="{1}"'.format(k, v) for k, v in picture_attributes.items()])
    )


def _generate_picture_img(context, image_url, params={}, **img_attributes):
    return "<img src=\"{0}\" {1}>".format(
        piuma(context, image_url, **params),
        " ".join(['{0}="{1}"'.format(k, v) for k, v in img_attributes.items()]),
    )


def _calculate_image_sizes(params, original_width, original_height):
    if (
        original_width
        and int(params.get("width") or 0) != 0
        and int(params.get("width") or 0) != original_height
        and int(params.get("height") or 0) == 0
    ):
        return (
            int(params["width"]),
            int((int(original_height) * int(params["width"])) / int(original_width)),
        )
    elif (
        original_height
        and int(params.get("height") or 0) != 0
        and int(params.get("height") or 0) != original_height
        and int(params.get("width") or 0) == 0
    ):
        return (
            int((int(original_width) * int(params["height"])) / int(original_height)),
            int(params["height"]),
        )
    else:
        return (
            int(params.get("width") or 0) or original_width,
            int(params.get("height") or 0) or original_height,
        )


@register.simple_tag(takes_context=True)
def piuma_picture(
    context,
    image_url,
    media_rules=None,
    width=0,
    height=0,
    quality=100,
    adaptive_quality=False,
    convert_to="",
    size="",
    image_width=0,
    image_height=0,
    **attributes
):
    picture_attributes = {
        key: value for key, value in attributes.items() if key.startswith("picture_")
    }
    img_attributes = {
        key: value for key, value in attributes.items() if key.startswith("img_")
    }
    params = piuma_size(
        size,
        width=width,
        height=height,
        quality=quality,
        adaptive_quality=adaptive_quality,
        convert_to=convert_to,
    )
    media_rules = media_rules or piuma_media_rules(
        int(params.get("width") or 0) or image_width or 0
    )
    html = _generate_picture_tag(**picture_attributes)
    for media_rule_size in _generate_media_rules_sizes(
        context, media_rules, int(params.get("width") or 0) or image_width or 0
    ):
        html += _generate_srcset(
            context, image_url, media_rule_size[0], media_rule_size[1], **params
        )

    tag_width, tag_height = _calculate_image_sizes(params, image_width, image_height)
    if tag_width:
        img_attributes["width"] = tag_width
    if tag_height:
        img_attributes["height"] = tag_height

    html += _generate_picture_img(context, image_url, **img_attributes)
    html += "</picture>"
    return mark_safe(html)


@register.simple_tag(takes_context=True)
def piuma_picture_static(
    context,
    image_url,
    media_rules=None,
    width=0,
    height=0,
    quality=100,
    adaptive_quality=False,
    convert_to="",
    size="",
    image_width=0,
    image_height=0,
    **attributes
):
    return piuma_picture(
        context,
        static(image_url),
        media_rules,
        width,
        height,
        quality,
        adaptive_quality,
        convert_to,
        size,
        image_width,
        image_height,
        **attributes,
    )
