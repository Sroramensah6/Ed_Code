from django.urls import path

from . import views

app_name = "community"
urlpatterns = [
    path(r'comment/<int:questionmodel_id>/rating', views.rating, name='rate'),
    path(r'search', views.search_view, name='search'),
    path(r'support', views.support_view, name='support'),
    path(r'refrence', views.refrencing_view, name='refrence'),
    path(r'questions', views.community_view, name='community'),
    path(r'tag/<slug:tag_slug>', views.community_view, name='tag'),
    path(r'question/<int:questionmodel_id>', views.post_view, name='question'),
    path(r'question/<int:questionmodel_id>/like',  views.post_view, name='like'),
    #     path(r'api/question/<int:questionmodel_id>/like',
    #          views.PostLikeAPIToggle.as_view(), name='like-api'),
    path(r'category/<slug:category_slug>',
         views.community_view, name='category'),
]
