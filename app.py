from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from conexion import obtener_conexion
from forms import ProductoForm, ClienteForm, ProveedorForm, FacturacionForm, UsuarioForm, LoginForm
from models import Usuario

app = Flask(__name__)
app.config["SECRET_KEY"] = "clave-secreta"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, usuario, password
        FROM usuarios
        WHERE id = %s
    """, (user_id,))

    datos = cursor.fetchone()

    cursor.close()
    conn.close()

    if datos:
        return Usuario(
            datos["id"],
            datos["usuario"],
            datos["password"]
        )

    return None

# Página de inicio
@app.route("/")
@login_required
def inicio():

    nombre_sistema = "Ruta Móvil"

    return render_template(
        "index.html",
        nombre_sistema=nombre_sistema
    )

    # Panel principal
@app.route("/dashboard")
@login_required
def dashboard():

    return render_template("dashboard.html")

# Registro de usuarios
@app.route("/registro", methods=["GET", "POST"])
def registro():

    form = UsuarioForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        # Proteger la contraseña antes de guardarla
        password_hash = generate_password_hash(form.password.data)

        cursor.execute("""
            INSERT INTO usuarios (usuario, password)
            VALUES (%s, %s)
        """, (
            form.usuario.data,
            password_hash
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("login"))

    return render_template(
        "registro.html",
        form=form
    )

# Login de usuarios
@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()
    mensaje = None

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, usuario, password
            FROM usuarios
            WHERE usuario = %s
        """, (form.usuario.data,))

        datos = cursor.fetchone()

        cursor.close()
        conn.close()

        if datos and check_password_hash(
            datos["password"],
            form.password.data
        ):

            usuario = Usuario(
                datos["id"],
                datos["usuario"],
                datos["password"]
            )

            login_user(usuario)

            return redirect(url_for("dashboard"))

        mensaje = "Usuario o contraseña incorrectos."

    return render_template(
        "login.html",
        form=form,
        mensaje=mensaje
    )

        
# Productos
@app.route("/productos", methods=["GET", "POST"])
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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

# Cerrar sesión
@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))

# Iniciar aplicación
if __name__ == "__main__":

    app.run(debug=True)