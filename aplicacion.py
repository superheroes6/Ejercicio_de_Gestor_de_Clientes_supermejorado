import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import Clientes

class Aplicacion:
    def __init__(self, master):
        self.master = master
        master.title("Gestor de Clientes")

        self.base_datos = Clientes

        # Configuración del Treeview para mostrar los clientes
        self.tree = ttk.Treeview(master)
        self.tree["columns"] = ("NIF", "Nombre", "Apellido")
        self.tree.column("#0", width=0, stretch=tk.NO)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)

        self.tree.pack(pady=10)

        # Botones para las acciones principales
        self.boton_añadir = tk.Button(master, text="Añadir Cliente", command=self.abrir_formulario_añadir)
        self.boton_añadir.pack(pady=5)

        self.boton_borrar = tk.Button(master, text="Borrar Cliente", command=self.borrar_cliente)
        self.boton_borrar.pack(pady=5)

        self.boton_modificar = tk.Button(master, text="Modificar Cliente", command=self.abrir_formulario_modificar)
        self.boton_modificar.pack(pady=5)

        self.boton_mostrar = tk.Button(master, text="Mostrar Base de Datos", command=self.listar_clientes)
        self.boton_mostrar.pack(pady=5)

        self.actualizar_treeview()

    def listar_clientes(self):
        self.actualizar_treeview()

    def abrir_formulario_añadir(self):
        self.abrir_formulario("Añadir Cliente", self.base_datos.crear)

    def abrir_formulario_modificar(self):
        dni = self.pedir_dni("Modificar Cliente")
        if dni:
            cliente = self.base_datos.buscar(dni)
            if cliente:
                self.abrir_formulario("Modificar Cliente", lambda d, n, a: self.base_datos.modificar(d, n, a), cliente)
            else:
                messagebox.showwarning("No Encontrado", "Cliente no encontrado.")

    def borrar_cliente(self):
        dni = self.pedir_dni("Borrar Cliente")
        if dni:
            if self.base_datos.borrar(dni):
                messagebox.showinfo("Éxito", "Cliente borrado correctamente.")
                self.actualizar_treeview()
            else:
                messagebox.showwarning("No Encontrado", "Cliente no encontrado.")

    def abrir_formulario(self, titulo, accion, cliente=None):
        formulario = tk.Toplevel(self.master)
        formulario.title(titulo)

        if cliente is None:  # Mostrar el campo DNI solo al añadir un cliente
            tk.Label(formulario, text="DNI:").grid(row=0, column=0, padx=10, pady=5)
            entrada_dni = tk.Entry(formulario)
            entrada_dni.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(formulario, text="Nombre:").grid(row=1 if cliente is None else 0, column=0, padx=10, pady=5)
        entrada_nombre = tk.Entry(formulario)
        entrada_nombre.grid(row=1 if cliente is None else 0, column=1, padx=10, pady=5)
        entrada_nombre.insert(0, cliente.nombre if cliente else "")

        tk.Label(formulario, text="Apellido:").grid(row=2 if cliente is None else 1, column=0, padx=10, pady=5)
        entrada_apellido = tk.Entry(formulario)
        entrada_apellido.grid(row=2 if cliente is None else 1, column=1, padx=10, pady=5)
        entrada_apellido.insert(0, cliente.apellido if cliente else "")

        def guardar():
            if cliente is None:  # Añadir cliente
                dni = entrada_dni.get()
                if not dni:
                    messagebox.showwarning("Campos Vacíos", "El campo DNI es obligatorio.")
                    return
            else:
                dni = cliente.dni  # Usar el DNI existente al modificar

            nombre = entrada_nombre.get()
            apellido = entrada_apellido.get()
            if nombre and apellido:
                accion(dni, nombre, apellido)  # Pasar DNI, nombre y apellido
                self.actualizar_treeview()
                formulario.destroy()
            else:
                messagebox.showwarning("Campos Vacíos", "Por favor, completa todos los campos.")

        tk.Button(formulario, text="Guardar", command=guardar).grid(row=3 if cliente is None else 2, column=0, columnspan=2, pady=10)

    def pedir_dni(self, titulo):
        dni = simpledialog.askstring(titulo, "Introduce el DNI del cliente:")
        return dni.upper() if dni else None

    def actualizar_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for cliente in self.base_datos.lista:
            self.tree.insert("", "end", values=(cliente.dni, cliente.nombre, cliente.apellido))

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()