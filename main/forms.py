from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Contact
import datetime
from django.utils.timezone import now


class ContactForm(forms.ModelForm):
    selected_date = forms.DateField(

        initial=format(datetime.date.today(), '%Y-%m-%d'),
        label="Дата обратной связи",
        localize=True,
        widget=forms.widgets.DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date',
                   'placeholder': 'Ваше имя',
                   'min': now().strftime('%Y-%m-%d'),
                   })
    )

    name = forms.CharField(
        min_length=2,
        label="Имя",
        widget=forms.TextInput(
            attrs={'placeholder': 'Ваше имя *'}
        )
    )

    phone_number = forms.IntegerField(
        label="Номер телефона",
        widget=forms.TextInput(
            attrs={'placeholder': 'Контактный телефон *'}
        )
    )
    telegram = forms.CharField(
        label="Ник в Telegram",
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Ник в Telegram (необяз.)'}
        )
    )

    class Meta:
        model = Contact
        fields = ["id", "name", "phone_number", "telegram", "selected_date"]


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Логин', required=True, widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}))
    password1 = forms.CharField(label='Пароль', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Повтор пароля', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Повтор пароля'}))


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
