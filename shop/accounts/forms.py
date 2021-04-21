from django import forms

from accounts.models import Account, UserProfile


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите Имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите Фамилию'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Введите телефон'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите почту'

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Подтвердите пароль',
    }))

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        email = self.cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')

    def clean_email(self):
        email = self.cleaned_data['email']
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError('Данный почтовый ящик уже зарегестрирован в системе')
        return email


class UserForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('address_line1', 'address_line2', 'city', 'state', 'country', 'profile_picture')

    profile_picture = forms.ImageField(required=False, error_messages={'Ошибка': "Можно загружать только картинки"},
                                       widget=forms.FileInput)