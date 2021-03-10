# from django import template
# from ..models import List
# from ..forms import ListForm
# from django.contrib import messages
# from django.shortcuts import render


# register = template.Library()


# @register.inclusion_tag('link.html', takes_context=True)
# def jump_link(context, request):

#     form = TodoListForm()

#     if request.method == 'POST':
#         form = TodoListForm(request.POST or None)
#         if form.is_valid():
#             form.save()
#             user = request.user.username.capitalize()
#             messages.success(request, f'{user}, has added a list!')
#     return {
#         'form': context[form],
#     }
