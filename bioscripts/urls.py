
from django.urls import path

from . import views

app_name = 'bioscripts'

urlpatterns = [
    path('', views.index, name='index'),
    path('var2texshade/', views.var2texshade, name='var2texshade'),
    path('var2texshade/<str:hgvsp>', views.var2texshade_api, name='var2texshade_api'),
    path('crosssymbolchecker/', views.crosssymbolchecker, name='crosssymbolchecker'),
    path('crosssymbolchecker/<str:label>', views.crosssymbolchecker_result, name='crosssymbolchecker_result'),
]
