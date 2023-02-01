import django_filters
from django import forms
from .models import Product, User, Item, ProductStatus, ItemSize, Designer, Manager


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Пошук',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Пошук',
                'class': "filter__form-item",
                "id": "search",
                "type": "search",
            }
        )
    )
    item = django_filters.ModelChoiceFilter(
        lookup_expr='exact',
        queryset=Item.objects.all(),
        widget=forms.Select(
            attrs={
                "name": "product",
                "id": "product",
                "class": "filter__form-item"
            }
        )
    )
    status = django_filters.ModelChoiceFilter(
        lookup_expr='exact',
        queryset=ProductStatus.objects.all(),
        widget=forms.Select(
            attrs={
                "name": "status",
                "id": "status",
                "class": "filter__form-item"
            }
        )
    )
    size = django_filters.ModelChoiceFilter(
        lookup_expr='exact',
        queryset=ItemSize.objects.all(),
        widget=forms.Select(
            attrs={
                "name": "size",
                "id": "size",
                "class": "filter__form-item"
            }
        )
    )
    created_at = django_filters.DateFilter(
        lookup_expr='exact',
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "name": "date",
                "id": "date",
                "class": "filter__form-item"
            }
        )
    )
    manager = django_filters.ModelChoiceFilter(
        lookup_expr='exact',
        queryset=Manager.objects.all(),
        widget=forms.Select(
            attrs={
                "name": "manager",
                "id": "manager",
                "class": "filter__form-item"
            }
        )
    )
    designer = django_filters.ModelChoiceFilter(
        lookup_expr='exact',
        queryset=Designer.objects.all(),
        widget=forms.Select(
            attrs={
                "name": "designer",
                "id": "designer",
                "class": "filter__form-item"
            }
        )
    )

    class Meta:
        model = Product
        fields = {
            'name': ['icontains'],
            'item': ['exact'],
            'status': ['exact'],
            'size': ['exact'],
            'created_at': ['exact'],
            'manager': ['exact'],
            'designer': ['exact']

        }


class ProductFilterForManager(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Пошук',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Пошук',
                'class': "filter__form-item",
                "id": "search",
                "type": "search",
            }
        )
    )
    item = django_filters.ModelChoiceFilter(
        lookup_expr='exact',
        queryset=Item.objects.all(),
        widget=forms.Select(
            attrs={
                "name": "product",
                "id": "product",
                "class": "filter__form-item"
            }
        )
    )
    status = django_filters.ModelChoiceFilter(
        lookup_expr='exact',
        queryset=ProductStatus.objects.all(),
        widget=forms.Select(
            attrs={
                "name": "status",
                "id": "status",
                "class": "filter__form-item"
            }
        )
    )
    size = django_filters.ModelChoiceFilter(
        lookup_expr='exact',
        queryset=ItemSize.objects.all(),
        widget=forms.Select(
            attrs={
                "name": "size",
                "id": "size",
                "class": "filter__form-item"
            }
        )
    )
    created_at = django_filters.DateFilter(
        lookup_expr='exact',
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "name": "date",
                "id": "date",
                "class": "filter__form-item"
            }
        )
    )
    designer = django_filters.ModelChoiceFilter(
        lookup_expr='exact',
        queryset=Designer.objects.all(),
        widget=forms.Select(
            attrs={
                "name": "designer",
                "id": "designer",
                "class": "filter__form-item"
            }
        )
    )

    class Meta:
        model = Product
        fields = {
        }


class ProductFilterForDesigner(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Пошук',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Пошук',
                'class': "filter__form-item",
                "id": "search",
                "type": "search",
            }
        )
    )
    item = django_filters.ModelChoiceFilter(
        lookup_expr='exact',
        queryset=Item.objects.all(),
        widget=forms.Select(
            attrs={
                "name": "product",
                "id": "product",
                "class": "filter__form-item"
            }
        )
    )
    status = django_filters.ModelChoiceFilter(
        lookup_expr='exact',
        queryset=ProductStatus.objects.all(),
        widget=forms.Select(
            attrs={
                "name": "status",
                "id": "status",
                "class": "filter__form-item"
            }
        )
    )
    size = django_filters.ModelChoiceFilter(
        lookup_expr='exact',
        queryset=ItemSize.objects.all(),
        widget=forms.Select(
            attrs={
                "name": "size",
                "id": "size",
                "class": "filter__form-item"
            }
        )
    )
    created_at = django_filters.DateFilter(
        lookup_expr='exact',
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "name": "date",
                "id": "date",
                "class": "filter__form-item"
            }
        )
    )
    manager = django_filters.ModelChoiceFilter(
        lookup_expr='exact',
        queryset=Manager.objects.all(),
        widget=forms.Select(
            attrs={
                "name": "manager",
                "id": "manager",
                "class": "filter__form-item"
            }
        )
    )

    class Meta:
        model = Product
        fields = {
            'name': ['icontains'],
            'item': ['exact'],
            'status': ['exact'],
            'size': ['exact'],
            'created_at': ['exact'],
            'manager': ['exact'],

        }