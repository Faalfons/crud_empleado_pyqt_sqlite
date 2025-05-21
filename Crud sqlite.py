import sqlite3

def connect_db():
    return sqlite3.connect("database.db")

def create_table():
    with connect_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL)''')
        conn.commit()

def create_user():
    name = input("Ingrese el nombre: ")
    email = input("Ingrese el email: ")
    with connect_db() as conn:
        conn.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        print("Usuario agregado exitosamente!")

def list_users():
    with connect_db() as conn:
        users = conn.execute("SELECT * FROM users").fetchall()
        for user in users:
            print(f"ID: {user[0]}, Nombre: {user[1]}, Email: {user[2]}")

def update_user():
    user_id = input("Ingrese el ID del usuario a actualizar: ")
    name = input("Nuevo nombre: ")
    email = input("Nuevo email: ")
    with connect_db() as conn:
        conn.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
        conn.commit()
        print("Usuario actualizado exitosamente!")

def delete_user():
    user_id = input("Ingrese el ID del usuario a eliminar: ")
    with connect_db() as conn:
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        print("Usuario eliminado!")

def menu():
    create_table()
    while True:
        print("\n--- MENÚ CRUD ---")
        print("1. Agregar usuario")
        print("2. Listar usuarios")
        print("3. Actualizar usuario")
        print("4. Eliminar usuario")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            create_user()
        elif opcion == "2":
            list_users()
        elif opcion == "3":
            update_user()
        elif opcion == "4":
            delete_user()
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu()