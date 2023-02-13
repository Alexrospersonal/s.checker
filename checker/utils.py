import os
from random import randint
from importlib._common import _
from io import BytesIO

from PIL import Image
from django.core.exceptions import ValidationError
from django.core.files import File
from django.contrib import messages

from checker.models import ItemCover, ItemPaper, Manager, Designer, Category, Item


def create_choices(qs_object):
    """
    function take query set and
    create choices [(pk, name), (pk, name), ....] for
    forms.ChoiceField
    """
    choices_list = []
    for obj in qs_object:
        choices_list.append((obj.pk, obj.__str__()))
    return choices_list


def compresing_image(image):
    original_img = Image.open(image)
    copy_of_image = original_img.copy()

    copy_of_image.thumbnail(size=(512, 512), resample=Image.Resampling.LANCZOS)
    img_io = BytesIO()
    copy_of_image.save(img_io, format='JPEG', quality=50)
    filename, ext = os.path.splitext(image.name)
    new_name = filename + "_thumbnail.jpeg"
    new_img = File(img_io, name=new_name)
    return new_img


def rename_image(image, product_name, front=False):
    name, ext = os.path.splitext(image.name)
    new_product_name = product_name.replace(' ', '_')
    sufix = str(randint(1000, 9000))
    # Добавити можливіть перевірки якщо тільки 2 файли то писати лице і зворот
    new_name = f'{new_product_name}_{sufix}{ext}'
    image.name = new_name
    return image


def add_values_to_fields(obj, form, kwargs, request):
    obj_sizes_qs = obj.itemsize_set.all()
    obj_cover_qs = ItemCover.objects.filter(items__id=kwargs['pk']) & ItemCover.objects.filter(in_stock=True)
    obj_paper_qs = ItemPaper.objects.filter(items__id=kwargs['pk']) & ItemPaper.objects.filter(in_stock=True)
    manager = Manager.objects.all()
    designer = Designer.objects.all()
    form.fields['item'].choices = [(obj.pk, obj.__str__())]
    form.fields['size'].choices = create_choices(obj_sizes_qs)
    form.fields['cover'].choices = create_choices(obj_cover_qs)
    form.fields['paper'].choices = create_choices(obj_paper_qs)
    if hasattr(request.user.employee, 'manager'):
        form.fields['designer'].choices = create_choices(designer)
    elif hasattr(request.user.employee, 'designer'):
        form.fields['manager'].choices = create_choices(manager)
    return form


def get_image_size(image):
    return round(image.width * 25.4 / 300), round(image.height * 25.4 / 300)


def get_image_dpi( img, form_size):
    return round(((img.width * 25.4 / form_size[0]) + (img.height * 25.4 / form_size[1])) / 2)


def create_validator(data, request):
    cleaned_data = data
    request = request

    def complex_validator(image_list):
        for img in image_list:
            image = Image.open(img)
            validate_image_color_mode(image)
            validate_image_format(image)
            start_image_validate(image)

    def validate_image_color_mode(value):
        color_mode = value.mode
        if color_mode != 'CMYK':
            messages.add_message(request, messages.ERROR, f'Color mode is {color_mode}')

    def validate_image_format(value):
        image_format = value.format
        if image_format not in ('TIFF', 'JPEG', 'PDF'):
            messages.add_message(request, messages.ERROR, f'{image_format} is not correct')

    def start_image_validate(image):
        form_size = cleaned_data['size'].width, cleaned_data['size'].height
        if image:
            validate_image_size(image, form_size)
            validate_image_dpi(image, form_size)

    def validate_image_size(image, form_size):
        error_size = []
        image_size = get_image_size(image)

        cut_value = Category.objects.get(item__pk=cleaned_data['item'].pk).cut_size

        for index, image in enumerate(image_size):
            if image != form_size[index] + cut_value * 2:
                error_size.append(form_size[index] + cut_value)

        if error_size:
            messages.add_message(request, messages.ERROR,
                                 f'Розмір файлу {image_size[0]}x{image_size[0]}мм, потрібно: {error_size[0]}x{error_size[1]}мм')

    def validate_image_dpi(image, form_size):
        image_dpi = get_image_dpi(image, form_size)
        dpi_from_model = getattr(Item.objects.get(pk=cleaned_data['item'].pk), 'dpi')

        if image_dpi < dpi_from_model:
            messages.add_message(request, messages.ERROR, f'{image_dpi} is not correct')

    return complex_validator


