from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class loginForm(AuthenticationForm):

    def __str__(self):
        return self.username

    class Meta:
        model = User
        fields = ('username', 'password')
