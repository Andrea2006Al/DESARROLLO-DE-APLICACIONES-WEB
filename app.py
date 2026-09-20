from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

from conexion import obtener_conexion
from forms import ProductoForm, ClienteForm, ProveedorForm, FacturacionForm


app = Flask(__name__)

app.config["SECRET_KEY"] = "clave-secreta"  


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

    # Guardar producto en MySQL
    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO productos
            (nombre, precio, stock, id_proveedor)
            VALUES (%s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.precio.data,
            form.cantidad.data,
            None
        ))

        conn.commit()
        cursor.close()
        conn.close()

        print("Producto registrado correctamente")

    # Consultar productos guardados
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_producto, nombre, precio, stock, id_proveedor
        FROM productos
        ORDER BY id_producto DESC
    """)

    productos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "productos.html",
        productos=productos,
        form=form
    )

    # Editar producto
@app.route("/productos/editar/<int:id_producto>", methods=["GET", "POST"])
def editar_producto(id_producto):

    form = ProductoForm()

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    # Buscar el producto seleccionado
    cursor.execute("""
        SELECT id_producto, nombre, precio, stock
        FROM productos
        WHERE id_producto = %s
    """, (id_producto,))

    producto = cursor.fetchone()

    cursor.close()
    conn.close()

    if producto is None:
        return "Servicio no encontrado"

    # Cargar los datos actuales en el formulario
    if request.method == "GET":
        form.nombre.data = producto["nombre"]
        form.precio.data = producto["precio"]
        form.cantidad.data = producto["stock"]

    # Actualizar el producto
    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE productos
            SET nombre = %s,
                precio = %s,
                stock = %s
            WHERE id_producto = %s
        """, (
            form.nombre.data,
            form.precio.data,
            form.cantidad.data,
            id_producto
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("productos"))

    return render_template(
        "productos.html",
        form=form,
        productos=[]
    )
    # Eliminar producto
@app.route("/productos/eliminar/<int:id_producto>")
def eliminar_producto(id_producto):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM productos
        WHERE id_producto = %s
    """, (id_producto,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("productos"))

# Clientes
@app.route("/clientes", methods=["GET", "POST"])
def clientes():

    form = ClienteForm()

    # Guardar cliente en MySQL
    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO clientes
            (nombre, cedula, telefono, correo)
            VALUES (%s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.cedula.data,
            form.telefono.data,
            form.correo.data
        ))

        conn.commit()
        cursor.close()
        conn.close()

        print("Cliente registrado correctamente")

    # Consultar clientes guardados
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_cliente, nombre, cedula, telefono, correo
        FROM clientes
        ORDER BY id_cliente DESC
    """)

    clientes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "clientes.html",
        clientes=clientes,
        form=form
    )


# Proveedores
@app.route("/proveedores", methods=["GET", "POST"])
def proveedores():

    form = ProveedorForm()

    # Guardar proveedor en MySQL
    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO proveedores
            (nombre, telefono, correo)
            VALUES (%s, %s, %s)
        """, (
            form.nombre.data,
            form.telefono.data,
            form.correo.data
        ))

        conn.commit()
        cursor.close()
        conn.close()

        print("Proveedor registrado correctamente")

    # Consultar proveedores guardados
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_proveedor, nombre, telefono, correo
        FROM proveedores
        ORDER BY id_proveedor DESC
    """)

    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "proveedores.html",
        proveedores=proveedores,
        form=form
    )
# Facturación
@app.route("/facturacion", methods=["GET", "POST"])
def facturacion():

    form = FacturacionForm()

    # Obtener clientes desde MySQL
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_cliente, nombre
        FROM clientes
        ORDER BY nombre
    """)

    clientes = cursor.fetchall()

    cursor.close()
    conn.close()

    # Cargar clientes en el formulario
    form.cliente.choices = [
        (cliente["id_cliente"], cliente["nombre"])
        for cliente in clientes
    ]

    # Guardar factura en MySQL
    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO facturas
            (id_cliente, fecha, total)
            VALUES (%s, %s, %s)
        """, (
            form.cliente.data,
            form.fecha.data,
            form.total.data
        ))

        conn.commit()
        cursor.close()
        conn.close()

        print("Factura registrada correctamente")
        mensaje = "Factura registrada correctamente."
    # Consultar facturas
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            f.id_factura,
            c.nombre AS cliente,
            f.fecha,
            f.total
        FROM facturas f
        LEFT JOIN clientes c
            ON f.id_cliente = c.id_cliente
        ORDER BY f.id_factura DESC
    """)

    facturas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
    "facturacion.html",
    facturas=facturas,
    form=form,
    mensaje=mensaje if "mensaje" in locals() else None
)   

# Iniciar aplicación
if __name__ == "__main__":

    app.run(debug=True)