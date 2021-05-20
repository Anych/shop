from django.contrib import messages
from django.contrib.sites import requests
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from axes.helpers import get_cache_timeout

from accounts.models import UserProfile


def _profile(user):
    """
    Create an User Profile
    """
    profile = UserProfile()
    profile.user_id = user.id
    profile.save()


def _confirm_email(user, email):
    """
    Confirm email for shopping
    """
    mail_subject = 'Активация аккаунта'
    message = render_to_string('accounts/account_verification_email.html', {
        'user': user,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'email': email,
    })
    to_email = email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()


def axes_disabled(request, credentials, *args, **kwargs):
    """
    Disable users who tried many attempts for authorization
    """
    messages.error(request, f'Слишком много неправильных попыток входа, попробуйте через {get_cache_timeout()} секунд')
    return redirect('login')


def redirect_to_next_page(request):
    """
    Redirect users to 'next' page
    when they were redirect to login page
    """
    url = request.META.get('HTTP_REFERER')
    query = requests.utils.urlparse(url).query
    params = dict(x.split('=') for x in query.split('&'))
    if 'next' in params:
        nextPage = params['next']
        return redirect(nextPage)
