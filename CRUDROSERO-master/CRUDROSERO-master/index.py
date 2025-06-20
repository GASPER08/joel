from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymongo
from pymongo import errors
from bson.objectid import ObjectId

# Parámetros de conexión a MongoDB
Mongo_Host = "localhost"            
Mongo_Puerto = "27017"
Mongo_Tiempo_Fuera = 1000

Mongo_Uri = f"mongodb://{Mongo_Host}:{Mongo_Puerto}/"
Mongo_Basedatos = "EquipoMamba"
Mongo_colleccion = "Jugadores"

# Conexión a la base de datos
cliente = pymongo.MongoClient(Mongo_Uri, serverSelectionTimeoutMS=Mongo_Tiempo_Fuera)
baseDatos = cliente[Mongo_Basedatos]
coleccion = baseDatos[Mongo_colleccion]

ID_Jugador = ""

def mostrarDatos(nombre="", sexo="", numero=""):
    """
    Muestra en la tabla los jugadores que coincidan con los criterios de búsqueda.
    Si no se pasan parámetros, muestra todos los jugadores.
    """
    objetoBuscar = {}
    if nombre:
        objetoBuscar["Nombre"] = nombre
    if sexo:
        objetoBuscar["Sexo"] = sexo
    if numero:
        objetoBuscar["Numero"] = numero

    try:
        tabla.delete(*tabla.get_children())  # Limpiar tabla antes de actualizarla
        for documento in coleccion.find(objetoBuscar):
            tabla.insert('', 0, text=str(documento["_id"]),
                         values=(documento["Nombre"], documento["Sexo"], documento["Numero"]))
    except errors.ServerSelectionTimeoutError as errorTiempo:
        print("Tiempo excedido:", errorTiempo)
    except errors.ConnectionFailure as errorConexion:
        print("Fallo al conectarse a MongoDB:", errorConexion)

def crearRegistro():
    """
    Crea un nuevo registro de jugador si todos los campos están completos.
    """
    if Nombre.get() and Numero.get() and Sexo.get():
        try:
            documento = {
                "Nombre": Nombre.get(),
                "Numero": Numero.get(),
                "Sexo": Sexo.get()
            }
            coleccion.insert_one(documento)
            print("Documento insertado con éxito")
            mostrarDatos()
            limpiarCampos()
        except errors.ConnectionFailure as error:
            print("Error de conexión:", error)
    else:
        print("Todos los campos son obligatorios")

def dobleClickTabla(event):
    """
    Carga los datos del jugador seleccionado al hacer doble clic en la tabla.
    Permite editar o borrar el registro.
    """
    global ID_Jugador
    seleccion = tabla.selection()
    if not seleccion:
        return

    ID_Jugador = str(tabla.item(seleccion[0])["text"])
    try:
        documento = coleccion.find_one({"_id": ObjectId(ID_Jugador)})

        # Rellenar los campos con los datos seleccionados
        Nombre.delete(0, END)
        Nombre.insert(0, documento["Nombre"])
        Sexo.delete(0, END)
        Sexo.insert(0, documento["Sexo"])
        Numero.delete(0, END)
        Numero.insert(0, documento["Numero"])

        crear["state"] = "disabled"
        editar["state"] = "normal"
        borrar["state"] = "normal"
    except Exception as e:
        print("Error al cargar datos del jugador:", e)

def editarRegistro():
    """
    Edita el registro del jugador actualmente seleccionado.
    """
    global ID_Jugador
    if Nombre.get() and Sexo.get() and Numero.get():
        try:
            idBuscar = {"_id": ObjectId(ID_Jugador)}
            nuevosValores = {
                "Nombre": Nombre.get(),
                "Sexo": Sexo.get(),
                "Numero": Numero.get()
            }
            coleccion.update_one(idBuscar, {"$set": nuevosValores})
            print("Documento actualizado con éxito")
            mostrarDatos()
            limpiarCampos()
        except errors.ConnectionFailure as error:
            print("Error de conexión:", error)
    else:
        print("Los campos no pueden estar vacíos")

    crear["state"] = "normal"
    editar["state"] = "disabled"
    borrar["state"] = "disabled"

def borrarRegistro():
    """
    Borra el registro del jugador actualmente seleccionado.
    """
    global ID_Jugador
    try:
        idBuscar = {"_id": ObjectId(ID_Jugador)}
        coleccion.delete_one(idBuscar)
        print("Documento eliminado con éxito")
        limpiarCampos()
        mostrarDatos()
    except errors.ConnectionFailure as error:
        print("Error de conexión:", error)

    crear["state"] = "normal"
    editar["state"] = "disabled"
    borrar["state"] = "disabled"

def limpiarCampos():
    """
    Limpia los campos de entrada del formulario principal.
    """
    Nombre.delete(0, END)
    Sexo.delete(0, END)
    Numero.delete(0, END)

def buscarRegistro():
    """
    Ejecuta la búsqueda de jugadores en base a los criterios introducidos.
    """
    mostrarDatos(buscarNombre.get(), buscarSexo.get(), buscarNumero.get())

# GUI principal
ventana = Tk()
ventana.title("CRUD Jugadores")
ventana.geometry("500x500")

# Tabla para mostrar registros
tabla = ttk.Treeview(ventana, columns=(1, 2, 3))
tabla.grid(row=1, column=0, columnspan=3, sticky=W+E)
tabla.heading("#0", text="ID")
tabla.heading("#1", text="Nombre")
tabla.heading("#2", text="Sexo")
tabla.heading("#3", text="Numero")
tabla.bind("<Double-Button-1>", dobleClickTabla)

# Entradas principales
Label(ventana, text="Nombre").grid(row=2, column=0, sticky=W)
Nombre = Entry(ventana)
Nombre.grid(row=2, column=1, sticky=W+E)

Label(ventana, text="Sexo").grid(row=3, column=0, sticky=W)
Sexo = Entry(ventana)
Sexo.grid(row=3, column=1, sticky=W+E)

Label(ventana, text="Numero").grid(row=4, column=0, sticky=W)
Numero = Entry(ventana)
Numero.grid(row=4, column=1, sticky=W+E)

# Botones CRUD
crear = Button(ventana, text="Crear nuevo jugador", command=crearRegistro, bg="purple", fg="white")
crear.grid(row=5, columnspan=3, sticky=W+E)

editar = Button(ventana, text="Editar Jugador", command=editarRegistro, bg="orange")
editar.grid(row=6, columnspan=3, sticky=W+E)
editar["state"] = "disabled"

borrar = Button(ventana, text="Borrar Jugador", command=borrarRegistro, bg="pink", fg="white")
borrar.grid(row=7, columnspan=3, sticky=W+E)
borrar["state"] = "disabled"

# Entradas búsqueda
Label(ventana, text="Buscar por nombre").grid(row=8, column=0, sticky=W)
buscarNombre = Entry(ventana)
buscarNombre.grid(row=8, column=1, sticky=W+E)

Label(ventana, text="Buscar por sexo").grid(row=9, column=0, sticky=W)
buscarSexo = Entry(ventana)
buscarSexo.grid(row=9, column=1, sticky=W+E)

Label(ventana, text="Buscar por número").grid(row=10, column=0, sticky=W)
buscarNumero = Entry(ventana)
buscarNumero.grid(row=10, column=1, sticky=W+E)

buscar = Button(ventana, text="Buscar jugador", command=buscarRegistro, bg="blue", fg="white")
buscar.grid(row=11, columnspan=3, sticky=W+E)

# Mostrar datos al iniciar
mostrarDatos()
ventana.mainloop()
