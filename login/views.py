from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate


from .forms import loginForm
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
                # return HttpResponseRedirect(reverse("individual:individual_basic"))
            else:
                messages.success(request, (
                    "Username Or Password is incorrect"))
        else:
            return render(request, "login/login.html", {
                'form': form
            })
    return render(request, 'login/login.html', {
        'form': form,
        "title": "Login"
    })
