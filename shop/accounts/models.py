from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):

    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('Введите e-mail')
        if not username:
            raise ValueError('Введите имя пользователя')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

    first_name = models.CharField(max_length=50, null=True, verbose_name='Фамилия')
    last_name = models.CharField(max_length=50, null=True, verbose_name='Имя')
    email = models.CharField(max_length=100, null=True, verbose_name='Почта')
    username = models.CharField(max_length=50, unique=True, null=True, verbose_name='Имя пользователя')
    phone_number = models.CharField(max_length=50, null=True, verbose_name='Номер телефона')

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    is_admin = models.BooleanField(default=False, verbose_name='Админ')
    is_staff = models.BooleanField(default=False, verbose_name='Работник')
    is_superadmin = models.BooleanField(default=False, verbose_name='Супер пользователь')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        if self.email:
            return self.email
        else:
            return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class UserProfile(models.Model):

    user = models.OneToOneField(Account, on_delete=models.CASCADE, verbose_name='Пользователь')
    address_line1 = models.CharField(max_length=255, blank=True, verbose_name='Адрес 1')
    address_line2 = models.CharField(max_length=255, blank=True, verbose_name='Адрес 2')
    profile_picture = models.ImageField(blank=True, default='user_profile/default.png',
                                        upload_to='user_profile', verbose_name='Фото')
    city = models.CharField(max_length=100, blank=True, verbose_name='Город')
    state = models.CharField(max_length=100, blank=True, verbose_name='Область')
    country = models.CharField(max_length=100, blank=True, verbose_name='Страна')

    def __str__(self):
        return self.user.first_name

    def full_address(self):
        return f'{self.address_line1} {self.address_line2}'
