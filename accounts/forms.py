from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.middleware.csrf import get_token


class CadastroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name', 'password1', 'password2']


class AutenticacaoForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.PasswordInput()
    



        