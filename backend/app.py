#app.py
from flask import Flask, request, jsonify, session, render_template, redirect, url_for
import xml.etree.ElementTree as ET
from models import VentasDepartamento 
from collections import defaultdict
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Para manejar sesiones

# Lista de departamentos válidos de Guatemala
DEPARTAMENTOS_VALIDOS = [
    "Guatemala", "Sacatepéquez", "Chimaltenango", "Escuintla", "Santa Rosa", "Jalapa", 
    "Jutiapa", "Baja Verapaz", "Alta Verapaz", "Petén", "Izabal", "Zacapa", "Chiquimula", 
    "El Progreso", "Quiché", "Huehuetenango", "San Marcos", "Quetzaltenango", "Totonicapán", 
    "Sololá", "Suchitepéquez", "Retalhuleu"
]

# Ruta para procesar el archivo XML
@app.route('/cargar', methods=['GET', 'POST'])
def cargar():
    if request.method == 'POST':
        if 'archivo_xml' not in request.files:
            return jsonify({'error': 'No se encontró el archivo XML'}), 400
        
        archivo_xml = request.files['archivo_xml']
        
        try:
            tree = ET.parse(archivo_xml)
            root = tree.getroot()
            ventas_departamentos = defaultdict(int)
            
            # Procesar las ventas
            for venta in root.find('ListadoVentas'):
                departamento = venta.attrib.get('departamento', None)
                if departamento in DEPARTAMENTOS_VALIDOS:
                    ventas_departamentos[departamento] += 1
            
            # Crear la lista de ventas que devolveremos en formato JSON
            lista_ventas = [
                {
                    'departamento': departamento, 
                    'cantidad_ventas': cantidad
                }
                for departamento, cantidad in ventas_departamentos.items()
                if cantidad > 0
            ]
            
            return jsonify(lista_ventas)
        except ET.ParseError:
            return jsonify({'error': 'Error al procesar el archivo XML'}), 400
    
    return jsonify({'error': 'Método no permitido'}), 405


# Ruta para mostrar los resultados
@app.route('/resultado')
def resultado():
    lista_ventas = session.get('lista_ventas', [])
    return render_template('resultado.html', lista_ventas=lista_ventas)

# Generar XML basado en los resultados
@app.route('/generar_xml')
def generar_xml():
    lista_ventas = session.get('lista_ventas', [])
    
    xml_string = '<?xml version="1.0" encoding="UTF-8"?>\n<resultados>\n<departamentos>\n'
    for venta in lista_ventas:
        xml_string += f'    <{venta["departamento"]}>\n'
        xml_string += f'        <cantidadVentas>{venta["cantidad_ventas"]}</cantidadVentas>\n'
        xml_string += f'    </{venta["departamento"]}>\n'
    xml_string += '</departamentos>\n</resultados>'
    
    # Devolver el XML generado
    return app.response_class(xml_string, content_type='application/xml')

# Ruta para mostrar el gráfico
@app.route('/grafico')
def grafico():
    lista_ventas = session.get('lista_ventas', [])
    
    # Preparar datos para el gráfico
    departamentos = [venta['departamento'] for venta in lista_ventas]
    cantidades = [venta['cantidad_ventas'] for venta in lista_ventas]
    
    return render_template('grafico.html', departamentos=json.dumps(departamentos), cantidades=json.dumps(cantidades))

# Ruta para mostrar la página de ayuda
@app.route('/ayuda')
def ayuda():
    estudiante = {
        'nombre': 'Josué David Velasquez Ixchop', 
        'carnet': '202307705',
        'curso': 'Introducción a la Programación y Computacion 2',
        'seccion': 'A',
    }
    
    return render_template('ayuda.html', estudiante=estudiante)

# Página de inicio
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
