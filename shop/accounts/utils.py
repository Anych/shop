from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from accounts.models import UserProfile


def _profile(user):
    profile = UserProfile()
    profile.user_id = user.id
    profile.save()


def _confirm_email(request, user, email):
    mail_subject = 'Активация аккаунта'
    current_site = get_current_site(request)
    message = render_to_string('accounts/account_verification_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'email': email,
    })
    to_email = email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
