
from django.urls import path

from . import views

app_name = 'personal'

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
]
