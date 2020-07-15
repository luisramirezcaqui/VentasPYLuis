from tkinter import ttk
import tkinter as tk
from tkinter import *

import sqlite3

productos = []
precio_total = 0.0

class Product(tk.Frame):
    db_nombre = 'mi_empresa.db'

    def __init__(self, window):
        self.log = window
        self.log.title('Login')

        login = LabelFrame(self.log, text = 'Login')
        login.grid(row = 1, column = 0, columnspan = 2, pady = 20)

        Label(login, text = 'Usuario: ').grid(row = 0, column = 0)
        self.usuario = Entry(login)
        self.usuario.focus()
        self.usuario.grid(row = 0, column = 1)

        Label(login, text = 'Contraseña: ').grid(row = 1, column = 0)
        self.contrasena = Entry(login)
        self.contrasena.grid(row = 1, column = 1)

        self.error_login = Label(login, text = '', fg = 'red')
        self.error_login.grid(row = 2, column = 0, columnspan = 2, sticky = W + E)

        ttk.Button(text = 'Iniciar Sesion', command = self.login).grid(row = 2, column = 0, sticky = W + E)
        ttk.Button(text = 'Registrate', command = self.sign_up).grid(row = 2, column = 1, sticky = W + E)

    def login(self):
        if len(self.usuario.get()) != 0 and len(self.contrasena.get()) != 0:
            query = 'SELECT * FROM usuario WHERE username = ?'
            usuario = self.busqueda(query, (self.usuario.get(), ))

            if usuario is None:
                self.error_login['text'] = 'Usuario no exite'

            else:
                if usuario[3] == self.contrasena.get():
                    self.error_login['text'] = ''
                    self.inicio()
                else:
                    self.error_login['text'] = 'Contraseña incorrecta'

        else:
            self.error_login['text'] = 'Usuario y/o contraseña está vacio'

    def sign_up(self):
        self.registro = Toplevel()
        self.registro.title('Registro')

        sign = LabelFrame(self.registro, text = 'Registro')
        sign.grid(row = 1, column = 0, columnspan = 2, pady = 20)

        Label(sign, text = 'Usuario: ').grid(row = 0, column = 0)
        self.usuario_sign_up = Entry(sign)
        self.usuario_sign_up.focus()
        self.usuario_sign_up.grid(row = 0, column = 1)

        Label(sign, text = 'Nombre: ').grid(row = 1, column = 0)
        self.nombre_sign_up = Entry(sign)
        self.nombre_sign_up.grid(row = 1, column = 1)

        Label(sign, text = 'Apellido: ').grid(row = 2, column = 0)
        self.apellido_sign_up = Entry(sign)
        self.apellido_sign_up.grid(row = 2, column = 1)

        Label(sign, text = 'Contraseña: ').grid(row = 3, column = 0)
        self.contrasena_sign_up = Entry(sign)
        self.contrasena_sign_up.grid(row = 3, column = 1)

        self.error_sign = Label(sign, text = '', fg = 'red')
        self.error_sign.grid(row = 4, column = 0, columnspan = 2, sticky = W + E)

        ttk.Button(self.registro, text = 'Registrar', command = self.sign_up_funcion).grid(row = 2, column = 0, columnspan = 2, sticky = W + E)

    def sign_up_funcion(self):
        if len(self.usuario_sign_up.get()) != 0 and len(self.nombre_sign_up.get()) != 0 and len(self.apellido_sign_up.get()) != 0 and len(self.contrasena_sign_up.get()) != 0:
            query = 'SELECT * FROM usuario WHERE username = ?'
            usuario = self.busqueda(query, (self.usuario_sign_up.get(), ))

            if usuario is None:
                query = 'INSERT INTO usuario VALUES (?, ?, ?, ?)'
                self.run_query(query, (self.usuario_sign_up.get(), self.nombre_sign_up.get(), self.apellido_sign_up.get(), self.contrasena_sign_up.get()))

                self.registro.destroy()

            else:
                self.error_sign['text'] = 'Usuario ya existe'

        else:
            self.error_sign['text'] = 'Datos incompletos'


    def inicio(self):
        self.wind = Toplevel()
        self.wind.title('Factura Online')

        #Frame Cliente
        cliente = LabelFrame(self.wind, text = 'Datos del Cliente')
        cliente.grid(row = 0, column = 0, pady = 20)

        #Inputs
        Label(cliente, text = 'Razon Social: ').grid(row = 1, column = 0)
        self.cliente = Entry(cliente)
        self.cliente.focus()
        self.cliente.grid(row = 1, column = 1)

        Label(cliente, text = 'RUC: ').grid(row = 2, column = 0)
        self.ruc = Entry(cliente)
        self.ruc.grid(row = 2, column = 1)

        Label(cliente, text = 'Direccion: ').grid(row = 3, column = 0)
        self.direccion = Entry(cliente)
        self.direccion.grid(row = 3, column = 1)

        #Error
        self.error_cliente = Label(cliente, text = '', fg = 'red')
        self.error_cliente.grid(row = 4, column = 0, columnspan = 2, sticky = W + E)

        #Boton
        ttk.Button(cliente, text = 'Buscar empresa', command = self.buscar_ruc).grid(row = 5, column = 0, sticky = W + E)

        ttk.Button(cliente, text = 'Registrar empresa', command = self.registrar_ruc).grid(row = 5, column = 1, sticky = W + E)

        #Frame Productos
        frame = LabelFrame(self.wind, text = 'Ingrese los productos')
        frame.grid(row = 0, column = 1, pady = 20)

        #Inputs
        Label(frame, text = 'Codigo del producto: ').grid(row = 1, column = 0)
        self.id_producto = Entry(frame)
        self.id_producto.grid(row = 1, column = 1)

        Label(frame, text = 'Cantidad: ').grid(row = 2, column = 0)
        self.cantidad = Entry(frame)
        self.cantidad.grid(row = 2, column = 1)

        #Error
        self.error = Label(frame, text = '', fg = 'red')
        self.error.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        #Boton
        ttk.Button(frame, text = 'Registrar compra', command = self.agregar_compra).grid(row = 4, column = 0, sticky = W + E)
        ttk.Button(frame, text = 'Agregar producto', command = self.agregar_producto).grid(row = 4, column = 1, sticky = W + E)

        #Cabeceras
        self.tree = ttk.Treeview(self.wind, height = 10, columns = (1, 2))
        self.tree.grid(row = 5, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Cantidad', anchor = 'center')
        self.tree.heading('#1', text = 'Nombre', anchor = 'center')
        self.tree.heading('#2', text = 'Precio S/.', anchor = 'center')
        self.tree.bind("<Double-1>", self.eliminar)

        #Generar
        ttk.Button(self.wind, text = 'Generar Factura', command = self.generarFactura).grid(row = 6, column = 0)

        #Total
        total = LabelFrame(self.wind, text = 'Total')
        total.grid(row = 6, column = 1, pady = 20)
        self.total = Label(total, text = str(precio_total))
        self.total.grid(row = 3, column = 0, sticky = W + E)

    def run_query(self, query, parametros = ()):
        with sqlite3.connect(self.db_nombre) as conexion:
            cursor = conexion.cursor()
            resultado = cursor.execute(query, parametros)
            conexion.commit()
        return resultado
        
    def busqueda(self, query, parametros = ()):
        with sqlite3.connect(self.db_nombre) as conexion:
            cursor = conexion.cursor()
            cursor.execute(query, parametros)
            resultado = cursor.fetchone()
            cursor.close()
        return resultado

    def buscar_ruc(self):
        if len(self.ruc.get()) != 0:
            query = 'SELECT * FROM empresas WHERE ruc = ?'
            empresa = self.busqueda(query, (self.ruc.get(), ))
            if empresa is None:
                self.error_cliente['fg'] = 'red'
                self.error_cliente['text'] = 'RUC no existe'
            else:
                self.error_cliente['text'] = ''
                self.cliente.delete(0, END)
                self.direccion.delete(0, END)
                self.cliente.insert(END, empresa[1])
                self.direccion.insert(END, empresa[2])
        else:
            self.error_cliente['fg'] = 'red'
            self.error_cliente['text'] = 'RUC esta vacio'


    def registrar_ruc(self):
        if self.validar_cliente():
            query = 'SELECT * FROM empresas WHERE ruc = ?'
            empresa = self.busqueda(query, (self.ruc.get(), ))
            if empresa is None:
                query = 'INSERT INTO empresas VALUES (?, ?, ?)'
                self.run_query(query, (self.ruc.get(), self.cliente.get(), self.direccion.get()))
                self.error_cliente['fg'] = 'green'
                self.error_cliente['text'] = 'Empresa insertada exitosamente'
            else:
                self.error_cliente['fg'] = 'red'
                self.error_cliente['text'] = 'RUC ya existe' 
        else:
            self.error_cliente['fg'] = 'red'
            self.error_cliente['text'] = 'Falta datos'

    def mostrar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for producto in productos:
            self.tree.insert('', 0, text = producto[0], values = (producto[1], producto[3]))

    def validar_producto(self):
        return len(self.id_producto.get()) != 0 and len(self.cantidad.get()) != 0

    def agregar_compra(self):
        if self.validar_producto():
            global precio_total
            query = 'SELECT * FROM product WHERE id = ?'
            producto = self.busqueda(query, (self.id_producto.get(), ))

            if producto is None:
                self.error['text'] = 'No exite producto'
            else:
                total_producto = float(self.cantidad.get()) * float(producto[2])
                productos.append((self.cantidad.get(), producto[1], producto[2], total_producto))
                precio_total += total_producto
                self.id_producto.delete(0, END)
                self.cantidad.delete(0, END)
                self.total['text'] = str(precio_total)
                self.error['text'] = ''
                self.mostrar()
        else:
            self.error['text'] = 'Nombre y/o precio esta vacio'

    def agregar_producto(self):
        self.producto_db = Toplevel()
        self.producto_db.title = "Registrar producto"
        Label(self.producto_db, text = 'ID: ').grid(row = 1, column = 1)
        self.producto_id = Entry(self.producto_db)
        self.producto_id.grid(row = 1, column = 2)

        Label(self.producto_db, text = 'Nombre: ').grid(row = 2, column = 1)
        self.producto_nombre = Entry(self.producto_db)
        self.producto_nombre.grid(row = 2, column = 2)

        Label(self.producto_db, text = 'Precio: ').grid(row = 3, column = 1)
        self.producto_precio = Entry(self.producto_db)
        self.producto_precio.grid(row = 3, column = 2)

        self.producto_error = Label(self.producto_db, text = '', fg = 'red')
        self.producto_error.grid(row = 4, column = 2, columnspan = 2, sticky = W + E)

        ttk.Button(self.producto_db, text = 'Agregar', command = self.agregar_producto_db).grid(row = 5, column = 2, columnspan = 2, sticky = W + E)

    def agregar_producto_db(self):
        if len(self.producto_id.get()) != 0 and len(self.producto_nombre.get()) != 0 and len(self.producto_precio.get()) != 0:
            query = 'SELECT * FROM product WHERE id = ?'
            producto = self.busqueda(query, (self.producto_id.get(), ))

            if producto is None:
                query = 'INSERT INTO product VALUES (?, ?, ?)'
                self.run_query(query, (self.producto_id.get(), self.producto_nombre.get(), self.producto_precio.get()))

                self.producto_id.delete(0, END)
                self.producto_nombre.delete(0, END)
                self.producto_precio.delete(0, END)

                self.producto_error['fg'] = 'green'
                self.producto_error['text'] = 'Producto insertado correctamente'
            else:
                self.producto_error['fg'] = 'red'
                self.producto_error['text'] = 'ID ya existe'
        else:
            self.producto_error['fg'] = 'red'
            self.producto_error['text'] = 'Falta datos'

    def eliminar(self, event):
        global precio_total
        temp_cantidad = self.tree.item(self.tree.selection())['text']
        temp_producto = self.tree.item(self.tree.selection())['values'][0]
        temp_total = self.tree.item(self.tree.selection())['values'][1]
        temp_precio = float(temp_total)/float(temp_cantidad)
        precio_total -= float(temp_total)
        productos.pop(productos.index((temp_cantidad, str(temp_producto), float(temp_precio), float(temp_total))))
        self.total['text'] = str(precio_total)
        self.mostrar()

    def validar_cliente(self):
        return len(self.cliente.get()) != 0 and len(self.ruc.get()) != 0 and len(self.direccion.get()) != 0

    def generarFactura(self):
        if self.validar_cliente():
            global precio_total
            sub_total = round(precio_total/1.18, 2)
            igv = round(precio_total - sub_total, 2)
            self.error_cliente['text'] = ''
            nombre_cliente = self.cliente.get()
            ruc_cliente = self.ruc.get()
            direccion_cliente = self.direccion.get()

            self.factura_wind = Toplevel()
            self.factura_wind.title('Factura')

            #Razon Social
            Label(self.factura_wind, text = 'Razon Social: ').grid(row = 1, column = 1)
            Entry(self.factura_wind, textvariable = StringVar(self.factura_wind, value = nombre_cliente), width = 60, state = 'readonly').grid(row = 1, column = 2)

            #RUC
            Label(self.factura_wind, text = 'R.U.C.: ').grid(row = 2, column = 1)
            Entry(self.factura_wind, textvariable = StringVar(self.factura_wind, value = ruc_cliente), width = 60, state = 'readonly').grid(row = 2, column = 2)

            #DIRECCION
            Label(self.factura_wind, text = 'Direccion: ').grid(row = 3, column = 1)
            Entry(self.factura_wind, textvariable = StringVar(self.factura_wind, value = direccion_cliente), width = 60, state = 'readonly').grid(row = 3, column = 2)
             
            #TREE
            self.factura_wind.tree = ttk.Treeview(self.factura_wind, height = 10, columns = (1, 2, 3))
            self.factura_wind.tree.grid(row = 4, column = 1, columnspan = 2)
            self.factura_wind.tree.heading('#0', text = 'Cantidad', anchor = 'center')
            self.factura_wind.tree.heading('#1', text = 'Descripcion', anchor = 'center')
            self.factura_wind.tree.heading('#2', text = 'Precio Unitario S/.', anchor = 'center')
            self.factura_wind.tree.heading('#3', text = 'Precio Total S/.', anchor = 'center')

            #INSERT
            for producto in productos:
                self.factura_wind.tree.insert('', 0, text = producto[0], values = (producto[1], producto[2], producto[3]))

            #Sub-Total
            Label(self.factura_wind, text = 'Sub-Total: ').grid(row = 5, column = 1)
            Entry(self.factura_wind, textvariable = StringVar(self.factura_wind, value = str(sub_total)), state = 'readonly').grid(row = 5, column = 2)

            #IGV
            Label(self.factura_wind, text = 'IGV (18%): ').grid(row = 6, column = 1)
            Entry(self.factura_wind, textvariable = StringVar(self.factura_wind, value = str(igv)), state = 'readonly').grid(row = 6, column = 2)

            #Total
            Label(self.factura_wind, text = 'Total: ').grid(row = 7, column = 1)
            Entry(self.factura_wind, textvariable = StringVar(self.factura_wind, value = str(precio_total)), state = 'readonly').grid(row = 7, column = 2)

        else:
            self.error_cliente['fg'] = 'red'
            self.error_cliente['text'] = 'Falta datos'

if __name__ == '__main__':
    window = Tk()
    app = Product(window)
    window.mainloop()
