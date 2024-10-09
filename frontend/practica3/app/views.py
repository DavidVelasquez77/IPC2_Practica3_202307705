#views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests  # Para hacer solicitudes HTTP a Flask
from django.conf import settings  # Para manejar variables globales como la URL de Flask
import json

# URL del servidor de Flask
FLASK_API_URL = 'http://127.0.0.1:5000' 

def cargar(request):
    if request.method == 'POST' and request.FILES['archivo_xml']:
        archivo_xml = request.FILES['archivo_xml']

        try:
            files = {'archivo_xml': archivo_xml}
            response = requests.post(f"{FLASK_API_URL}/cargar", files=files)
            
            if response.status_code == 200:
                # Guardar los resultados devueltos por Flask en la sesión
                request.session['lista_ventas'] = response.json()
                return redirect('resultado')
            else:
                return HttpResponse(f"Error en el servidor Flask: {response.status_code}")
        except Exception as e:
            return HttpResponse(f"Error al comunicar con Flask: {str(e)}")
    
    return render(request, 'cargar.html')


def resultado(request):
    lista_ventas = request.session.get('lista_ventas', [])
    return render(request, 'resultado.html', {'lista_ventas': lista_ventas})

def grafico(request):
    lista_ventas = request.session.get('lista_ventas', [])
    
    # Preparar datos para el gráfico
    departamentos = [venta['departamento'] for venta in lista_ventas]
    cantidades = [venta['cantidad_ventas'] for venta in lista_ventas]
    
    context = {
        'departamentos': json.dumps(departamentos),
        'cantidades': json.dumps(cantidades)
    }
    
    return render(request, 'grafico.html', context)

def ayuda(request):
    estudiante = {
        'nombre': 'Josué David Velasquez Ixchop', 
        'carnet': '202307705',
        'curso': 'Introducción a la Programación y Computación 2',
        'seccion': 'A',
    }
    
    return render(request, 'ayuda.html', {'estudiante': estudiante})

def index(request):
    return render(request, 'index.html')
