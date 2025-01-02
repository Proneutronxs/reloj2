const desde = document.getElementById('fechaInicio');
const hasta = document.getElementById('fechaFinal');

window.addEventListener("load", async () => {
    fechaActual();
    cargaDepartamentos();
});


const choiceLegajos = new Choices('#selector_legajos', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE LEGAJO',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceDepartamentos = new Choices('#selector_departamentos', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE DEPARTAMENTO',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});


const cargaDepartamentos = async () => {
    openProgressBar();
    try {
        const response = await fetch("carga-departamentos/");
        const data = await response.json();
        closeProgressBar();
        console.log(data);
        if (data.Message == "Success") {
            let result = [];
            result.push();
            data.Datos.forEach((datos) => {
                result.push({ value: datos.Codigo, label: datos.Descripcion });
            });
            choiceDepartamentos.setChoices(result, 'value', 'label', true);
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

function fechaActual() {
    var fecha = new Date();
    var mes = fecha.getMonth() + 1;
    var dia = fecha.getDate();
    var ano = fecha.getFullYear();
    if (dia < 10) dia = '0' + dia;
    if (mes < 10) mes = '0' + mes;
    const formattedDate = `${ano}-${mes}-${dia}`;
    const formattedDateDesde = `${ano}-${mes}-${'01'}`;
    desde.value = formattedDateDesde;
    hasta.value = formattedDate;
}