# views.py

from django.shortcuts import render
from django.http import HttpResponse
import xml.etree.ElementTree as ET
from collections import defaultdict
from .models import VentasDepartamento

def cargar_archivo(request):
    if request.method == 'POST' and request.FILES['archivo_xml']:
        archivo_xml = request.FILES['archivo_xml']

        try:
            # Parseamos el archivo XML de entrada
            tree = ET.parse(archivo_xml)
            root = tree.getroot()
            ventas_departamentos = defaultdict(int)  # Para contar las ventas por departamento

            # Procesamos las ventas del archivo XML
            for venta in root.find('ListadoVentas'):
                departamento = venta.attrib['departamento']
                ventas_departamentos[departamento] += 1  # Contamos las ventas por departamento

            # Filtramos los departamentos con al menos una venta
            lista_ventas = [
                VentasDepartamento(departamento, ventas) 
                for departamento, ventas in ventas_departamentos.items() 
                if ventas > 0
            ]

            # Renderizamos el XML de salida en la vista
            return render(request, 'resultado.html', {'lista_ventas': lista_ventas})

        except ET.ParseError:
            return HttpResponse('Error al procesar el archivo XML. Asegúrate de que tiene el formato correcto.')
    
    return render(request, 'cargar_archivo.html')


def generar_xml(ventas_departamentos):
    """
    Genera el XML de salida basado en los departamentos y las ventas procesadas.
    """
    xml_string = '<?xml version="1.0" encoding="UTF-8"?>\n<resultados>\n<departamentos>\n'
    for venta in ventas_departamentos:
        xml_string += venta.to_xml() + '\n'
    xml_string += '</departamentos>\n</resultados>'
    return xml_string



# Vista de inicio actual
def index(request):
    return render(request, 'index.html')
