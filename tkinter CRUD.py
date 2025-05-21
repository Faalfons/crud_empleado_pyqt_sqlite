import sqlite3
import tkinter as tk
from tkinter import messagebox

def conectar_bd():
    conexion = sqlite3.connect("uninproyectos.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estudiantes (
            documento TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            fecha TEXT NOT NULL,
            correo TEXT UNIQUE NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

def insertar():
    documento = entry_doc.get()
    nombre = entry_nombre.get()
    fecha = entry_fecha.get()
    correo = entry_correo.get()

    if documento and nombre and fecha and correo:
        try:
            conexion = sqlite3.connect("uninproyectos.db")
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO estudiantes VALUES (?, ?, ?, ?)", 
                           (documento, nombre, fecha, correo))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Estudiante registrado correctamente")
            listar()  # Actualiza la lista
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Documento o correo ya registrados")
    else:
        messagebox.showwarning("Atención", "Todos los campos son obligatorios")

def listar():
    conexion = sqlite3.connect("uninproyectos.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM estudiantes")
    registros = cursor.fetchall()
    conexion.close()

    text_lista.delete("1.0", tk.END)  
    for estudiante in registros:
        text_lista.insert(tk.END, f"{estudiante}\n")

def actualizar():
    documento = entry_doc.get()
    nombre = entry_nombre.get()
    fecha = entry_fecha.get()
    correo = entry_correo.get()

    if documento:
        conexion = sqlite3.connect("uninproyectos.db")
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE estudiantes 
            SET nombre=?, fecha=?, correo=?
            WHERE documento=?
        """, (nombre, fecha, correo, documento))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Estudiante actualizado")
        listar()
    else:
        messagebox.showwarning("Atención", "Ingresa un documento válido")

def eliminar():
    documento = entry_doc.get()
    if documento:
        conexion = sqlite3.connect("uninproyectos.db")
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM estudiantes WHERE documento=?", (documento,))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Estudiante eliminado")
        listar()
    else:
        messagebox.showwarning("Atención", "Ingresa un documento válido")

root = tk.Tk()
root.title("CRUD de Estudiantes")
root.geometry("500x500")

tk.Label(root, text="Documento:").pack(pady=(10, 0))
entry_doc = tk.Entry(root)
entry_doc.pack(pady=(0, 10))

tk.Label(root, text="Nombre:").pack()
entry_nombre = tk.Entry(root)
entry_nombre.pack(pady=(0, 10))

tk.Label(root, text="Fecha (YYYY-MM-DD):").pack()
entry_fecha = tk.Entry(root)
entry_fecha.pack(pady=(0, 10))

tk.Label(root, text="Correo:").pack()
entry_correo = tk.Entry(root)
entry_correo.pack(pady=(0, 10))

tk.Button(root, text="Registrar", command=insertar).pack(pady=5)
tk.Button(root, text="Actualizar", command=actualizar).pack(pady=5)
tk.Button(root, text="Eliminar", command=eliminar).pack(pady=5)
tk.Button(root, text="Listar", command=listar).pack(pady=5)

text_lista = tk.Text(root, height=10, width=50)
text_lista.pack(pady=10)

conectar_bd()

root.mainloop()
