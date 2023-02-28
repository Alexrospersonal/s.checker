import os
import zipfile

from django.contrib.messages import get_messages
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
from django.db.models.fields.files import ImageFieldFile
from django.shortcuts import redirect, render, get_list_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.detail import SingleObjectMixin, BaseDetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView, DeletionMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.files.storage import FileSystemStorage
# from django_filters.views import FilterMixin, FilterView
# from django.core.files.base import ContentFile
from django.core.files import File
from django.contrib.auth.views import logout_then_login
from django.core.paginator import Paginator
from django.contrib.auth import views as auth_views
from django.http import FileResponse, HttpResponse, JsonResponse, HttpResponseRedirect

from check_image.settings import MEDIA_ROOT, MEDIA_URL
from checker.forms import FileForm, ProductForm, ProductEditForm, UserLoginForm, ProductImageForm
from .filters import ProductFilter, ProductFilterForManager, ProductFilterForDesigner
from .models import *

from .utils import *


def error_404(requerst, exception):
    context = {'title': '404'}
    response = render(requerst, 'checked/errors/404.html', context)
    response.status_code = 404
    return response


def error_403(requerst, exception):
    context = {'title': '403'}
    response = render(requerst, 'checked/errors/403.html', context)
    response.status_code = 403
    return response


def logout(request):
    return logout_then_login(request, reverse_lazy('checker:login_user'))


def conver_image_view(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        compressed_img = compresing_image(file)
        fs_location = MEDIA_ROOT + r'\tmp_img'
        fs_base_url = MEDIA_URL + r'tmp_img'
        fs = FileSystemStorage(location=fs_location, base_url=fs_base_url)
        filename = fs.save(compressed_img.name, compressed_img)
        uploaded_file_url = fs.url(filename)
        absolute_file_url = request.build_absolute_uri(uploaded_file_url)
        img = {
            'images': absolute_file_url
        }
        response = JsonResponse(img)
        return response


def download_files_view(request, pk):
    if request.method == 'GET':
        model_images_list = ProductImage.objects.filter(product__id=pk)
        zip_file_name = transliteration(Product.objects.get(pk=pk).name.replace(' ', '_') + '.zip')
        image_list = []

        for model_image in model_images_list:
            img = model_image.image.open()
            image_list.append((os.path.basename(img.name), img))

        zip_bytes_buffer = BytesIO()
        with zipfile.ZipFile(zip_bytes_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for f in image_list:
                zf.writestr(f[0], f[1].read())

        zip_files = zip_bytes_buffer.getvalue()

        response = HttpResponse(zip_files, content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="{zip_file_name}"'
        return response


def product_list(request):
    if hasattr(request.user, 'employee'):
        employee = getattr(request.user, 'employee')
        if hasattr(employee, 'designer'):
            queryset = Product.objects.filter(designer_id=employee.designer.pk)
            f = ProductFilterForDesigner(request.GET, queryset=queryset)
        elif hasattr(employee, 'manager'):
            queryset = Product.objects.filter(manager_id=employee.manager.pk)
            f = ProductFilterForManager(request.GET, queryset=queryset)
        elif hasattr(employee, 'category') and employee.category:
            employee_category = getattr(employee, 'category')
            queryset = Product.objects.filter(item__category_id=employee_category.id)
            f = ProductFilter(request.GET, queryset=queryset)
    else:
        queryset = Product.objects.all()
        f = ProductFilter(request.GET, queryset=queryset)
    paginator = Paginator(f.qs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'checked/productslist.html', {'filter': f, 'page_obj': page_obj})

##############
# New View test for Product model and form
###########


class LoginView(auth_views.LoginView):
    template_name = 'checked/accounts/login.html'
    authentication_form = UserLoginForm
    redirect_authenticated_user = 'checker:products_list'
    next_page = 'checker:products_list'


# def image_multiple_form_view(request):
#     form_class = TestImageForm
#     template = 'checked/image-multiple-form-view.html'
#     if request.method == 'POST':
#         form = form_class(request.POST, request.FILES)
#
#         if form.is_valid():
#             data = form.cleaned_data
#             print(data)
#     return render(request, template, {"form": form_class()})


class ProductFormView(FormView):
    template_name = 'checked/test_new_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('checker:categories')
    item_id = None

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
            # kwargs['image_form'] = ProductImageForm()
            item = Item.objects.get(pk=kwargs['pk'])
            pages_number = PagesNumber.objects.filter(items__id=item.id)
            kwargs['item_name'] = item.name
            kwargs['pages_number'] = pages_number
            kwargs['item_category'] = item.category

        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        data = self.get_context_data(**kwargs)
        return render(request, self.template_name, data)

    def setup(self, request, *args, **kwargs):
        self.item_id = kwargs['pk']
        return super().setup(request, *args, **kwargs)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.form_class
        kwargs = self.get_form_kwargs()
        kwargs['item_id'] = self.item_id
        kwargs['user'] = self.request.user
        form = form_class(**kwargs)
        return form

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            data = form.cleaned_data
            image_validator = create_validator(data, request)
            image_list = request.FILES.getlist('images')
            if not image_list:
                messages.add_message(request, messages.ERROR, f'Загрузіть зображення')
                data = self.get_context_data(**kwargs)
                return render(request, self.template_name, data)

            product = form.save(commit=False)

            product.item = Item.objects.get(pk=self.item_id)
            product.status = ProductStatus.objects.get(pk=1)

            # Глянути на код і зайнятись рефакторингом
            image_validator(image_list)
            messages_storage = get_messages(request)

            if messages_storage:
                data = self.get_context_data(**kwargs)
                return render(request, self.template_name, data)

            product.save()

            for image in image_list:
                renamed_image = rename_image(image, data['name'], front=True)
                thumbnail = compresing_image(renamed_image)
                # Глянути на метод save в ProductImage, виправити в ньому недоліки
                # Переписати код в Detail View та temaple щоб коректно відображати нові зображення
                # Edit View виправити та її форму
                #
                ProductImage.objects.create(image=renamed_image, thumbnail=thumbnail, product=product)


            # product.front_image = rename_image(data['front_image'], data['name'], front=True)
            # product.back_thumbnail = None
            # product.front_thumbnail = compresing_image(data['front_image'])
            # if data['back_image']:
            #     product.back_image = rename_image(data['back_image'], data['name'])
            #     product.back_thumbnail = compresing_image(data['back_image'])

            if os.path.exists(os.path.join(MEDIA_ROOT, 'tmp_img')):
                path = os.path.join(MEDIA_ROOT, 'tmp_img')
                shutil.rmtree(path)

            return redirect('checker:products_list')

        return render(request, self.template_name, {'form': form})


class ProductDetailView(DetailView):
    model = Product
    template_name = 'checked/product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        kwargs['images'] = ProductImage.objects.filter(product_id=self.object.id)
        return super().get_context_data(**kwargs)


# class MainView(LoginRequiredMixin, TemplateView):
#     login_url = reverse_lazy('checker:login_user')
#     template_name = 'checked/index.html'


class CategoryListView(ListView):
    template_name = 'checked/categories.html'
    context_object_name = 'categoies'
    model = Category


class ItemsListView(ListView):
    template_name = 'checked/items.html'

    def get_queryset(self):
        self.qs = get_list_or_404(Item, category_id=self.kwargs['pk'])
        return self.qs

# class CreateProductView(PermissionRequiredMixin, FormView):
#     template_name = 'checked/alternative_create_project.html'
#     form_class = ItemForm
#     success_url = reverse_lazy('checker:categories')
#     obj = None
#     initial = {}
#
#     permission_required = 'checker.add_product'
#     raise_exception = True
#     permission_denied_message = 'Додавати продукт може тільки менеджер або дизайнер'
#
#     def setup(self, request, *args, **kwargs):
#         self.obj = Item.objects.get(pk=kwargs['pk'])
#         return super().setup(request, *args, **kwargs)
#
#     def get_initial(self):
#         initial = self.initial.copy()
#         initial.update({
#             'item': self.obj.pk
#         })
#         return initial
#
#     def get_form(self, form_class=None):
#         if form_class is None:
#             form_class = self.form_class
#         kwargs = self.get_form_kwargs()
#         kwargs['request'] = self.request
#         form = form_class(**kwargs)
#         add_values_to_fields(self.obj, form, self.kwargs, self.request)
#         return form
#
#     def get_context_data(self, **kwargs):
#         """Insert the form into the context dict."""
#         if "form" not in kwargs:
#             form = self.get_form()
#
#             kwargs['name'] = self.obj.name
#             kwargs['category'] = self.obj.category
#             kwargs["form"] = form
#         return super().get_context_data(**kwargs)
#
#     def get(self, request, *args, **kwargs):
#         data = self.get_context_data(**kwargs)
#         return render(request, self.template_name, data)
#
#     def create_product(self, data):
#         Product.objects.create(
#             name=data['name'],
#             item=Item.objects.get(pk=data['item']),
#             size=ItemSize.objects.get(pk=data['size']),
#             paper=ItemPaper.objects.get(pk=data['paper']),
#             cover=ItemCover.objects.get(pk=data['cover']),
#             description=data['description'],
#             manager=data['manager'],
#             designer=data['designer'],
#             status=data['status'],
#             front_image=data['front_img'],
#             back_image=data['back_img'],
#             front_thumbnail=data['front_thumbnail'],
#             back_thumbnail=data['back_thumbnail'],
#             quantity=data['quantity']
#         )
#
#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         if form.is_valid():
#             data = form.cleaned_data
#             data['front_img'] = rename_image(data['front_img'], data['name'], front=True)
#             data['front_thumbnail'] = compresing_image(data['front_img'])
#             data['back_thumbnail'] = None
#             data['status'] = ProductStatus.objects.get(pk=1)
#             if data['back_img']:
#                 data['back_img'] = rename_image(data['back_img'], data['name'])
#                 data['back_thumbnail'] = compresing_image(data['back_img'])
#
#             if hasattr(self.request.user.employee, 'manager'):
#                 data['manager'] = Manager.objects.get(pk=self.request.user.employee.manager.id)
#                 data['designer'] = Designer.objects.get(pk=data['designer'])
#             elif hasattr(self.request.user.employee, 'designer'):
#                 data['manager'] = Manager.objects.get(pk=data['manager'])
#                 data['designer'] = Designer.objects.get(pk=self.request.user.employee.designer.id)
#
#             self.create_product(data)
#
#             return redirect('checker:products_list')
#
#         return render(request, self.template_name, {'form': form})



# Поправити view можливо віднаслідуватись від ProductFormView та внести зміти в Form можливо теж віднаслідуватись

class DeleteProductView(DeletionMixin, BaseDetailView):
    model = Product
    success_url = reverse_lazy('checker:products_list')

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)






# class UpdateProductView(UpdateView):
#     model = Product
#     form_class = ProductEditForm
#
#     template_name = 'checked/test_new_form.html'
#     # template_name_suffix = '_update_form'
#
#     # def get_context_data(self, **kwargs):
#     #     """Insert the form into the context dict."""
#     #     if "form" not in kwargs:
#     #         kwargs["form"] = self.get_form()
#     #         # product = self.get_object()
#     #         item = self.get_object().item
#     #         pages_number = PagesNumber.objects.filter(items__id=item.id)
#     #         kwargs['item_name'] = item.name
#     #         kwargs['pages_number'] = pages_number
#     #         kwargs['item_category'] = item.category
#     #     super().get_context_data(**kwargs)
#
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         item = self.get_object().item
#         pages_number = PagesNumber.objects.filter(items__id=item.id)
#         images = ProductImage.objects.filter(product_id=self.object.id)
#         res = super().get(request, *args, **kwargs)
#         res.context_data['item_name'] = item.name
#         res.context_data['pages_number'] = pages_number
#         res.context_data['item_category'] = item.category
#         res.context_data['images'] = images
#         return res
#
#     def get_form(self, form_class=None):
#         if form_class is None:
#             form_class = self.form_class
#         kwargs = self.get_form_kwargs()
#         kwargs['user'] = self.request.user
#         form = form_class(**kwargs)
#         return form
#
#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         if form.is_valid():
#             data = form.cleaned_data
#             image_validator = create_validator(data, request)
#             image_list = request.FILES.getlist('images')
#             if not image_list:
#                 messages.add_message(request, messages.ERROR, f'Загрузіть зображення')
#                 data = self.get_context_data(**kwargs)
#                 return render(request, self.template_name, data)
#
#             product = form.save(commit=False)
#
#             product.item = Item.objects.get(pk=self.item_id)
#             product.status = ProductStatus.objects.get(pk=1)
#
#             # Глянути на код і зайнятись рефакторингом
#             image_validator(image_list)
#             messages_storage = get_messages(request)
#
#             if messages_storage:
#                 data = self.get_context_data(**kwargs)
#                 return render(request, self.template_name, data)
#
#             product.save()
#
#             for image in image_list:
#                 renamed_image = rename_image(image, data['name'], front=True)
#                 thumbnail = compresing_image(renamed_image)
#                 # Глянути на метод save в ProductImage, виправити в ньому недоліки
#                 # Переписати код в Detail View та temaple щоб коректно відображати нові зображення
#                 # Edit View виправити та її форму
#                 #
#                 ProductImage.objects.create(image=renamed_image, thumbnail=thumbnail, product=product)
#
#
#             # product.front_image = rename_image(data['front_image'], data['name'], front=True)
#             # product.back_thumbnail = None
#             # product.front_thumbnail = compresing_image(data['front_image'])
#             # if data['back_image']:
#             #     product.back_image = rename_image(data['back_image'], data['name'])
#             #     product.back_thumbnail = compresing_image(data['back_image'])
#
#             if os.path.exists(os.path.join(MEDIA_ROOT, 'tmp_img')):
#                 path = os.path.join(MEDIA_ROOT, 'tmp_img')
#                 shutil.rmtree(path)
#
#             return redirect('checker:products_list')
#
#         return render(request, self.template_name, {'form': form})

    # def post(self, request, *args, **kwargs):
    #     # self.object = self.get_object()
    #     form = self.get_form()
    #     if form.is_valid():
    #         """Якщо зображення замінюється то його попереднє треба видалити
    #         дістати з екземпляра моделі зображення і його шлях та видалити
    #         потім зрозуміти як працювати з зображеннями які були вже загружені,
    #         тобто зробити перевірку якщо зображення не змінювалось то його не трогати
    #         а якщо зображення не змінюється то ми його не трогаємо і не виконуємо компресію
    #         """
    #
    #         data = form.cleaned_data
    #         product = form.save(commit=False)
    #
    #         print(type(data['front_image']))
    #         print(type(data['back_image']))
    #
    #         print(type(data['front_image']) == InMemoryUploadedFile)
    #         print(type(data['back_image']) == InMemoryUploadedFile)
    #
    #         if type(data['front_image']) == InMemoryUploadedFile:
    #             product.front_image = rename_image(data['front_image'], data['name'], front=True)
    #             product.front_thumbnail = compresing_image(data['front_image'])
    #         if type(data['back_image']) == InMemoryUploadedFile:
    #             product.back_image = rename_image(data['back_image'], data['name'])
    #             product.back_thumbnail = compresing_image(data['back_image'])
    #
    #         product.status = ProductStatus.objects.get(pk=1)
    #         # front_image_path = product.front_image.path
    #         product.save()
    #         # if this_product.name != self.name:
    #         #     folder_path = this_product.front_image.path.split('\\')
    #         #     new_folder_path = '\\'.join(folder_path[:-1])
    #         #     this_product.front_image.delete(save=False)
    #         #     this_product.front_thumbnail.delete(save=False)
    #         #     this_product.back_image.delete(save=False)
    #         #     this_product.back_thumbnail.delete(save=False)
    #         #     os.removedirs(new_folder_path)
    #
    #         return redirect('checker:products_list')
    #
    #     return render(request, self.template_name, {'form': form})
