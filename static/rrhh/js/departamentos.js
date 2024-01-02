


window.addEventListener("load", async () => {
    await cargaDepartamentos();
});

document.getElementById("btnGuardaDepartamento").addEventListener("click", function () {
    const nombreDepto = document.getElementById("nombreDepto").value;
    if (nombreDepto === '') {
        var Message = "El Nombre del Departamento no puede estar vacío.";
        mostrarError(Message);
    } else {
        enviaDepartamento();
    }
});

const cargaDepartamentos = async () => {
    openProgressBar();
    try {
        const response = await fetch("llama-departamentos/");
        const data = await response.json();
        if (data.Message == "Success") {
            let listado = ``;
            data.Datos.forEach(datos => {
                listado += `<tr>                                  
            <td style="width: 100px;">${datos.idDepto}</td>
            <td >${datos.nombre}</td
            </tr>`;
            });

            document.getElementById('tablaDepartamentos').innerHTML = listado;
            closeProgressBar();
        }else {
            closeProgressBar();
        }

    } catch (error) {
        alert("No se pudieron Cargar los Departamentos.")
        closeProgressBar();
    }
};

const modalOverlay = document.querySelector('.modal-overlay');
function openProgressBar() {
    modalOverlay.style.display = 'block';
}
function closeProgressBar() {
    modalOverlay.style.display = 'none';
}

const enviaDepartamento = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formGuardaDepartamento");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };
        const response = await fetch("guarda-departamentos/", options);
        const data = await response.json();
        if (data.Message == "Success") {
            var nota = data.Nota
            mostrarInfo(nota);
            closeProgressBar();
            document.getElementById("nombreDepto").value = '';
            await cargaDepartamentos();
        } else {
            var nota = data.Nota
            mostrarInfo(nota);
            closeProgressBar();
        }
    } catch (error) {
        closeProgressBar();
        alert("Se produjo un error al procesar la solicitud.");
    }
};

function mostrarInfo(Message) {
    const infoParrafo = document.getElementById("infoParrafo");
    infoParrafo.innerHTML = `<p style="color: darkgreen; font-size: 13px;"><b>${Message}</b></p>`;
    infoParrafo.style.display = "block";

    setTimeout(() => {
        infoParrafo.style.display = "none";
    }, 5000);
}

function mostrarError(Message) {
    const infoParrafo = document.getElementById("infoParrafo");
    infoParrafo.innerHTML = `<p style="color: darkred; font-size: 13px;"><b>${Message}</b></p>`;
    infoParrafo.style.display = "block";

    setTimeout(() => {
        infoParrafo.style.display = "none";
    }, 5000);
}
  
































