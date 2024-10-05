from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cargar-archivo/', views.cargar_archivo, name='cargar_archivo'),
    path('resultado/', views.resultado, name='resultado'),
    path('grafico/', views.mostrar_grafico, name='mostrar_grafico'),
]
