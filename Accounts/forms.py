from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


from .models import Profile


class loginForm(AuthenticationForm):

    def __str__(self):
        return self.username

    class Meta:
        model = User
        fields = ('username', 'password')


class SignUpForm(UserCreationForm):
    # name = forms.CharField(max_length=254, required=True)
    email = forms.EmailField(
        max_length=254, required=True, help_text='Required. Inform a valid email address.')

    def __str__(self):
        return self.name

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('email', 'phone_number', 'profile_image',
                  'location', 'company_name')
        exclude = ['user']
