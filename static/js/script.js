const formulario = document.getElementById("formRegistro");

const lista = document.getElementById("listaServicios");
const mensaje = document.getElementById("mensaje");
const spinner = document.getElementById("spinnerCarga");
const contador = document.getElementById("contador");

const nombre = document.getElementById("nombre");
const descripcion = document.getElementById("descripcion");
const categoria = document.getElementById("categoria");

// Arreglo donde se almacenan los servicios
let servicios = [

    {
        nombre: "Ruta Nueva Loja - Comunidades",
        descripcion: "Servicio de transporte para conectar comunidades rurales.",
        categoria: "Bus"
    },

    {
        nombre: "Taxi Rural Seguro",
        descripcion: "Transporte bajo solicitud para usuarios de zonas rurales.",
        categoria: "Taxi"
    }

];

// ======================
// VALIDACIONES
// ======================

function validarNombre() {
    if (nombre.value.trim().length < 4) {
        nombre.classList.add("is-invalid");
        nombre.classList.remove("is-valid");
        return false;
    }

    nombre.classList.remove("is-invalid");
    nombre.classList.add("is-valid");
    return true;
}

function validarDescripcion() {
    if (descripcion.value.trim().length < 10) {
        descripcion.classList.add("is-invalid");
        descripcion.classList.remove("is-valid");
        return false;
    }

    descripcion.classList.remove("is-invalid");
    descripcion.classList.add("is-valid");
    return true;
}

function validarCategoria() {
    if (categoria.value === "") {
        categoria.classList.add("is-invalid");
        categoria.classList.remove("is-valid");
        return false;
    }

    categoria.classList.remove("is-invalid");
    categoria.classList.add("is-valid");
    return true;
}

// Eventos de validación
nombre.addEventListener("input", validarNombre);
descripcion.addEventListener("input", validarDescripcion);
categoria.addEventListener("change", validarCategoria);

// ======================
// MOSTRAR SERVICIOS
// ======================

function mostrarServicios() {

    lista.innerHTML = "";

    //
    if (servicios.length === 0 ) {

        lista.innerHTML = `
            <div class="alert alert-warning">
                No existen servicios registrados.
            </div>
        `;

        contador.textContent = 0;
        return;
    }

    // Estructura repetitiva 
    servicios.forEach((servicio, index) => {

        const tarjeta = document.createElement("div");

        tarjeta.className = "card p-3 mb-3 shadow";

        tarjeta.innerHTML = `
            <h5>${servicio.nombre}</h5>

            <p>${servicio.descripcion}</p>

            <span class="badge bg-primary mb-3">
                ${servicio.categoria}
            </span>

            <button class="btn btn-danger">
                Eliminar
            </button>
        `;

        tarjeta.querySelector("button").addEventListener("click", function () {

            servicios.splice(index, 1);

            mostrarServicios();

        });

        lista.appendChild(tarjeta);

    });

    contador.textContent = servicios.length;

}

// REGISTRAR SERVICIO

formulario.addEventListener("submit", function (e) {

    e.preventDefault();

    spinner.classList.remove("d-none");

    const nombreValido = validarNombre();
    const descripcionValida = validarDescripcion();
    const categoriaValida = validarCategoria();

    if (!nombreValido || !descripcionValida || !categoriaValida) {

        mensaje.innerHTML = `
            <div class="alert alert-danger">
                Corrija los errores antes de registrar.
            </div>
        `;
        spinner.classList.add("d-none");
        return;
    }

   setTimeout(function () {

    servicios.push({

        nombre: nombre.value,

        descripcion: descripcion.value,

        categoria: categoria.value

    });

    spinner.classList.add("d-none");

    mensaje.innerHTML = `
        <div class="alert alert-success">
            Registro agregado correctamente.
        </div>
    `;

    mostrarServicios();

    formulario.reset();

    nombre.classList.remove("is-valid");
    descripcion.classList.remove("is-valid");
    categoria.classList.remove("is-valid");

}, 1500);

});

// Mostrar mensaje al cargar la página
mostrarServicios();