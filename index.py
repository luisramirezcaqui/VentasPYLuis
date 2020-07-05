from tkinter import ttk
import tkinter as tk
from tkinter import *

productos = []
precio_total = 0

class Product:
    def __init__(self, window):
        self.wind = window
        self.wind.title('Factura Online')

        #Frame Cliente
        cliente = LabelFrame(self.wind, text = 'Datos del Cliente')
        cliente.grid(row = 0, column = 0, pady = 20)

        #Inputs
        Label(cliente, text = 'Nombre: ').grid(row = 1, column = 0)
        self.cliente = Entry(cliente)
        self.cliente.focus()
        self.cliente.grid(row = 1, column = 1)

        Label(cliente, text = 'RUC: ').grid(row = 2, column = 0)
        self.ruc = Entry(cliente)
        self.ruc.grid(row = 2, column = 1)

        #Error
        self.error_cliente = Label(cliente, text = '', fg = 'red')
        self.error_cliente.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        #Frame Productos
        frame = LabelFrame(self.wind, text = 'Ingrese los productos')
        frame.grid(row = 0, column = 1, pady = 20)

        #Inputs
        Label(frame, text = 'Nombre: ').grid(row = 1, column = 0)
        self.nombre = Entry(frame)
        self.nombre.grid(row = 1, column = 1)

        Label(frame, text = 'Precio: ').grid(row = 2, column = 0)
        self.precio = Entry(frame)
        self.precio.grid(row = 2, column = 1)

        #Error
        self.error = Label(frame, text = '', fg = 'red')
        self.error.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        #Boton
        ttk.Button(frame, text = 'Registrar', command = self.agregar).grid(row = 4, columnspan = 2, sticky = W + E)

        #Cabeceras
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 5, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Nombre', anchor = 'center')
        self.tree.heading('#1', text = 'Precio S/.', anchor = 'center')
        self.tree.bind("<Double-1>", self.eliminar)

        #Generar
        ttk.Button(text = 'Generar Factura', command = self.generarFactura).grid(row = 6, column = 0)

        #Total
        total = LabelFrame(self.wind, text = 'Total')
        total.grid(row = 6, column = 1, pady = 20)
        self.total = Label(total, text = str(precio_total))
        self.total.grid(row = 3, column = 0, sticky = W + E)

    def mostrar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for producto in productos:
            self.tree.insert('', 0, text = producto[0], values = producto[1])

    def validar_producto(self):
        return len(self.nombre.get()) != 0 and len(self.precio.get()) != 0

    def agregar(self):
        if self.validar_producto():
            global precio_total
            productos.append((self.nombre.get(), self.precio.get()))
            precio_total += float(self.precio.get())
            self.nombre.delete(0, END)
            self.precio.delete(0, END)
            self.total['text'] = str(precio_total)
            self.error['text'] = ''
            self.mostrar()
        else:
            self.error['text'] = 'Nombre y/o precio esta vacio'

    def eliminar(self, event):
        global precio_total
        temp_text = self.tree.item(self.tree.selection())['text']
        temp_value = self.tree.item(self.tree.selection())['values'][0]
        precio_total -= float(temp_value)
        productos.pop(productos.index((temp_text, str(temp_value))))
        self.total['text'] = str(precio_total)
        self.mostrar()

    def validar_cliente(self):
        return len(self.cliente.get()) != 0 and len(self.ruc.get()) != 0

    def generarFactura(self):
        if self.validar_cliente():
            global precio_total
            sub_total = round(precio_total/1.18, 2)
            igv = round(precio_total - sub_total, 2)
            self.error_cliente['text'] = ''
            nombre_cliente = self.cliente.get()
            ruc_cliente = self.ruc.get()

            self.factura_wind = Toplevel()
            self.factura_wind.title = "Factura"

            #Razon Social
            Label(self.factura_wind, text = 'Razon Social: ').grid(row = 1, column = 1)
            Entry(self.factura_wind, textvariable = StringVar(self.factura_wind, value = nombre_cliente), state = 'readonly').grid(row = 1, column = 2)

            #RUC
            Label(self.factura_wind, text = 'R.U.C.: ').grid(row = 2, column = 1)
            Entry(self.factura_wind, textvariable = StringVar(self.factura_wind, value = ruc_cliente), state = 'readonly').grid(row = 2, column = 2)
             
            #TREE
            self.factura_wind.tree = ttk.Treeview(self.factura_wind, height = 10, columns = 2)
            self.factura_wind.tree.grid(row = 3, column = 1, columnspan = 2)
            self.factura_wind.tree.heading('#0', text = 'Descripcion', anchor = 'center')
            self.factura_wind.tree.heading('#1', text = 'Precio S/.', anchor = 'center')

            #INSERT
            for producto in productos:
                self.factura_wind.tree.insert('', 0, text = producto[0], values = producto[1])

            #Sub-Total
            Label(self.factura_wind, text = 'Sub-Total: ').grid(row = 4, column = 1)
            Entry(self.factura_wind, textvariable = StringVar(self.factura_wind, value = str(sub_total)), state = 'readonly').grid(row = 4, column = 2)

            #IGV
            Label(self.factura_wind, text = 'IGV (18%): ').grid(row = 5, column = 1)
            Entry(self.factura_wind, textvariable = StringVar(self.factura_wind, value = str(igv)), state = 'readonly').grid(row = 5, column = 2)

            #Total
            Label(self.factura_wind, text = 'Total: ').grid(row = 6, column = 1)
            Entry(self.factura_wind, textvariable = StringVar(self.factura_wind, value = str(precio_total)), state = 'readonly').grid(row = 6, column = 2)

        else:
            self.error_cliente['text'] = 'Nombre y/o RUC esta vacio'

if __name__ == '__main__':
    window = Tk()
    app = Product(window)
    window.mainloop()
