# backend/models.py (Flask)

class VentasDepartamento:
    def __init__(self, departamento, cantidad_ventas):
        self.departamento = departamento
        self.cantidad_ventas = cantidad_ventas
  
    def to_xml(self):
        # Genera el XML para cada departamento con ventas
        return f"<{self.departamento}><cantidadVentas>{self.cantidad_ventas}</cantidadVentas></{self.departamento}>"
