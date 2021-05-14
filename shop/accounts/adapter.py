from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from accounts.utils import _profile


class MyAdapter(DefaultSocialAccountAdapter):

    def get_connect_redirect_url(self, request, socialaccount):
        super().get_connect_redirect_url(request, socialaccount)
        _profile(socialaccount)
