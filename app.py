import os
import sqlite3

from flask import Flask, render_template
from forms import ProductoForm, ClienteForm, ProveedorForm, FacturacionForm


app = Flask(__name__)

app.config["SECRET_KEY"] = "clave-secreta"


# Ubicación de la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATABASE = os.path.join(DATA_DIR, "ferreteria.db")


# Crear la base de datos y la tabla de productos
def crear_base_datos():

    os.makedirs(DATA_DIR, exist_ok=True)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            precio REAL NOT NULL,
            cantidad INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Página de inicio
@app.route("/")
def inicio():

    nombre_sistema = "Ruta Móvil"

    return render_template(
        "index.html",
        nombre_sistema=nombre_sistema
    )


# Productos
@app.route("/productos", methods=["GET", "POST"])
def productos():

    form = ProductoForm()

    # Guardar producto en SQLite
    if form.validate_on_submit():

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO productos
            (nombre, descripcion, precio, cantidad)
            VALUES (?, ?, ?, ?)
        """, (
            form.nombre.data,
            form.descripcion.data,
            form.precio.data,
            form.cantidad.data
        ))

        conn.commit()
        conn.close()

        print("Producto registrado correctamente")
        print("Nombre:", form.nombre.data)
        print("Descripción:", form.descripcion.data)
        print("Precio:", form.precio.data)
        print("Cantidad:", form.cantidad.data)

    # Consultar productos guardados
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre, descripcion, precio, cantidad
        FROM productos
        ORDER BY id DESC
    """)

    productos = cursor.fetchall()

    conn.close()

    return render_template(
        "productos.html",
        productos=productos,
        form=form
    )


# Clientes
@app.route("/clientes", methods=["GET", "POST"])
def clientes():

    form = ClienteForm()

    clientes = [
        {
            "nombre": "María López",
            "telefono": "0991234567",
            "comunidad": "Nueva Loja"
        },
        {
            "nombre": "Juan Pérez",
            "telefono": "0987654321",
            "comunidad": "El Eno"
        },
        {
            "nombre": "Carlos Andrade",
            "telefono": "0976543210",
            "comunidad": "Santa Cecilia"
        }
    ]

    if form.validate_on_submit():

        nuevo_cliente = {
            "nombre": form.nombre.data,
            "telefono": form.telefono.data,
            "comunidad": form.comunidad.data
        }

        clientes.append(nuevo_cliente)

        print("Cliente registrado correctamente")
        print("Nombre:", form.nombre.data)
        print("Teléfono:", form.telefono.data)
        print("Comunidad:", form.comunidad.data)

    return render_template(
        "clientes.html",
        clientes=clientes,
        form=form
    )


# Proveedores
@app.route("/proveedores", methods=["GET", "POST"])
def proveedores():

    form = ProveedorForm()

    proveedores = [
        {
            "nombre": "Cooperativa de Transporte Rural",
            "descripcion": "Proveedor de servicios de buses para las comunidades rurales.",
            "estado": "Activo"
        },
        {
            "nombre": "Servicio de Taxi Rural",
            "descripcion": "Proveedor de transporte personalizado para los usuarios.",
            "estado": "Activo"
        },
        {
            "nombre": "Cooperativa de Mototaxis Rurales",
            "descripcion": "Proveedor de transporte rápido para comunidades rurales.",
            "estado": "Inactivo"
        }
    ]

    if form.validate_on_submit():

        nuevo_proveedor = {
            "nombre": form.nombre.data,
            "descripcion": form.descripcion.data,
            "estado": form.estado.data
        }

        proveedores.append(nuevo_proveedor)

        print("Proveedor registrado correctamente")
        print("Nombre:", form.nombre.data)
        print("Descripción:", form.descripcion.data)
        print("Estado:", form.estado.data)

    return render_template(
        "proveedores.html",
        proveedores=proveedores,
        form=form
    )


# Facturación
@app.route("/facturacion", methods=["GET", "POST"])
def facturacion():

    form = FacturacionForm()

    facturas = [
        {
            "numero": "001-001-000001",
            "cliente": "María López",
            "servicio": "Taxi rural",
            "valor": 5.00
        },
        {
            "numero": "001-001-000002",
            "cliente": "Juan Pérez",
            "servicio": "Bus rural",
            "valor": 2.50
        },
        {
            "numero": "001-001-000003",
            "cliente": "Carlos Andrade",
            "servicio": "Mototaxi",
            "valor": 3.00
        }
    ]

    if form.validate_on_submit():

        nueva_factura = {
            "numero": form.numero.data,
            "cliente": form.cliente.data,
            "servicio": form.servicio.data,
            "valor": form.valor.data
        }

        facturas.append(nueva_factura)

        print("Factura registrada correctamente")
        print("Número:", form.numero.data)
        print("Cliente:", form.cliente.data)
        print("Servicio:", form.servicio.data)
        print("Valor:", form.valor.data)

    return render_template(
        "facturacion.html",
        facturas=facturas,
        form=form
    )


# Iniciar aplicación
if __name__ == "__main__":

    crear_base_datos()

    app.run(debug=True)