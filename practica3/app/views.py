# views.py

from django.shortcuts import render
from django.http import HttpResponse
import xml.etree.ElementTree as ET

def cargar_archivo(request):
    if request.method == 'POST' and request.FILES['archivo_xml']:
        archivo_xml = request.FILES['archivo_xml']
        
        # Procesar el archivo XML
        try:
            tree = ET.parse(archivo_xml)
            root = tree.getroot()
            ventas_departamentos = {}

            # Recorrer el XML para contar ventas por departamento
            for venta in root.find('ListadoVentas'):
                departamento = venta.attrib['departamento']
                if departamento in ventas_departamentos:
                    ventas_departamentos[departamento] += 1
                else:
                    ventas_departamentos[departamento] = 1

            # Renderizar resultados
            return render(request, 'resultado.html', {'ventas_departamentos': ventas_departamentos})

        except ET.ParseError:
            return HttpResponse('Error al procesar el archivo XML. Asegúrate de que tiene el formato correcto.')
    
    return render(request, 'cargar_archivo.html')


# Vista de inicio actual
def index(request):
    return render(request, 'index.html')
