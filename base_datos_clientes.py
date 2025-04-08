from cliente import Cliente

class BaseDatosClientes:
    def __init__(self):
        self.clientes = []

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)

    def eliminar_cliente(self, cliente):
        self.clientes.remove(cliente)

    def obtener_clientes(self):
        return self.clientes
