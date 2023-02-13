import os

from django import forms
from django.core.validators import validate_image_file_extension
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, UsernameField

from .models import *

from PIL import Image

from .validators import validate_image_color_mode, validate_image_format
from .utils import get_image_dpi, get_image_size


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={
            'type': 'text',
            'placeholder': 'введіть логін',
            'id': 'login'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'type': 'password',
            'placeholder': 'введіть пароль',
            'id': 'password'
        }
    ))


class FileForm(forms.Form):
    name = forms.CharField(label='File name', max_length=100)
    img = forms.ImageField()


# class ItemForm(forms.Form):
#     name = forms.CharField(label='Назва', max_length=150)
#     item = forms.ChoiceField()
#     size = forms.ChoiceField(label='Розміри', widget=forms.RadioSelect())
#     paper = forms.ChoiceField(label='Папір', widget=forms.RadioSelect())
#     cover = forms.ChoiceField(label='Ламінація', widget=forms.RadioSelect())
#     description = forms.CharField(label='Опис', max_length=440, required=False ,widget=forms.Textarea(attrs={
#         'title': 'Опис',
#     }))
#     manager = forms.ChoiceField(label='Менеджер', widget=forms.RadioSelect())
#     designer = forms.ChoiceField(label='Дизайнер', widget=forms.RadioSelect())
#
#     # status = forms.ChoiceField(choices=[
#     #     ('1', 'в очікуванні'), ('2', 'в роботі'),
#     #     ('3', 'відхилено'), ('4', 'брак')
#     # ], initial='1', label='')
#
#     front_img = forms.ImageField(label="Лице")
#     back_img = forms.ImageField(required=False, label="Зворот")
#
#     quantity = forms.IntegerField(min_value=1, max_value=1_000_000, initial=1, label='Кількість')
#
#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop('request')
#         self.user = getattr(self.request, 'user')
#         super().__init__(*args, **kwargs)
#
#         #if user is manager or designer, delete current fielf drom form
#         fields = self.fields
#         # if self.user.employee.manager:
#         if hasattr(self.user.employee, 'manager'):
#             del fields['manager']
#         # elif self.user.employee.designer:
#         elif hasattr(self.user.employee, 'designer'):
#             del fields['designer']
#
#     def clean(self):
#         cleaned_data = super().clean()
#         self.image_check(cleaned_data)
#
#     def get_image(self, value):
#         img = self.cleaned_data.get(value, False)
#         if img:
#             return img
#         elif self.files[value]:
#             return Image.open(self.files[value])
#         else:
#             return None
#
#     def image_check(self, cleaned_data):
#         sizes_from_model = ItemSize.objects.get(pk=cleaned_data['size'])
#         model_size = (sizes_from_model.width, sizes_from_model.height)
#
#         front_image = cleaned_data.get('front_img', False)
#         back_image = cleaned_data.get('back_img', False)
#
#         # front_image = cleaned_data.get('front_img', False).image
#         # back_image = cleaned_data.get('back_img', False).image
#
#         # self.cleaned_data['front_img'] = front_image
#         # self.cleaned_data['back_img'] = back_image
#
#         # try:
#         #     front_image = cleaned_data['front_img'].image
#         #     back_image = cleaned_data['back_img'].image
#         #
#         #     # if cleaned_data['front_img']:
#         #     #     front_image = cleaned_data['front_img'].image
#         #     # else:
#         #     #     front_image = self.files['front_img']
#         # except KeyError:
#         #     # Image.MAX_IMAGE_PIXELS = 933120000
#         #     front_image = Image.open(self.files['front_img'])
#         #
#         #     if not cleaned_data['back_img'] and self.files['back_img']:
#         #         back_image = Image.open(self.files['back_img'])
#
#         if back_image:
#             front_image = front_image.image
#             back_image = back_image.image
#             # images = ((cleaned_data['front_img'].image, 'front_img'), (cleaned_data['back_img'].image, 'back_img'))
#             images = ((front_image, 'front_img'), (back_image, 'back_img'))
#         else:
#             front_image = front_image.image
#             # images = ((cleaned_data['front_img'].image, 'front_img'),)
#             images = ((front_image, 'front_img'),)
#
#         # if cleaned_data['back_img']:
#         #     # images = ((cleaned_data['front_img'].image, 'front_img'), (cleaned_data['back_img'].image, 'back_img'))
#         #     images = ((front_image, 'front_img'), (cleaned_data['back_img'].image, 'back_img'))
#         # else:
#         #     # images = ((cleaned_data['front_img'].image, 'front_img'),)
#         #     images = ((front_image, 'front_img'),)
#
#         for image in images:
#             self.check_img_format(image)
#             image_mode = image[0].mode
#             image_size_and_dpi = self.get_image_size(image[0]), self.get_image_dpi(image[0], model_size)
#             self.validate_image(image_mode, image_size_and_dpi, model_size, image[1])
#
#     def check_img_format(self, image):
#         if image[0].format not in ('TIFF', 'JPEG', 'PDF'):
#             self.add_error(f'{image[1]}', f'Формат не відповідяє вимогам: [TIFF, JPEG, PDF] != {image[0].format}')
#
#     def validate_image(self, image_mode, front_image_size_and_dpi, model_size, error_message):
#         """
#         function take a four arguments:
#             image mode: string,
#             front_image_size_and_dpi: Tupple with list of sizes and DPI ([90, 50], 300)
#             model_size: size from Model
#             error_message is message of error
#         """
#         if image_mode != "CMYK":
#             self.add_error(f'{error_message}', f'Кольоровий профіль не CMYK: {image_mode}')
#
#         cut_value_from_model = getattr(Category.objects.get(item__pk=self.cleaned_data['item']), 'cut_size') * 2
#
#         for index, size in enumerate(front_image_size_and_dpi[0]):
#             if size != model_size[index] + cut_value_from_model:
#                 self.add_error(f'{error_message}', f'зображення не відповідає розміру: {front_image_size_and_dpi[0]}'
#                                                  f'!= {model_size}')
#                 break
#         dpi_from_model = getattr(Item.objects.get(pk=self.cleaned_data['item']), 'dpi')
#         if front_image_size_and_dpi[1] < dpi_from_model:
#             self.add_error(f'{error_message}', f'DPI має бути 300 і більше: {front_image_size_and_dpi[1]}')
#
#     def get_image_dpi(self, img, model_size):
#         """
#         Convert width and height to DPI and round value,
#         formula: dpi = 5669px * 25.4mm / 900mm = 160dpi
#         5669px - image size,
#         25.4mm - Inches,
#         900mm - real size of image,
#         Example:
#             width dpi - (busuness card 90x50mm): 1110px * 25.4 / 90mm = 313dpi
#             height dpi - (busuness card 90x50mm): 600px * 25.4 / 50mm = 304dpi
#             dpi: (width + height) / 2 - (313 + 304) / 2 = 308dpi
#         """
#         return round(((img.width * 25.4 / model_size[0]) + (img.height * 25.4 / model_size[1])) / 2)
#
#     def get_image_size(self, image):
#         """
#         Conver image size from pixels to milimeters and round values,
#         image object must have 2 params, width and height
#         formula:
#             width = 3264px * 25.4mm / 100dpi = 830mm
#             height = 3264px * 25.4mm / 100dpi = 830mm
#         5669px - image size,
#         2.54cm - Centimeters,
#         100dpi - dpi for we needed
#         Example:
#             width - 1110px * 2.54 / 300dpi = 9.4cm or 1110px * 25.4 / 300dpi = 94mm
#             height - 600px * 2.54 / 300dpi = 5cm or 600px * 25.4 / 300dpi = 90mm
#         """
#         return round(image.width * 25.4 / 300), round(image.height * 25.4 / 300)


# class TestImageForm(forms.ModelForm):
#     image = forms.ImageField(label='Зображення', widget=forms.ClearableFileInput(
#         attrs={
#             # "multiple": True,
#         }
#     ))
    #
    # images = forms.FileField(
    #     label='Лице',
    #     widget=forms.ClearableFileInput(
    #         attrs={
    #             "name": "file",
    #             "accept": ".jpeg, .jpg, .tif, .pdf",
    #             "id": "front-image-button",
    #             "multiple": True,
    #         },
    #     ),
    # )

    # def clean(self):
    #     pass
    #
    # def clean_image(self):
    #     pass
    #
    # class Meta:
    #     model = ProductImage
    #     fields = [
    #         'image',
    #     ]


class ProductImageForm(forms.ModelForm):

    image = forms.ImageField(
        label='Лице',
        widget=forms.ClearableFileInput(
            attrs={
                "name": "file",
                "accept": ".jpeg, .jpg, .tif, .pdf",
                "id": "front-image-button",
                "multiple": True,
            },
        ),
    )

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        self.start_image_validate(image)
        return image

    def start_image_validate(self, image):
        form_size = self.cleaned_data['size'].width, self.cleaned_data['size'].height
        if image:
            self.validate_image_size(image.image, form_size)
            self.validate_image_dpi(image.image, form_size)

    def validate_image_size(self, image, form_size):
        image_size = get_image_size(image)
        cut_value = Category.objects.get(item__pk=self.cleaned_data['item'].pk).cut_size

        for index, image in enumerate(image_size):
            if image != form_size[index] + cut_value * 2:
                raise ValidationError(_(f'{image_size} is not correct must be{form_size[index] + cut_value}'))

    def validate_image_dpi(self, image, form_size):
        image_dpi = get_image_dpi(image, form_size)
        dpi_from_model = getattr(Item.objects.get(pk=self.cleaned_data['item'].pk), 'dpi')

        if image_dpi < dpi_from_model:
            raise ValidationError(_(f'{image_dpi} is not correct'))

    class Meta:
        model = ProductImage
        fields = [
            'image',
        ]


class ProductForm(forms.ModelForm):
    item = forms.ModelChoiceField(
        queryset=None, label='Одиниця',
        widget=forms.RadioSelect(
            attrs={
                "checked": ""
            }
        )
    )
    size = forms.ModelChoiceField(
        queryset=None,
        label="Розмір",
        widget=forms.RadioSelect(
            attrs={

            }
        )
    )
    paper = forms.ModelChoiceField(
        queryset=None,
        label='Матеріал',
        widget=forms.RadioSelect(
            attrs={

            }
        )
    )
    cover = forms.ModelChoiceField(
        queryset=None,
        label='Покриття',
        widget=forms.RadioSelect(
            attrs={

            }
        )
    )
    manager = forms.ModelChoiceField(
        queryset=None,
        label='Менеджер',
        widget=forms.RadioSelect(
            attrs={

            }
        )
    )
    designer = forms.ModelChoiceField(
        queryset=None,
        label='Дизайнер',
        widget=forms.RadioSelect(
            attrs={

            }
        )
    )
    description = forms.CharField(
        label='Опис',
        max_length=440,
        required=False,
        widget=forms.Textarea(
            attrs={
                'title': 'Опис',
                'name': 'text',
                'id': 'textArea'
            }
        )
    )
    # front_image = forms.ImageField(
    #     label='Лице',
    #     widget=forms.FileInput(
    #         attrs={
    #             "name": "file",
    #             "accept": ".jpeg, .jpg, .tif, .pdf",
    #             "id": "front-image-button"
    #         },
    #     ),
    #     validators=[
    #         validate_image_file_extension,
    #         validate_image_color_mode,
    #         validate_image_format
    #     ]
    # )
    # back_image = forms.ImageField(
    #     label='Зворот',
    #     required=False,
    #     widget=forms.FileInput(
    #         attrs={
    #             "name": "file",
    #             "accept": ".jpeg, .jpg, .tif, .pdf",
    #             "id": "back-image-button"
    #         },
    #     ),
    #     validators=[
    #         validate_image_file_extension,
    #         validate_image_color_mode,
    #         validate_image_format
    #     ]
    # )

    def __init__(self, *args, **kwargs):
        self.item_pk = kwargs.pop('item_id')
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        fields = self.fields
        fields['item'].queryset = Item.objects.filter(pk=self.item_pk)
        fields['size'].queryset = ItemSize.objects.filter(items__pk=self.item_pk)
        fields['paper'].queryset = ItemPaper.objects.filter(items__pk=self.item_pk)
        fields['cover'].queryset = ItemCover.objects.filter(items__pk=self.item_pk)
        self.add_user_to_fields()

    def add_user_to_fields(self):
        if hasattr(self.user.employee, 'manager'):
            manager = Manager.objects.filter(pk=self.user.employee.manager.id)
            self.fields['manager'].queryset = manager
            self.fields['manager'].choices = [(manager[0].id, manager[0])]
            self.fields['designer'].queryset = Designer.objects.all()

        elif hasattr(self.user.employee, 'manager'):
            designer = Designer.objects.filter(pk=self.user.employee.designer.id)
            self.fields['designer'].queryset = designer
            self.fields['designer'].choices = [(designer[0].id, designer[0])]
            self.fields['manager'].queryset = Manager.objects.all()

    # def clean_front_image(self):
    #     image = self.cleaned_data.get('front_image', False)
    #     self.start_image_validate(image)
    #     return image
    #
    # def clean_back_image(self):
    #     image = self.cleaned_data.get('back_image', False)
    #     self.start_image_validate(image)
    #     return image
    #
    # def start_image_validate(self, image):
    #     form_size = self.cleaned_data['size'].width, self.cleaned_data['size'].height
    #     if image:
    #         self.validate_image_size(image.image, form_size)
    #         self.validate_image_dpi(image.image, form_size)
    #
    # def validate_image_size(self, image, form_size):
    #     image_size = get_image_size(image)
    #     cut_value = Category.objects.get(item__pk=self.cleaned_data['item'].pk).cut_size
    #
    #     for index, image in enumerate(image_size):
    #         if image != form_size[index] + cut_value * 2:
    #             raise ValidationError(_(f'{image_size} is not correct must be{form_size[index] + cut_value}'))
    #
    # def validate_image_dpi(self, image, form_size):
    #     image_dpi = get_image_dpi(image, form_size)
    #     dpi_from_model = getattr(Item.objects.get(pk=self.cleaned_data['item'].pk), 'dpi')
    #
    #     if image_dpi < dpi_from_model:
    #         raise ValidationError(_(f'{image_dpi} is not correct'))

    class Meta:
        model = Product
        fields = [
            'item', 'name', 'size', 'paper', 'cover',
            'description', 'manager', 'designer',
            'quantity'
        ]


class ProductEditForm(forms.ModelForm):
    item = forms.ModelChoiceField(
        queryset=None, label='Одиниця',
        widget=forms.RadioSelect(
            attrs={
                "checked": ""
            }
        )
    )
    size = forms.ModelChoiceField(
        queryset=None,
        label="Розмір",
        widget=forms.RadioSelect(
            attrs={

            }
        )
    )
    paper = forms.ModelChoiceField(
        queryset=None,
        label='Матеріал',
        widget=forms.RadioSelect(
            attrs={

            }
        )
    )
    cover = forms.ModelChoiceField(
        queryset=None,
        label='Покриття',
        widget=forms.RadioSelect(
            attrs={

            }
        )
    )
    manager = forms.ModelChoiceField(
        queryset=None,
        label='Менеджер',
        widget=forms.RadioSelect(
            attrs={

            }
        )
    )
    designer = forms.ModelChoiceField(
        queryset=None,
        label='Дизайнер',
        widget=forms.RadioSelect(
            attrs={

            }
        )
    )
    description = forms.CharField(
        label='Опис',
        max_length=440,
        required=False,
        widget=forms.Textarea(
            attrs={
                'title': 'Опис',
                'name': 'text',
                'id': 'textArea'
            }
        )
    )
    # front_image = forms.ImageField(label='Лице')
    # back_image = forms.ImageField(label='Зворот', required=False)

    def __init__(self, *args, **kwargs):

        self.item_pk = kwargs['instance'].item_id
        self.user = kwargs.pop('user')
        super(forms.ModelForm, self).__init__(*args, **kwargs)

        fields = self.fields
        item = Item.objects.filter(pk=self.item_pk)
        fields['item'].queryset = item
        fields['item'].choices = [(item[0].id, item[0])]
        fields['size'].queryset = ItemSize.objects.filter(items__pk=self.item_pk)
        fields['paper'].queryset = ItemPaper.objects.filter(items__pk=self.item_pk)
        fields['cover'].queryset = ItemCover.objects.filter(items__pk=self.item_pk)
        self.add_user_to_fields()

    def add_user_to_fields(self):
        if hasattr(self.user.employee, 'manager'):
            manager = Manager.objects.filter(pk=self.user.employee.manager.id)
            self.fields['manager'].queryset = manager
            self.fields['manager'].choices = [(manager[0].id, manager[0])]
            self.fields['designer'].queryset = Designer.objects.all()

        elif hasattr(self.user.employee, 'manager'):
            designer = Designer.objects.filter(pk=self.user.employee.designer.id)
            self.fields['designer'].queryset = designer
            self.fields['designer'].choices = [(designer[0].id, designer[0])]
            self.fields['manager'].queryset = Manager.objects.all()

    # def clean_front_image(self):
    #     image = self.cleaned_data.get('front_image', False)
    #     self.start_image_validate(image)
    #     return image
    #
    # def clean_back_image(self):
    #     image = self.cleaned_data.get('back_image', False)
    #     self.start_image_validate(image)
    #     return image
    #
    # def start_image_validate(self, image):
    #     form_size = self.cleaned_data['size'].width, self.cleaned_data['size'].height
    #     if hasattr(image, 'image'):
    #         valid_image = image.image
    #     else:
    #         valid_image = image
    #     if image:
    #         self.validate_image_size(valid_image, form_size)
    #         self.validate_image_dpi(valid_image, form_size)
    #
    # def validate_image_size(self, image, form_size):
    #     image_size = get_image_size(image)
    #     cut_value = Category.objects.get(item__pk=self.item_pk).cut_size
    #
    #     for index, image in enumerate(image_size):
    #         if image != form_size[index] + cut_value:
    #             raise ValidationError(_(f'{image_size} is not correct'))
    #
    # def validate_image_dpi(self, image, form_size):
    #     image_dpi = get_image_dpi(image, form_size)
    #     dpi_from_model = getattr(Item.objects.get(pk=self.item_pk), 'dpi')
    #
    #     if image_dpi < dpi_from_model:
    #         raise ValidationError(_(f'{image_dpi} is not correct'))

    class Meta:
        model = Product
        fields = [
            'name', 'size', 'paper', 'cover', 'description',
            'manager', 'designer', 'quantity',
        ]
