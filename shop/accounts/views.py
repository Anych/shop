from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from accounts.forms import RegistrationForm, UserForm, UserProfileForm
from accounts.models import Account, UserProfile
from accounts.utils import _confirm_email, _profile, _redirect_to_next_page
from cart.utils import _move_cart_when_authenticate
from orders.models import Order


class RegisterView(View):

    def get(self, request, *args, **kwargs):
        """
        Render the register template
        """
        form = RegistrationForm()
        context = {
            'form': form,
        }
        return render(request, 'accounts/register.html', context)

    def post(self, request, *args, **kwargs):
        """
        Register for new user and after create profile
        for him and sending email. Try to move his cart
        items to new cart.
        """
        form = RegistrationForm(request.POST or None)

        if form.is_valid():
            # create new user
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email
            user = Account.objects.create_user(first_name=first_name, last_name=last_name,
                                               email=email, username=username, password=password)
            user.phone_number = phone_number

            # create profile for user and save him
            _profile(user)
            user.save()

            # email confirmation
            _confirm_email(user, email)

            user = auth.authenticate(request=request, username=email, password=password)

            # login user and move his cart
            if user is not None:
                _move_cart_when_authenticate(request, user)
                auth.login(request, user)
                return redirect('store')
        context = {'form': form}
        return render(request, 'accounts/register.html', context)


class LoginView(View):

    def get(self, request, *args, **kwargs):
        """
        Render the login template
        """
        return render(request, 'accounts/login.html')

    def post(self, request, *args, **kwargs):
        """
        Authentication and authorization code,
        gets email and password, if authentication
        success tried to redirect to 'next' page
        and move a cart to authorized user
        """
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(request=request, username=email, password=password)

        # login user and move his cart
        if user is not None:
            _move_cart_when_authenticate(request, user)
            auth.login(request, user)
            try:
                _redirect_to_next_page(request)
            except:
                return redirect('store')

        else:
            messages.error(request, 'Неправильно введена почта или пароль')
            return redirect('login')


class LogoutView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        """
        Logout view, only for has already logged in users
        """
        auth.logout(request)
        messages.success(request, 'Вы успешно вышли из системы')
        return redirect('login')


def confirm_email(request):
    user = request.user
    if request.method == 'POST':
        email = request.POST['email']
        _confirm_email(user, email)
        return redirect('/accounts/login/?command=activate&email=' + email)
    elif user.email:
        _confirm_email(user, user.email)
        return render(request, 'accounts/confirm_email.html')
    else:
        return render(request, 'accounts/confirm_email.html')


def activate(request, uidb64, token, email):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.email = email
        user.was_confirm_email = True
        user.save()
        messages.success(request, 'Поздравляем, Вы успешно подтвердили свою почту!')
        return redirect('checkout')
    else:
        messages.error(request, 'Ошибка активации!')
        return redirect('confirm_email')


@login_required(login_url='login')
def dashboard(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except Exception:
        _profile(user)
        user_profile = UserProfile.objects.get(user=user)

    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    if request.method == 'POST':

        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваши данные успешно обновлены!')
            return redirect('dashboard')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    context = {
        'orders': orders,
        'orders_count': orders_count,
        'user_form': user_form,
        'profile_form': profile_form,
        'user_profile': user_profile,
    }
    return render(request, 'accounts/dashboard.html', context)


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(username=email).exists():
            user = Account.objects.get(email__exact=email)

            mail_subject = 'Восстановление пароля'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Письмо с инструкцией отправлено на вашу почту')
            return redirect('login')
        else:
            messages.error(request, 'Пользователь с такой почтой не зарегистрирован!')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Пожалуйста сбросьте Ваш пароль')
        return redirect('resetPassword')
    else:
        messages.error(request, 'Ссылка устарела')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Пароль успешно сброшен!')
            return redirect('login')

        else:
            messages.error(request, 'Пароли не совпадают')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Ваш пароль успешно обновлён!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Текущий пароль введен не правильно.')
                return redirect('dashboard')
        else:
            messages.error(request, 'Введенные пароли не совпадают.')
            return redirect('dashboard')


@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)
