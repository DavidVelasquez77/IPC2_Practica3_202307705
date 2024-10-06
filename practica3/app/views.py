from django.shortcuts import render, redirect
from django.http import HttpResponse
import xml.etree.ElementTree as ET
from collections import defaultdict
import json

# Lista de los 22 departamentos válidos de Guatemala
DEPARTAMENTOS_VALIDOS = [
    "Guatemala", "Sacatepéquez", "Chimaltenango", "Escuintla", "Santa Rosa", "Jalapa", 
    "Jutiapa", "Baja Verapaz", "Alta Verapaz", "Petén", "Izabal", "Zacapa", "Chiquimula", 
    "El Progreso", "Quiché", "Huehuetenango", "San Marcos", "Quetzaltenango", "Totonicapán", 
    "Sololá", "Suchitepéquez", "Retalhuleu"
]

def cargar(request):
    if request.method == 'POST' and request.FILES['archivo_xml']:
        archivo_xml = request.FILES['archivo_xml']
        
        try:
            tree = ET.parse(archivo_xml)
            root = tree.getroot()
            ventas_departamentos = defaultdict(int)
            
            for venta in root.find('ListadoVentas'):
                departamento = venta.attrib.get('departamento', None)
                if departamento in DEPARTAMENTOS_VALIDOS:
                    ventas_departamentos[departamento] += 1
            
            # Asegúrate de usar la estructura correcta
            request.session['lista_ventas'] = [
                {
                    'departamento': departamento, 
                    'cantidad_ventas': cantidad
                }
                for departamento, cantidad in ventas_departamentos.items()
                if cantidad > 0
            ]
            
            return redirect('resultado')
        except ET.ParseError:
            return HttpResponse('Error al procesar el archivo XML. Asegúrate de que tiene el formato correcto.')
    
    return render(request, 'cargar.html')

# 2. Actualizar la función generar_xml
def generar_xml(lista_ventas):
    xml_string = '<?xml version="1.0" encoding="UTF-8"?>\n<resultados>\n<departamentos>\n'
    
    for venta in lista_ventas:
        xml_string += f'    <{venta["departamento"]}>\n'
        xml_string += f'        <cantidadVentas>{venta["cantidad_ventas"]}</cantidadVentas>\n'
        xml_string += f'    </{venta["departamento"]}>\n'
    
    xml_string += '</departamentos>\n</resultados>'
    return xml_string
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
        'curso': 'Introducción a la Programación y Computacion 2',
        'seccion': 'A',
    }
    
    return render(request, 'ayuda.html', {'estudiante': estudiante})


def index(request):
    return render(request, 'index.html')
