from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def inicio():
    nombre_sistema = "Ruta Móvil"

    return render_template(
        "index.html",
        nombre_sistema=nombre_sistema
    )


@app.route("/productos")
def productos():

    servicios = [
        {
            "nombre": "Bus rural",
            "descripcion": "Servicio de transporte para las comunidades rurales.",
            "disponible": True
        },
        {
            "nombre": "Taxi",
            "descripcion": "Transporte personalizado para los usuarios.",
            "disponible": True
        },
        {
            "nombre": "Mototaxi",
            "descripcion": "Transporte rápido para zonas rurales.",
            "disponible": True
        }
    ]

    return render_template(
        "productos.html",
        servicios=servicios
    )


@app.route("/clientes")
def clientes():

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

    return render_template(
        "clientes.html",
        clientes=clientes
    )


@app.route("/proveedores")
def proveedores():

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

    return render_template(
        "proveedores.html",
        proveedores=proveedores
    )

@app.route("/facturacion")
def facturacion():

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

    return render_template(
        "facturacion.html",
        facturas=facturas
    )
if __name__ == "__main__":
    app.run(debug=True)