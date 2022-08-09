from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

username_validator = UnicodeUsernameValidator()

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label=_('Adınız'),max_length=12, min_length=4, required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label=_('Soyadınız'),max_length=12, min_length=4, required=True,
                               widget=(forms.TextInput(attrs={'class': 'form-control'})))
    email = forms.EmailField(label=_('Email Adresiniz'),max_length=50, help_text='Geçerli bir email adresi yazınız.',
                             widget=(forms.TextInput(attrs={'class': 'form-control'})))
    password1 = forms.CharField(label=_('Şifre'),
                                widget=(forms.PasswordInput(attrs={'class': 'form-control'})),
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label=_('Şifre Tekrar'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    username = forms.CharField(
        label=_('Kullanıcı Adınız'),
        max_length=150,
        help_text=_('150 karakter veya daha az olmalıdır. Yalnızca harfler, rakamlar ve @/./+/-/_. kullanabilirsiniz.'),
        validators=[username_validator],
        error_messages={'unique': _("Bir kullanıcı bu ismi zaten kulanıyor.")},
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)