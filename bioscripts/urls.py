
from django.urls import path

from . import views

app_name = 'bioscripts'

urlpatterns = [
    path('', views.index, name='index'),
    path('var2texshade/', views.var2texshade, name='var2texshade'),
    path('var2texshade/<str:hgvsp>', views.var2texshade_api, name='var2texshade_api'),
    path('genesymbolchecker/', views.genesymbolchecker, name='genesymbolchecker'),
    path('genesymbolchecker/<str:label>', views.genesymbolchecker_result, name='genesymbolchecker_result'),
]
