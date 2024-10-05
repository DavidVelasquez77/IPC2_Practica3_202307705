# app/forms.py

from django import forms

class CargarArchivoForm(forms.Form):
    archivo = forms.FileField(label="Seleccione un archivo XML")
