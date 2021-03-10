from django.urls import path

from . import views

app_name = "comment"
urlpatterns = [
    path(r'<int:comment_id>', views.comment_thread, name='thread'),
    path(r'<int:comment_id>/delete', views.comment_thread_delete, name='delete'),
]
