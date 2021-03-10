from django.contrib import admin

from .models import NewsPost, PostView, Categories


admin.site.register(Categories)
admin.site.register(NewsPost)
admin.site.register(PostView)
