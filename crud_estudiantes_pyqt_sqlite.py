import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
)

def conectar_bd():
    conexion = sqlite3.connect("uninproyectos.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estudiantes (
            documento TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            fecha TEXT NOT NULL,
            correo TEXT UNIQUE NOT NULL,
            edad INTEGER NOT NULL
        )
    """)
    cursor.execute("ALTER TABLE estudiantes ADD COLUMN edad TEXT NOT NULL DEFAULT '0'")
    conexion.commit()
    conexion.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD de Estudiantes")
        self.setGeometry(100, 100, 500, 500)
        self.init_ui()
        conectar_bd()
        self.listar()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        self.entry_doc = QLineEdit()
        self.entry_nombre = QLineEdit()
        self.entry_fecha = QLineEdit()
        self.entry_correo = QLineEdit()
        self.entry_edad = QLineEdit()

        layout.addWidget(QLabel("Documento identificacion:"))
        layout.addWidget(self.entry_doc)
        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.entry_nombre)
        layout.addWidget(QLabel("Fecha (dd-mm-aaaa):"))
        layout.addWidget(self.entry_fecha)
        layout.addWidget(QLabel("Correo:"))
        layout.addWidget(self.entry_correo)
        layout.addWidget(QLabel("Edad:"))
        layout.addWidget(self.entry_edad)

        btn_layout = QHBoxLayout()
        btn_registrar = QPushButton("Registrar")
        btn_actualizar = QPushButton("Actualizar")
        btn_eliminar = QPushButton("Eliminar")
        btn_listar = QPushButton("Listar")
        btn_layout.addWidget(btn_registrar)
        btn_layout.addWidget(btn_actualizar)
        btn_layout.addWidget(btn_eliminar)
        btn_layout.addWidget(btn_listar)
        layout.addLayout(btn_layout)

        self.text_lista = QTextEdit()
        self.text_lista.setReadOnly(True)
        layout.addWidget(self.text_lista)

        central_widget.setLayout(layout)

        btn_registrar.clicked.connect(self.insertar)
        btn_actualizar.clicked.connect(self.actualizar)
        btn_eliminar.clicked.connect(self.eliminar)
        btn_listar.clicked.connect(self.listar)

    def insertar(self):
        documento = self.entry_doc.text()
        nombre = self.entry_nombre.text()
        fecha = self.entry_fecha.text()
        correo = self.entry_correo.text()
        edad = self.entry_edad.text()
        if documento and nombre and fecha and correo and edad:
            try:
                conexion = sqlite3.connect("uninproyectos.db")
                cursor = conexion.cursor()
                cursor.execute("INSERT INTO estudiantes VALUES (?, ?, ?, ?, ?)",
                               (documento, nombre, fecha, correo, edad))
                conexion.commit()
                conexion.close()
                QMessageBox.information(self, "Éxito", "Estudiante registrado correctamente")
                self.listar()
            except sqlite3.IntegrityError:
                QMessageBox.critical(self, "Error", "Documento o correo ya registrados")
        else:
            QMessageBox.warning(self, "Atención", "Todos los campos son obligatorios")

    def listar(self):
        conexion = sqlite3.connect("uninproyectos.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM estudiantes")
        registros = cursor.fetchall()
        conexion.close()
        self.text_lista.clear()
        for estudiante in registros:
            self.text_lista.append(str(estudiante))

    def actualizar(self):
        documento = self.entry_doc.text()
        nombre = self.entry_nombre.text()
        fecha = self.entry_fecha.text()
        correo = self.entry_correo.text()
        edad = self.entry_edad.text()
        if documento:
            conexion = sqlite3.connect("uninproyectos.db")
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE estudiantes 
                SET nombre=?, fecha=?, correo=?, edad=?
                WHERE documento=?
            """, (nombre, fecha, correo, edad, documento))
            conexion.commit()
            conexion.close()
            QMessageBox.information(self, "Éxito", "Estudiante actualizado")
            self.listar()
        else:
            QMessageBox.warning(self, "Atención", "Ingresa un documento válido")

    def eliminar(self):
        documento = self.entry_doc.text()
        if documento:
            conexion = sqlite3.connect("uninproyectos.db")
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM estudiantes WHERE documento=?", (documento,))
            conexion.commit()
            conexion.close()
            QMessageBox.information(self, "Éxito", "Estudiante eliminado")
            self.listar()
        else:
            QMessageBox.warning(self, "Atención", "Ingresa un documento válido")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())