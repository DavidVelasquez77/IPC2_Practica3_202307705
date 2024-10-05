from django.shortcuts import render
from .forms import CargarArchivoForm
import xml.etree.ElementTree as ET

# Vista para cargar el archivo XML
def cargar_archivo(request):
    mensaje = ""
    if request.method == "POST":
        form = CargarArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            try:
                # Procesar el archivo XML
                tree = ET.parse(archivo)
                root = tree.getroot()

                # Aquí puedes realizar más operaciones con el XML,
                # como revisar los departamentos y ventas
                mensaje = "Archivo cargado y procesado correctamente."
            except ET.ParseError:
                mensaje = "Error al procesar el archivo XML."

    else:
        form = CargarArchivoForm()

    return render(request, 'cargar_archivo.html', {'form': form, 'mensaje': mensaje})

# Vista de inicio actual
def index(request):
    return render(request, 'index.html')
