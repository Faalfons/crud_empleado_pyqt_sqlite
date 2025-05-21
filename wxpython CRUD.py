import wx
import sqlite3

# Función para conectar a la base de datos y crear la tabla si no existe
def crear_tabla():
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

# Clase principal
class EstudiantesApp(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Gestión de Estudiantes", size=(500, 550))
        self.panel = wx.Panel(self)
        self.inicializar_interfaz()
        crear_tabla()
        self.cargar_estudiantes()

    def inicializar_interfaz(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Campos de texto
        self.txt_documento = wx.TextCtrl(self.panel)
        self.txt_nombre = wx.TextCtrl(self.panel)
        self.txt_fecha = wx.TextCtrl(self.panel)
        self.txt_correo = wx.TextCtrl(self.panel)

        campos = [
            ("Documento:", self.txt_documento),
            ("Nombre:", self.txt_nombre),
            ("Fecha (YYYY-MM-DD):", self.txt_fecha),
            ("Correo:", self.txt_correo)
        ]

        for etiqueta, campo in campos:
            vbox.Add(wx.StaticText(self.panel, label=etiqueta), flag=wx.TOP, border=8)
            vbox.Add(campo, flag=wx.EXPAND | wx.BOTTOM, border=5)

        # Botones
        botones = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_guardar = wx.Button(self.panel, label="Registrar")
        self.btn_modificar = wx.Button(self.panel, label="Actualizar")
        self.btn_borrar = wx.Button(self.panel, label="Eliminar")
        botones.Add(self.btn_guardar, flag=wx.RIGHT, border=5)
        botones.Add(self.btn_modificar, flag=wx.RIGHT, border=5)
        botones.Add(self.btn_borrar, flag=wx.RIGHT, border=5)

        vbox.Add(botones, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        # Área de texto para mostrar la lista
        self.area_lista = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(480, 220))
        vbox.Add(self.area_lista, flag=wx.EXPAND | wx.ALL, border=10)

        self.panel.SetSizer(vbox)

        # Eventos de botones
        self.btn_guardar.Bind(wx.EVT_BUTTON, self.registrar_estudiante)
        self.btn_modificar.Bind(wx.EVT_BUTTON, self.actualizar_estudiante)
        self.btn_borrar.Bind(wx.EVT_BUTTON, self.eliminar_estudiante)

    def limpiar_campos(self):
        self.txt_documento.SetValue("")
        self.txt_nombre.SetValue("")
        self.txt_fecha.SetValue("")
        self.txt_correo.SetValue("")

    def cargar_estudiantes(self):
        conexion = sqlite3.connect("uninproyectos.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM estudiantes")
        estudiantes = cursor.fetchall()
        conexion.close()

        self.area_lista.SetValue("")
        for est in estudiantes:
            self.area_lista.AppendText(f"Documento: {est[0]}, Nombre: {est[1]}, Fecha: {est[2]}, Correo: {est[3]}\n")

    def registrar_estudiante(self, event):
        documento = self.txt_documento.GetValue().strip()
        nombre = self.txt_nombre.GetValue().strip()
        fecha = self.txt_fecha.GetValue().strip()
        correo = self.txt_correo.GetValue().strip()

        if documento and nombre and fecha and correo:
            try:
                conexion = sqlite3.connect("uninproyectos.db")
                cursor = conexion.cursor()
                cursor.execute("INSERT INTO estudiantes (documento, nombre, fecha, correo) VALUES (?, ?, ?, ?)",
                               (documento, nombre, fecha, correo))
                conexion.commit()
                conexion.close()
                wx.MessageBox("¡Estudiante registrado exitosamente!", "Éxito", wx.OK | wx.ICON_INFORMATION)
                self.limpiar_campos()
                self.cargar_estudiantes()
            except sqlite3.IntegrityError:
                wx.MessageBox("Error: Documento o correo ya registrado.", "Error", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox("Por favor llena todos los campos.", "Advertencia", wx.OK | wx.ICON_WARNING)

    def actualizar_estudiante(self, event):
        documento = self.txt_documento.GetValue().strip()
        nombre = self.txt_nombre.GetValue().strip()
        fecha = self.txt_fecha.GetValue().strip()
        correo = self.txt_correo.GetValue().strip()

        if documento:
            conexion = sqlite3.connect("uninproyectos.db")
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE estudiantes SET nombre=?, fecha=?, correo=? WHERE documento=?
            """, (nombre, fecha, correo, documento))
            conexion.commit()
            conexion.close()
            wx.MessageBox("Datos del estudiante actualizados.", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.limpiar_campos()
            self.cargar_estudiantes()
        else:
            wx.MessageBox("Debes ingresar un documento válido.", "Advertencia", wx.OK | wx.ICON_WARNING)

    def eliminar_estudiante(self, event):
        documento = self.txt_documento.GetValue().strip()

        if documento:
            conexion = sqlite3.connect("uninproyectos.db")
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM estudiantes WHERE documento=?", (documento,))
            conexion.commit()
            conexion.close()
            wx.MessageBox("Estudiante eliminado.", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.limpiar_campos()
            self.cargar_estudiantes()
        else:
            wx.MessageBox("Debes ingresar un documento válido.", "Advertencia", wx.OK | wx.ICON_WARNING)

if __name__ == "__main__":
    app = wx.App(False)
    ventana = EstudiantesApp()
    ventana.Show()
    app.MainLoop()