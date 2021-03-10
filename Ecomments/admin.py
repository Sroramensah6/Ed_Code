from django.contrib import admin

from .models import Comment


# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('user', 'parent', 'post', 'content', 'time_reply')


admin.site.register(Comment)
