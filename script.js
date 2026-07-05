const formulario = document.getElementById("formRegistro");

const lista = document.getElementById("listaServicios");
const mensaje = document.getElementById("mensaje");
const contador = document.getElementById("contador");

const nombre = document.getElementById("nombre");
const descripcion = document.getElementById("descripcion");
const categoria = document.getElementById("categoria");

let total = 0;

// Validar nombre
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

// Validar descripción
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

// Validar categoría
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

// Eventos en tiempo real
nombre.addEventListener("input", validarNombre);
nombre.addEventListener("blur", validarNombre);

descripcion.addEventListener("input", validarDescripcion);
descripcion.addEventListener("blur", validarDescripcion);

categoria.addEventListener("change", validarCategoria);
categoria.addEventListener("blur", validarCategoria);

// Envío del formulario
formulario.addEventListener("submit", function (e) {

    e.preventDefault();

    const nombreValido = validarNombre();
    const descripcionValida = validarDescripcion();
    const categoriaValida = validarCategoria();

    if (!nombreValido || !descripcionValida || !categoriaValida) {

        mensaje.innerHTML = `
        <div class="alert alert-danger">
            Corrija los errores antes de registrar.
        </div>
        `;

        return;
    }

    mensaje.innerHTML = `
    <div class="alert alert-success">
        Registro agregado correctamente.
    </div>
    `;

    const tarjeta = document.createElement("div");

    tarjeta.className = "card p-3 mb-3 shadow";

    tarjeta.innerHTML = `
        <h5>${nombre.value}</h5>

        <p>${descripcion.value}</p>

        <span class="badge bg-primary mb-3">
            ${categoria.value}
        </span>

        <button class="btn btn-danger">
            Eliminar
        </button>
    `;

    tarjeta.querySelector("button").addEventListener("click", function () {

        tarjeta.remove();

        total--;

        contador.textContent = total;
    });

    lista.appendChild(tarjeta);

    total++;

    contador.textContent = total;

    formulario.reset();

    nombre.classList.remove("is-valid");
    descripcion.classList.remove("is-valid");
    categoria.classList.remove("is-valid");
});