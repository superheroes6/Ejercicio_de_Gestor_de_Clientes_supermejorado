import tkinter as tk
from tkinter import ttk
from base_datos_clientes import BaseDatosClientes
from cliente import Cliente

class Aplicacion:
    def __init__(self, master):
        self.master = master
        master.title("Gestor de Clientes")

        self.base_datos = BaseDatosClientes()

        self.tree = ttk.Treeview(master)
        self.tree["columns"] = ("NIF", "Nombre", "Dirección", "Teléfono", "Correo", "VIP")
        self.tree.column("#0", width=0, stretch=tk.NO)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)

        self.tree.pack()

        self.frame_formulario = tk.Frame(master)
        self.frame_formulario.pack()

        self.etiquetas = ["NIF", "Nombre", "Dirección", "Teléfono", "Correo", "VIP"]
        self.entradas = {}

        for etiqueta in self.etiquetas:
            fila = tk.Frame(self.frame_formulario)
            fila.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

            tk.Label(fila, text=etiqueta, width=15).pack(side=tk.LEFT)
            entrada = tk.Entry(fila)
            entrada.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

            self.entradas[etiqueta.lower()] = entrada

        self.boton_agregar = tk.Button(master, text="Agregar Cliente", command=self.agregar_cliente)
        self.boton_agregar.pack()

        self.boton_eliminar = tk.Button(master, text="Eliminar Cliente", command=self.eliminar_cliente)
        self.boton_eliminar.pack()

    def agregar_cliente(self):
        datos = {clave: entrada.get() for clave, entrada in self.entradas.items()}
        vip = datos["vip"].lower() == "si"
        cliente = Cliente(datos["nif"], datos["nombre"], datos["dirección"], datos["teléfono"], datos["correo"], vip)
        self.base_datos.agregar_cliente(cliente)
        self.actualizar_treeview()

    def eliminar_cliente(self):
        seleccion = self.tree.selection()
        if seleccion:
            item = seleccion[0]
            valores = self.tree.item(item, "values")
            for cliente in self.base_datos.obtener_clientes():
                if cliente.nif == valores[0]:
                    self.base_datos.eliminar_cliente(cliente)
                    break
            self.actualizar_treeview()

    def actualizar_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for cliente in self.base_datos.obtener_clientes():
            self.tree.insert("", "end", values=(cliente.nif, cliente.nombre, cliente.direccion,
                                                cliente.telefono, cliente.correo_electronico,
                                                "Sí" if cliente.vip else "No"))
