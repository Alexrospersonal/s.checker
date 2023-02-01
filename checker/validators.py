import os

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_image_color_mode(value):
    color_mode = value.image.mode
    if color_mode != 'CMYK':
        raise ValidationError(_(f'Color mode is {color_mode}'))


def validate_image_format(value):
    image_format = value.image.format
    if image_format not in ('TIFF', 'JPEG', 'PDF'):
        raise ValidationError(_(f'{image_format} is not correct'))
