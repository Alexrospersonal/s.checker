from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


class Login(LoginView):
    template_name = 'checked/accounts/login.html'
    next_page = reverse_lazy('checker:main')


# class Logout(LoginView):
#     next_page = reverse_lazy('checker:login_user')