from django.urls import path, re_path

from . import views

app_name = 'blog'

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    re_path('(?P<path>.*)/', views.post, name='post'),
    # ex: /polls/5/
]
