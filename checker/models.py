import os
import shutil
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


# class User(AbstractUser):
#     pass


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Назва')
    cut_size = models.SmallIntegerField(verbose_name='Розмір порізки', null=True)

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=150, verbose_name='Назва')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    dpi = models.SmallIntegerField(verbose_name="DPI", null=True)

    class Meta:
        verbose_name = 'Одиниця'
        verbose_name_plural = 'Одиниці'

    def __str__(self):
        return f'{self.name}'


class ItemSize(models.Model):
    name = models.CharField(max_length=150, verbose_name='Назва', null=True, blank=True)
    width = models.IntegerField(verbose_name='Ширина')
    height = models.IntegerField(verbose_name='Висота')
    items = models.ManyToManyField(Item, verbose_name='Елемент')

    class Meta:
        verbose_name = 'Розмір'
        verbose_name_plural = 'Роміри'

    def __str__(self):
        return f'{self.width}x{self.height}мм'


class ItemPaper(models.Model):
    name = models.CharField(max_length=150, verbose_name='Назва')
    paper_width = models.IntegerField(verbose_name='Щільність матеріалу')
    description = models.CharField(max_length=300, verbose_name='Опис', blank=True)
    items = models.ManyToManyField(Item, verbose_name='Елементи')
    in_stock = models.BooleanField(verbose_name="В наявності", null=True, default=True)

    class Meta:
        verbose_name = 'Папір'
        verbose_name_plural = 'Папір'

    def __str__(self):
        return f'{self.name} {self.paper_width}г'


class ItemCover(models.Model):
    name = models.CharField(max_length=150, verbose_name='Назва')
    items = models.ManyToManyField(Item, verbose_name='Елементи')
    in_stock = models.BooleanField(verbose_name="В наявності", null=True, default=True)

    class Meta:
        verbose_name = 'Покриття'
        verbose_name_plural = 'Покриття'

    def __str__(self):
        return f'{self.name}'


# class Position(models.Model):
#     position = models.CharField(max_length=150, verbose_name='Посада')
#
#     def __str__(self):
#         return self.position
#
#     class Meta:
#         verbose_name = 'Посада'
#         verbose_name_plural = 'Посади'


class User(models.Model):
    first_name = models.CharField(max_length=200, verbose_name='Ім\'я')
    last_name = models.CharField(max_length=250, verbose_name='Фамілія')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    e_mail = models.EmailField(max_length=254, verbose_name='Пошта')
    user = models.OneToOneField(get_user_model(), models.CASCADE, null=True, related_name='employee')
    category = models.ForeignKey(Category, models.CASCADE, null=True, related_name='category', blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Працівник'
        verbose_name_plural = 'Працівники'

#
# class Bussinesscard


class Manager(models.Model):
    manager = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='менеджер', related_name="manager")

    def __str__(self):
        return f'{self.manager.first_name} {self.manager.last_name}'

    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджери'


class Designer(models.Model):
    designer = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='дизайнер', related_name="designer")

    def __str__(self):
        return f'{self.designer.first_name} {self.designer.last_name}'

    class Meta:
        verbose_name = 'Дизайнер'
        verbose_name_plural = 'Дизайнери'


class ProductStatus(models.Model):
    name = models.CharField(max_length=100, verbose_name='Статус')
    div_status_class = models.CharField(max_length=50, verbose_name='Стиль блоку', null=True, blank=True)
    img_status_class = models.CharField(max_length=50, verbose_name='Стиль зображення', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статуси'


def product_directory_path(instance, filename):
    product_name = get_name(instance)
    return f'{instance.product.item.category.name}/{instance.product.item.name}/{product_name}/{filename}'


def thumbnail_directory_path(instance, filename):
    product_name = get_name(instance)
    return f'{instance.product.item.category.name}/{instance.product.item.name}/{product_name}/thumbnails/{filename}'


def get_name(instance):
    name = instance.product.name
    name = name.replace(' ', '_')
    name = f'{name}-{datetime.now().strftime("%d_%m_%Y_%H_%M")}'
    return name


class ProductImage(models.Model):
    image = models.ImageField(upload_to=product_directory_path, verbose_name='Зображення', null=True, max_length=300)
    thumbnail = models.ImageField(upload_to=thumbnail_directory_path, verbose_name='Мініатюра', null=True, max_length=300)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, verbose_name='Продукт')

    def save(self, *args, **kwargs):
        if self.pk:
            this_image = ProductImage.objects.get(pk=self.pk)

            folder_path = this_image.image.path.split('\\')
            new_folder_path = '\\'.join(folder_path[:-1])

            if this_image.image != self.front_image:
                this_image.image.delete(save=False)
                this_image.thumbnail.delete(save=False)
            if this_image.name != self.name:
                shutil.rmtree(new_folder_path)

        super(ProductImage, self).save(*args, **kwargs)


class PagesNumber(models.Model):
    pages = models.SmallIntegerField(verbose_name='Кількість сторінок')
    items = models.ManyToManyField(Item, verbose_name='Елементи')

    def __str__(self):
        return f"Pages: {self.pages}"

    class Meta:
        verbose_name = 'Сторінка'
        verbose_name_plural = 'Сторінки'


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Назва')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Елемент', related_name='item')
    size = models.ForeignKey(ItemSize, on_delete=models.CASCADE, verbose_name='Розмір')
    paper = models.ForeignKey(ItemPaper, on_delete=models.CASCADE, verbose_name='Папір')
    cover = models.ForeignKey(ItemCover, on_delete=models.CASCADE, verbose_name='Покриття')
    description = models.TextField(max_length=700, verbose_name='', null=True)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, verbose_name='Менеджер', null=True)
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE, verbose_name='Дизайнер', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(ProductStatus, on_delete=models.CASCADE)
    # front_image = models.ImageField(upload_to=product_directory_path, verbose_name='Лице', null=True)
    # back_image = models.ImageField(upload_to=product_directory_path, verbose_name='Зворот', null=True)
    # front_thumbnail = models.ImageField(upload_to=thumbnail_directory_path, verbose_name='Лице мініатюра', null=True)
    # back_thumbnail = models.ImageField(upload_to=thumbnail_directory_path, verbose_name='Зворот мініатюра', null=True)
    quantity = models.PositiveIntegerField(verbose_name='Кількість', default=1, null=True)

    def get_absolute_url(self):
        return f'/products/{self.pk}'

    def __str__(self):
        return f'{self.name} {self.item} {self.size} {self.paper} {self.cover} {self.manager} {self.designer}'

    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         this_product = Product.objects.get(pk=self.pk)
    #
    #         folder_path = this_product.front_image.path.split('\\')
    #         new_folder_path = '\\'.join(folder_path[:-1])
    #
    #         if this_product.front_image != self.front_image:
    #             this_product.front_image.delete(save=False)
    #             this_product.front_thumbnail.delete(save=False)
    #         if this_product.back_image != self.back_image:
    #             this_product.back_image.delete(save=False)
    #             this_product.back_thumbnail.delete(save=False)
    #         if this_product.name != self.name:
    #             shutil.rmtree(new_folder_path)
    #
    #     super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'
        ordering = ['id']
