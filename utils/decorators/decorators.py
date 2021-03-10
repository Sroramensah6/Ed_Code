from django.urls import reverse
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("individual:payecal"))
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def individual_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'individual' or group == None:
            return view_func(request, *args, **kwargs)

    return wrapper_func
