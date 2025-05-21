import sqlite3

def crear_base_datos():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    # Crear tabla si no existe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        edad INTEGER NOT NULL
    )
    ''')

    # Cerrar la conexión
    conn.commit()
    conn.close()

# Llamamos a la función para crear la base de datos y la tabla
crear_base_datos()
import tkinter as tk
from tkinter import messagebox
import sqlite3

# Funciones CRUD
def crear_usuario(nombre, edad):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (nombre, edad) VALUES (?, ?)', (nombre, edad))
    conn.commit()
    conn.close()

def obtener_usuarios():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def actualizar_usuario(id, nombre, edad):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE usuarios SET nombre = ?, edad = ? WHERE id = ?', (nombre, edad, id))
    conn.commit()
    conn.close()

def eliminar_usuario(id):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# Funciones para actualizar la lista en la interfaz
def cargar_usuarios():
    for widget in frame_lista.winfo_children():
        widget.destroy()

    usuarios = obtener_usuarios()
    for usuario in usuarios:
        tk.Label(frame_lista, text=f'{usuario[0]} | {usuario[1]} | {usuario[2]}').pack()

# Funciones de la interfaz
def agregar_usuario():
    nombre = entry_nombre.get()
    edad = entry_edad.get()

    if not nombre or not edad.isdigit():
        messagebox.showerror('Error', 'Por favor ingrese un nombre y una edad válida.')
        return

    crear_usuario(nombre, int(edad))
    cargar_usuarios()

def eliminar():
    try:
        id_usuario = int(entry_id.get())
        eliminar_usuario(id_usuario)
        cargar_usuarios()
    except ValueError:
        messagebox.showerror('Error', 'Por favor ingrese un ID válido.')

def actualizar():
    try:
        id_usuario = int(entry_id.get())
        nombre = entry_nombre.get()
        edad = entry_edad.get()

        if not nombre or not edad.isdigit():
            messagebox.showerror('Error', 'Por favor ingrese un nombre y una edad válida.')
            return

        actualizar_usuario(id_usuario, nombre, int(edad))
        cargar_usuarios()
    except ValueError:
        messagebox.showerror('Error', 'Por favor ingrese un ID válido.')

# Interfaz de Tkinter
ventana = tk.Tk()
ventana.title("CRUD de Usuarios")

# Frame para la entrada de datos
frame_entrada = tk.Frame(ventana)
frame_entrada.pack(padx=10, pady=10)

tk.Label(frame_entrada, text="ID:").grid(row=0, column=0, padx=5, pady=5)
entry_id = tk.Entry(frame_entrada)
entry_id.grid(row=0, column=1)

tk.Label(frame_entrada, text="Nombre:").grid(row=1, column=0, padx=5, pady=5)
entry_nombre = tk.Entry(frame_entrada)
entry_nombre.grid(row=1, column=1)

tk.Label(frame_entrada, text="Edad:").grid(row=2, column=0, padx=5, pady=5)
entry_edad = tk.Entry(frame_entrada)
entry_edad.grid(row=2, column=1)

# Botones
btn_agregar = tk.Button(frame_entrada, text="Agregar Usuario", command=agregar_usuario)
btn_agregar.grid(row=3, column=0, padx=5, pady=5)

btn_actualizar = tk.Button(frame_entrada, text="Actualizar Usuario", command=actualizar)
btn_actualizar.grid(row=3, column=1, padx=5, pady=5)

btn_eliminar = tk.Button(frame_entrada, text="Eliminar Usuario", command=eliminar)
btn_eliminar.grid(row=4, column=0, columnspan=2, pady=10)

# Frame para la lista de usuarios
frame_lista = tk.Frame(ventana)
frame_lista.pack(padx=10, pady=10)

# Cargar usuarios al iniciar
cargar_usuarios()

ventana.mainloop()
