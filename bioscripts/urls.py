
from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('bioscripts', views.index, name='index'),
    # ex: /polls/5/
]
