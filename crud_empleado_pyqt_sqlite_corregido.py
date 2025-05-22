import sys 
import sqlite3 #Prueba 2025-05-21
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
)
import os

DB_PATH = os.path.join(os.getcwd(), "uninproyectos.db")

def conectar_bd():
    # Si no existe la base de datos, crearla con la tabla completa
    conexion = sqlite3.connect(DB_PATH)
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD Empleados")
        self.setGeometry(100, 100, 500, 500)
        self.init_ui()
        conectar_bd()
        self.listar()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Campos
        self.entry_doc = QLineEdit()
        self.entry_nombre = QLineEdit()
        self.entry_fecha = QLineEdit()
        self.entry_correo = QLineEdit()

        layout.addWidget(QLabel("Documento:"))
        layout.addWidget(self.entry_doc)
        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.entry_nombre)
        layout.addWidget(QLabel("Fecha (YYYY-MM-DD):"))
        layout.addWidget(self.entry_fecha)
        layout.addWidget(QLabel("Correo:"))
        layout.addWidget(self.entry_correo)
        
        # Botones
        botones = QHBoxLayout()
        btn_registrar = QPushButton("Registrar")
        btn_actualizar = QPushButton("Actualizar")
        btn_eliminar = QPushButton("Eliminar")
        btn_listar = QPushButton("Listar")
        
        botones.addWidget(btn_registrar)
        botones.addWidget(btn_actualizar)
        botones.addWidget(btn_eliminar)
        botones.addWidget(btn_listar)
        layout.addLayout(botones)
        
        # Texto
        self.text_lista = QTextEdit()
        self.text_lista.setReadOnly(True)
        layout.addWidget(self.text_lista)
        
        central_widget.setLayout(layout)
        
        # Conexión eventos
        btn_registrar.clicked.connect(self.insertar)
        btn_actualizar.clicked.connect(self.actualizar)
        btn_eliminar.clicked.connect(self.eliminar)
        btn_listar.clicked.connect(self.listar)

    def insertar(self):
        doc = self.entry_doc.text()
        nombre = self.entry_nombre.text()
        fecha = self.entry_fecha.text()
        correo = self.entry_correo.text()
        
        if doc and nombre and fecha and correo:
            try:
                con = sqlite3.connect(DB_PATH)
                cur = con.cursor()
                cur.execute("INSERT INTO estudiantes VALUES (?, ?, ?, ?)", (doc, nombre, fecha, correo))
                con.commit()
                con.close()
                QMessageBox.information(self, "Éxito", "Estudiante registrado.")
                self.listar()
            except sqlite3.IntegrityError:
                QMessageBox.critical(self, "Error", "Documento o correo ya registrado.")
        else:
            QMessageBox.warning(self, "Atención", "Todos los campos son obligatorios.")
            
    def listar(self):
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("SELECT * FROM estudiantes")
        registros = cur.fetchall()
        con.close()
        self.text_lista.clear()
        for r in registros:
            self.text_lista.append(str(r))
    
    def actualizar(self):
        doc = self.entry_doc.text()
        nombre = self.entry_nombre.text()
        fecha = self.entry_fecha.text()
        correo = self.entry_correo.text()
        
        if doc:
            con = sqlite3.connect(DB_PATH)
            cur = con.cursor()
            cur.execute("""
                UPDATE estudiantes 
                SET nombre=?, fecha=?, correo=?
                WHERE documento=?
            """, (nombre, fecha, correo, doc))
            con.commit()
            con.close()
            QMessageBox.information(self, "Actualizado", "Datos actualizados.")
            self.listar()
        else:
            QMessageBox.warning(self, "Atención", "Documento requerido.")
    
    def eliminar(self):
        doc = self.entry_doc.text()
        if doc:
            con = sqlite3.connect(DB_PATH)
            cur = con.cursor()
            cur.execute("DELETE FROM estudiantes WHERE documento=?", (doc,))
            con.commit()
            if cur.rowcount == 0:
                QMessageBox.warning(self, "Error", "No se encontró el estudiante.")
            else:
                QMessageBox.information(self, "Eliminado", "Estudiante eliminado.")
            con.close()
            self.listar()
        else:
            QMessageBox.warning(self, "Atención", "Documento requerido.")
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    