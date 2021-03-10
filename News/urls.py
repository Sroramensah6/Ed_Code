from django.urls import path

from . import views

app_name = "news"
urlpatterns = [
    path(r'', views.news_view, name='news'),
    path(r'blog', views.blog_view, name='blog'),
    path(r'nav', views.nav, name='nav'),
    path(r'search', views.search_view, name='search'),
    path(r'create', views.post_create_view, name='post-created'),
    path(r'tag/<slug:tag_slug>', views.blog_view, name='post-by-tag'),
    path(r'categories/<slug:category_slug>',
         views.blog_view, name='post-category'),
    path(r'post/<int:newspost_id>', views.post_view, name='post-details'),
    path(r'question/<int:newspost_id>/like',  views.post_view, name='like'),
    path(r'post/<int:newspost_id>/update',
         views.post_update_view, name='post-updated'),
    path(r'post/<int:newspost_id>/delete',
         views.post_delete_view, name='post-deleted'),
]
