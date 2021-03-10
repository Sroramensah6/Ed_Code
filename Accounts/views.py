from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.contrib.auth.models import Group
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.sites.shortcuts import get_current_site

from .forms import loginForm, SignUpForm, ProfileForm

from utils.tokens.tokens import account_activation_token
from utils.decorators.decorators import unauthenticated_user


@unauthenticated_user
def loginPage_view(request):
    form = loginForm()
    if request.method == "POST":
        form = loginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # After submitting to the form you'll be redirected to the home page
                return HttpResponseRedirect(reverse("individual:payecal"))
            else:
                messages.success(request, (
                    "Username Or Password is incorrect"))
        else:
            return render(request, "accounts/login/login.html", {
                'form': form
            })
    return render(request, 'accounts/login/login.html', {
        'form': form,
        "title": "Login"
    })


def activation_sent_view(request):
    context = {
        'title': 'Activation link sent!'
    }
    return render(request, 'accounts/activations/activation_sent.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse("individual:payecal"))
    else:
        return render(request, 'accounts/activations/activation_invalid.html')


@unauthenticated_user
def signup_view(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.email = form.cleaned_data['email']
            # user can't login until link confirmed
            user.is_active = False
            user.save()
            use_group = Group.objects.get(name='individual')
            user.groups.add(use_group)
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            # load a template like get_template()
            # and calls its render() method immediately.
            message = render_to_string('accounts/activations/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return HttpResponseRedirect(reverse("accounts:activation_sent"))
        else:
            return render(request, "accounts/signup/signup.html", {
                'form': form
            })
    return render(request, 'accounts/signup/signup.html', {
        'form': form,
        "title": "Signup",
        "header": "Create An Account"
    })


@login_required(login_url="accounts:login")
def update_profile_view(request):
    profile = request.user.profile
    profile_form = ProfileForm(instance=profile)
    if request.method == 'POST':
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, (
                'Your profile was successfully updated!'))
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        profile_form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile/profile.html', {
        'profile_form': profile_form,
        'title': f'{request.user}\'s profile settings'
    })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("accounts:login"))
