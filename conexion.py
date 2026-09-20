import mysql.connector


def obtener_conexion():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="lady123",
        database="proyecto_integrador"
    )

    return conexion


if __name__ == "__main__":
    conexion = obtener_conexion()

    if conexion.is_connected():
        print("Conexión exitosa con MySQL")

    conexion.close()