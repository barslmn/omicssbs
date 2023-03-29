
from django.urls import path

from . import views

app_name = 'personal'

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('cv_html', views.cv_html, name='cv_html'),
    # ex: /polls/5/
]
