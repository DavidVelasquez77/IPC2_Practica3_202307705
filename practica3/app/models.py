# models.py

class VentasDepartamento:
    def __init__(self, departamento, cantidad_ventas):
        self.departamento = departamento
        self.cantidad_ventas = cantidad_ventas  # Asegúrate de que este nombre es correcto

    def to_xml(self):
        # Genera el XML para cada departamento con ventas
        return f"<{self.departamento}><cantidadVentas>{self.cantidad_ventas}</cantidadVentas></{self.departamento}>"
