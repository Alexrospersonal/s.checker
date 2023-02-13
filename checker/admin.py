from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


# admin.site.register(User, UserAdmin)

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(ItemSize)
admin.site.register(ItemPaper)
admin.site.register(ItemCover)
admin.site.register(Manager)
admin.site.register(Designer)
# admin.site.register(Position)
admin.site.register(User)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductStatus)
admin.site.register(PagesNumber)


