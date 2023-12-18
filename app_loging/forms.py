from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from app_loging.models import User

CHOISES =(
    ("1", "Магазин"),
    ("2", "Покупатель"),
)
class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Логин', required=True, widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}))
    password1 = forms.CharField(label='Пароль', required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
                                help_text='от 8-ми символов', )
    password2 = forms.CharField(label='Повтор пароля', required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Повтор пароля'}))
    type = forms.ChoiceField(choices=CHOISES)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password1", "password2"]


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
