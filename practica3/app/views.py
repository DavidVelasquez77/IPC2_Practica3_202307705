from django.shortcuts import render, redirect  # Importar redirect
from django.http import HttpResponse
import xml.etree.ElementTree as ET
from collections import defaultdict
from .models import VentasDepartamento

# Lista de departamentos válidos de Guatemala
DEPARTAMENTOS_VALIDOS = [
    "Guatemala", "Sacatepéquez", "Chimaltenango", "Escuintla", "Santa Rosa", "Jalapa", 
    "Jutiapa", "Baja Verapaz", "Alta Verapaz", "Petén", "Izabal", "Zacapa", "Chiquimula", 
    "El Progreso", "Quiché", "Huehuetenango", "San Marcos", "Quetzaltenango", "Totonicapán", 
    "Sololá", "Suchitepéquez", "Retalhuleu"
]

# Vista para cargar archivo y procesar datos
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

                # Solo contamos departamentos válidos
                if departamento in DEPARTAMENTOS_VALIDOS:
                    ventas_departamentos[departamento] += 1  # Contamos las ventas por departamento

            # Filtramos los departamentos con al menos una venta
            lista_ventas = [
                VentasDepartamento(departamento, ventas) 
                for departamento, ventas in ventas_departamentos.items() 
                if ventas > 0
            ]

            # Almacenar los datos en la sesión para acceso posterior
            request.session['lista_ventas'] = [
                {'departamento': venta.departamento, 'ventas': venta.cantidad_ventas} 
                for venta in lista_ventas
            ]

            # Redirigir a la vista de resultados
            return redirect('resultado')  # Cambiado de render a redirect

        except ET.ParseError:
            return HttpResponse('Error al procesar el archivo XML. Asegúrate de que tiene el formato correcto.')

    return render(request, 'cargar_archivo.html')

# Vista para mostrar el XML de salida
def resultado(request):
    lista_ventas = request.session.get('lista_ventas', [])
    return render(request, 'resultado.html', {'lista_ventas': lista_ventas})

# Vista para mostrar la gráfica
def mostrar_grafico(request):
    lista_ventas = request.session.get('lista_ventas', [])
    departamentos = [venta['departamento'] for venta in lista_ventas]
    cantidades = [venta['ventas'] for venta in lista_ventas]

    return render(request, 'grafico.html', {
        'departamentos': departamentos,
        'cantidades': cantidades,
    })

# Función para generar el XML de salida
def generar_xml(ventas_departamentos):
    """
    Genera el XML de salida basado en los departamentos y las ventas procesadas.
    Solo incluirá departamentos con más de 0 ventas.
    """
    # Creamos la estructura base del XML
    xml_string = '<?xml version="1.0" encoding="UTF-8"?>\n<resultados>\n<departamentos>\n'
    
    # Recorremos cada departamento y sus ventas
    for venta in ventas_departamentos:
        # Aseguramos que solo departamentos con más de 0 ventas se incluyan
        if venta.cantidad_ventas > 0:
            xml_string += f'    <{venta.departamento}>\n'
            xml_string += f'        <cantidadVentas>{venta.cantidad_ventas}</cantidadVentas>\n'
            xml_string += f'    </{venta.departamento}>\n'
    
    # Cerramos las etiquetas de departamentos y resultados
    xml_string += '</departamentos>\n</resultados>'
    
    return xml_string

# Vista de inicio actual
def index(request):
    return render(request, 'index.html')
