const desde = document.getElementById('fechaInicio');
const hasta = document.getElementById('fechaFinal');
const modalOverlay = document.querySelector('.modal-overlay');



window.addEventListener("load", async () => {
    fechaActual();
});


document.getElementById('cr-buscar').addEventListener('click', function () {
    buscarCajas();
});

const buscarCajas = async () => {
    openProgressBar();
    try {
        const formData = new FormData();
        const empaque = document.getElementById("selector_empaque").value;
        formData.append("Inicio", desde.value);
        formData.append("Final", hasta.value);
        formData.append("Empaque", empaque);

        const options = {
            method: 'POST',
            headers: {
                'Cache-Control': 'no-cache, no-store, must-revalidate'
            },
            body: formData
        };

        const response = await fetch("busqueda-cajas/", options);
        const data = await response.json();
        if (data.Message == "Success") {

            let detalles = ``;
            data.DataCaja.forEach((datos) => {
                console.log(datos.FotoPlu);
                console.log(datos.FotoCaja);
                detalles += `
                            <div class="box-border">
                                <div class="tbc-header">
                                    <table>
                                        <tr>
                                            <td>Caja N°: ${datos.IdCaja}</td>
                                            <td>Bulto: ${datos.idBulto}</td>
                                            <td>Fecha: ${datos.Caja_Fecha}</td>
                                            <td>Hora: ${datos.Caja_Hora} Hs.</td>
                                            <td>Empaque: ${datos.Galpon}</td>
                                            <td>Máquina: ${datos.Maquina}</td>
                                        </tr>
                                    </table>
                                </div>

                                <div class="tbc-content">
                                    <div class="tbc-left-section">
                                        <table class="tbc-info-table">
                                            <tr>
                                                <td class="fondo-items">Variedad</td>
                                                <td class="fondo-items">Envase</td>
                                                <td class="fondo-items">Marca</td>
                                                <td class="fondo-items">Tamaño</td>
                                            </tr>
                                            <tr>
                                                <td>${datos.Variedad}</td>
                                                <td>${datos.Envase}</td>
                                                <td>${datos.Marca}</td>
                                                <td>${datos.Calibre}</td>
                                            </tr>
                                            <tr>
                                                <td class="fondo-items">Categoría</td>
                                                <td class="fondo-items">Embalador</td>
                                                <td class="fondo-items">UP</td>
                                                <td></td>
                                            </tr>
                                            <tr>
                                                <td>${datos.Calidad}</td>
                                                <td>${datos.Embalador}</td>
                                                <td>${datos.UP}</td>
                                                <td></td>
                                            </tr>
                                            <tr>
                                                <td class="fondo-items">Lote/UMI</td>
                                                <td class="fondo-items">% PLU</td>
                                                <td class="fondo-items">Peso Bruto</td>
                                                <td class="fondo-items">Peso Neto</td>
                                            </tr>
                                            <tr>
                                                <td>${datos.Lote} / ${datos.UMI}</td>
                                                <td>${datos.PLU}</td>
                                                <td>${datos.PesoBruto}</td>
                                                <td>${datos.PesoNeto}</td>
                                            </tr>
                                        </table>

                                        <div class="tbc-defects">
                                            <table>
                                                <tr>
                                                    <td class="fondo-items">DEFECTOS</td>
                                                </tr>
                                                <tr>
                                                    <td>Desformadas: ${datos.Deformadas}</td>
                                                    <td>Cracking: ${datos.Cracking}</td>
                                                </tr>
                                                <tr>
                                                    <td>T. Incorrecto: ${datos.TamañoIncorrecto}</td>
                                                    <td>Bitterpit/Corcho: ${datos.Bitterpit}</td>
                                                </tr>
                                                <tr>
                                                    <td>Falta de Color: ${datos.FaltaDeColor}</td>
                                                    <td>Granizo: ${datos.Granizo}</td>
                                                </tr>
                                                <tr>
                                                    <td>Russeting: ${datos.Russeting}</td>
                                                    <td>Daño por Insecto: ${datos.DañoPorInsecto}</td>
                                                </tr>
                                                <tr>
                                                    <td>Heladas: ${datos.Heladas}</td>
                                                    <td>Falta de Pedúnculo: ${datos.FaltaDePedunculo}</td>
                                                </tr>
                                                <tr>
                                                    <td>Roce Bins: ${datos.roceBins}</td>
                                                    <td>Desvío Calsificación: ${datos.DesvioDeClasificacion}</td>
                                                </tr>
                                                <tr>
                                                    <td>Asoleado: ${datos.Asoleado}</td>
                                                    <td>Segunda Flor: ${datos.SegundaFlor}</td>
                                                </tr>
                                                <tr>
                                                    <td>Quemado por Sol: ${datos.QuemadoPorSol}</td>
                                                    <td>Madurez: ${datos.Madurez}</td>
                                                </tr>
                                                <tr>
                                                    <td>Fitotoxicidad: ${datos.Fitotoxicidad}</td>
                                                    <td>Deshidratación: ${datos.Deshidratacion}</td>
                                                </tr>
                                                <tr>
                                                    <td>Rolado: ${datos.Rolado}</td>
                                                    <td>Decahimiento Interno: ${datos.Decaimiento}</td>
                                                </tr>
                                                <tr>
                                                    <td>Golpes P/M/G: ${datos.Golpes}</td>
                                                    <td>C. Mohoso H/S/A: ${datos.MohoHumedo}/${datos.MohoSeco}/${datos.MohoAcuoso}</td>
                                                </tr>
                                                <tr>
                                                    <td>Heridas P/M/G: ${datos.Heridas}</td>
                                                    <td>Firmeza Pulpa Min/Prom/Max: ${datos.FirmezaPulpaMin}/${datos.FirmezaPulpaPromedio}/${datos.FirmezaPulpaMin}</td>
                                                </tr>
                                                <tr>
                                                    <td>Heridas Viejas P/M/G: ${datos.HeridasViejas}</td>
                                                    <td>Falta de Boro: ${datos.faltaDeBoro}</td>
                                                </tr>
                                                <tr>
                                                    <td>Rameado: ${datos.Rameado}</td>
                                                    <td>Obs: ${datos.Observaciones}</td>
                                                </tr>
                                            </table>
                                        </div>
                                    </div>

                                    <div class="tbc-right-section">
                                        <div class="tbc-image-plu">
                                            <p>Imagen PLU</p>
                                            <img src="${'http://191.97.47.114:8000/api/calidad/caja/' + (datos.FotoPlu !== '0' ? datos.FotoPlu : 'nodisponible.png')}" alt="Imagen PLU" class="tbc-imagen-plu">
                                        </div>
                                        <div class="tbc-image-caja">
                                            <p>Imagen Caja</p>
                                            <img src="${'http://191.97.47.114:8000/api/calidad/caja/' + (datos.FotoCaja !== '0' ? datos.FotoCaja : 'nodisponible.png')}" alt="Imagen Caja" class="tbc-imagen-caja">
                                        </div>
                                    </div>
                                </div>
                            </div>
                            `
            });
            document.getElementById('listadoCajas').innerHTML = detalles;
            closeProgressBar();
        } else {
            closeProgressBar();
            document.getElementById('listadoCajas').innerHTML = ``;
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        closeProgressBar();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};




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

document.getElementById("closePopup").addEventListener("click", function () {
    document.getElementById("popup").classList.remove("active");
});

function mostrarInfo(Message, Color) {
    document.getElementById("popup").classList.add("active");
    const colorBorderMsg = document.getElementById("popup");
    const mensaje = document.getElementById("mensaje-pop-up");
    colorBorderMsg.style.border = `2px solid ${Color}`;
    mensaje.innerHTML = `<p style="color: black; font-size: 13px;"><b>${Message}</b></p>`;

    setTimeout(() => {
        document.getElementById("popup").classList.remove("active");
    }, 5000);
}





























