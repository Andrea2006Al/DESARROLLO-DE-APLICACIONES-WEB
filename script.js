const formulario = document.getElementById("formRegistro");

const lista = document.getElementById("listaServicios");

const mensaje = document.getElementById("mensaje");

const contador = document.getElementById("contador");

let total = 0;

formulario.addEventListener("submit", function (e) {

    e.preventDefault();

    const nombre = document.getElementById("nombre").value.trim();

    const descripcion = document.getElementById("descripcion").value.trim();

    const categoria = document.getElementById("categoria").value;

    if (
        nombre === "" ||
        descripcion === "" ||
        categoria === ""
    ) {

        mensaje.innerHTML = `
        <div class="alert alert-danger">
            Complete todos los campos.
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

        <h5>${nombre}</h5>

        <p>${descripcion}</p>

        <span class="badge bg-primary mb-3">

            ${categoria}

        </span>

        <button class="btn btn-danger">

            Eliminar

        </button>

    `;

    const botonEliminar = tarjeta.querySelector("button");

    botonEliminar.addEventListener("click", function () {

        tarjeta.remove();

        total--;

        contador.textContent = total;

    });

    lista.appendChild(tarjeta);

    total++;

    contador.textContent = total;

    formulario.reset();

});