from django.shortcuts import render
from django.views import View


class BaseView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'shop/index.html', {})


class PageNotFoundView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'shop/404.html')


class PermissionDeniedView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'shop/403.html')


class PrivacyPolicyView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'shop/privacy.html', {})


class TermsView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'shop/terms.html', {})


class AboutUs(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'shop/about_us.html', {})
