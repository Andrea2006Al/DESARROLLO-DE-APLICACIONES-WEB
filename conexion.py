import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def obtener_conexion():
    conexion = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    return conexion


if __name__ == "__main__":
    conexion = obtener_conexion()

    if conexion.is_connected():
        print("Conexión exitosa con MySQL")

    conexion.close()