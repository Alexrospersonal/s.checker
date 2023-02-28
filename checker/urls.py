from django.urls import path

from .views import (
    CategoryListView, ItemsListView, product_list,
    ProductDetailView, logout, ProductFormView, LoginView, conver_image_view, download_files_view,
    DeleteProductView,
    # image_multiple_form_view
)
from .auth import Login

urlpatterns = [
    # path('login/', Login.as_view(), name='login_user'),
    path('login/', LoginView.as_view(), name='login_user'),
    path('logout/', logout, name='logout_user'),
    # path('', MainView.as_view(), name='main'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('items/<int:pk>/', ItemsListView.as_view(), name='items'),
    path('', product_list, name='products_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='products_detail'),
    path('delete_product/<int:pk>', DeleteProductView.as_view(), name='delete_product'),
    path('test_new_form/<int:pk>', ProductFormView.as_view(), name='test_new_form'),
    path('conver-file/', conver_image_view, name='conver_image_view'),
    path('download-files/<int:pk>', download_files_view, name="download_files_view")
    # path('image-multiple-form-view/', image_multiple_form_view, name='image_multiple_form_view'),
]
