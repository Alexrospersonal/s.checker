from django.shortcuts import redirect


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    # def process_view(self, request, view_func, *view_args, **view_kwargs):
    #
    #     if not request.user.is_authenticated:
    #         return redirect('checker:login_user')


# def simple_middleware(get_response):
#     # One-time configuration and initialization.
#
#     def middleware(request):
#         # Code to be executed for each request before
#         # the view (and later middleware) are called.
#         if not request.user.is_authenticated:
#             return reverse('checker:login_user')
#         else:
#             response = get_response(request)
#
#         # Code to be executed for each request/response after
#         # the view is called.
#
#         return response
#
#     return middleware
#
