// FORMULARIOS DE CARGA CORRIDO/CORTADO
const horarioCorrido = document.getElementById("horario-corrido");
const horarioCortado = document.getElementById("horario-cortado");


ComboxTipoHorario.addEventListener("change", (event) => {
    const selectedValue = event.target.value;
    if (selectedValue === '0') {
        horarioCorrido.style.display = 'none';
        horarioCortado.style.display = 'none';
    } else if (selectedValue === '1') {
        horarioCorrido.style.display = 'block';
        horarioCortado.style.display = 'none';
    }else if (selectedValue === '2') {
        horarioCorrido.style.display = 'none';
        horarioCortado.style.display = 'block';
    }
});

// FORMULARIOS CARGA PARA ASIGNACIÓN
ComboxAsignarPor.addEventListener("change", (event) => {
    const tablaLegajos = document.getElementById("tabla-legajos");
    const tablaDeptos = document.getElementById("tabla-departamentos");
    const comboxHorarios = document.getElementById("ComboxTurnoHorario");
    const selectedValue = event.target.value;
    if (selectedValue === '0') {
        tablaLegajos.style.display = 'none';
        tablaDeptos.style.display = 'none';
        comboxHorarios.style.display = 'none';
    } else if (selectedValue === 'D') {
        comboxHorarios.style.display = 'block';
        tablaLegajos.style.display = 'none';
        tablaDeptos.style.display = 'block';
        cargaTurnosHorarios();
        mostrarLegajos_Departamentos();
    }else if (selectedValue === 'L') {
        comboxHorarios.style.display = 'block';
        tablaDeptos.style.display = 'none';
        tablaLegajos.style.display = 'block';
        cargaTurnosHorarios();
        mostrarLegajos_Departamentos();
    }
});

document.getElementById("btnGuardaTurnoHorario").addEventListener("click", function () {
    // DESCRIPCION DEL TURNO
    const descripcionTurno = document.getElementById("descripcionTurno").value;
    //CORRIDO
    const turnoEntrada = document.getElementById("entrada").value;
    const turnoSalida = document.getElementById("salida").value;
    //CORTADO
    const entradaMañana = document.getElementById("entrada-mañana").value;
    const salidaMañana = document.getElementById("salida-mañana").value;
    const entradaTarde = document.getElementById("entrada-tarde").value;
    const salidaTarde = document.getElementById("salida-tarde").value;
    //COMBOX TIPO TURNO
    const comboxTurno = document.getElementById("ComboxTipoHorario").value;
    if (comboxTurno === '0'){
        var Message = "Debe Seleccionar un Turno.";
        mostrarError(Message);
    }else if (comboxTurno === '1'){
        if (turnoEntrada === '' || turnoSalida == '' || descripcionTurno === ''){
            var Message = "Debe Completar todos los campos.";
            mostrarError(Message);
        }else{
            enviaHorario();
        }
        
    }else if (comboxTurno === '2'){
        if (entradaMañana === '' || salidaMañana == '' || entradaTarde === '' || salidaTarde === '' || descripcionTurno === ''){
            var Message = "Debe Completar todos los campos.";
            mostrarError(Message);
        }else{
            enviaHorario();
        }
    }
});




const enviaHorario = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formGuardaTurno");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };
        const response = await fetch("guarda-horarios/", options);
        const data = await response.json();
        if (data.Message == "Success") {
            var nota = data.Nota
            mostrarInfo(nota);
            document.getElementById("descripcionTurno").value = '';
            document.getElementById("entrada").value = '';
            document.getElementById("salida").value = '';
            document.getElementById("entrada-mañana").value = '';
            document.getElementById("salida-mañana").value = '';
            document.getElementById("entrada-tarde").value = '';
            document.getElementById("salida-tarde").value = '';
            closeProgressBar();
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


const mostrarLegajos_Departamentos = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formBuscaDepto-Legajos");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("muestra-legajos-departamentos/", options);
        const data = await response.json();
        if(data.Message=="Success"){
            if (data.Tipo=="Legajos"){
                let datos_completa = ``;
                data.Datos.forEach((datos) => {
                datos_completa += `<tr>
                <td style="width: 40px;">
                    <input id="idCheck" name="idCheck" value="${datos.legajo}" class="input-checkbox" type="checkbox">
                </td> 
                <td style="width: 80px;">${datos.legajo}</td>
                <td style="width: 245px; text-align: left;">${datos.nombre}</td>
                <td style="width: 160px;">${datos.departamento}</td>
                <td >${datos.horario}</td>
            </tr>`
            });
            document.getElementById('bodyAsignarHorario').innerHTML = datos_completa;
                closeProgressBar(); 
            }
            if (data.Tipo=="Departamentos"){
                let datos_completa = ``;
                data.Datos.forEach((datos) => {
                datos_completa += `<tr>
                <td style="width: 40px;">
                    <input id="idCheck" name="idCheck" value="${datos.idDepto}" class="input-checkbox" type="checkbox">
                </td> 
                <td >${datos.departamento}</td>
            </tr>`
            });
            document.getElementById('bodyAsignarHorarioDepto').innerHTML = datos_completa;
                closeProgressBar(); 
            }
            closeProgressBar();
        }else {
            closeProgressBar();
            var nota = data.Nota
            alert(nota);
        }
    } catch (error) {
        closeProgressBar();
        alert("Se produjo un error al procesar la solicitud.");
    }
};


const cargaTurnosHorarios = async () => {
    try {
        const response = await fetch("carga-combox-horarios/");
        const data = await response.json();
        if (data.Message == "Success") {
            let listado = `<option value="0">Seleccione</option>`;
            data.Datos.forEach(datos => {
                listado += `<option value="${datos.idTurno}">${datos.descripTurno}</option>`;
            });
            document.getElementById('ComboxHorarios').innerHTML = listado;
            closeProgressBar();
        }else {
            closeProgressBar();
            alert("No se pudieron Cargar los Horarios.");
        }

    } catch (error) {
        alert("No se pudo procesar la solicitud")
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
  