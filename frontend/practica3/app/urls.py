from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cargar/', views.cargar, name='cargar'),
    path('resultado/', views.resultado, name='resultado'),
    path('grafico/', views.grafico, name='grafico'),
    path('ayuda/', views.ayuda, name='ayuda')
]