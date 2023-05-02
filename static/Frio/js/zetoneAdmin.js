//TOKEN
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}


function buscar_reportes_camaras() {
  showProgressBar();
  var formReporteCamara = new FormData(document.getElementById('formReportesCamaras'));
  fetch("/empaque/reportes/camaras/buscar", {
    method: "POST",
    body: formReporteCamara,
    headers: {
      "X-CSRFToken": getCookie('csrftoken'),
    }
  }).then(
    function(response){
      return response.json();      
    }
  ).then(
    function(data){
      //console.log(data)
      try {
        let arrayData = JSON.parse(data);//CONVIERTE EL JSON en ARRAY
        if(arrayData.message == "Success"){
          hideProgessBar();
          console.log(arrayData.pdf)
          let descarga =  `<a href="http://10.32.26.35/empaque/reportes/donwload/${arrayData.pdf}"><button type="button" class="button" onclick="hideButton()" id="descargaPDF">Descargar</button></a>`;
          document.getElementById('descargarReportesCamaras').innerHTML = descarga;
        }else{
          hideProgessBar();
          alert(arrayData.message);
        }
      }catch(error){
        hideProgessBar();
        console.log(error);
      }
    }
  );  
}

function hideButton() {
  var button = document.getElementById("descarga_ZIP");
  button.style.display = "none";
}

function hideProgessBar() {
  const modal = document.getElementById('modal');
  modal.style.display = "none";
}

function showProgressBar(){
  modal.style.display = 'block';
}



$("#buscarReportes").on("click",function(event){
  event.preventDefault();
  // resto de tu codigo
  buscar_reportes_camaras();
});




function no_Disponible(){
  alert("Función aún no disponible.");
}


const cargaEspacio = async() => {
  showProgressBar();
  try{
      const response = await fetch("espacio");
      const data = await response.json();
      let datos = JSON.parse(data)
      if (datos.message == "Success"){
          let espacio = ``;
          espacio = `<a href="#" class="nav-link"  style="color: #011327;" >Espacio - ${datos.datos}</a>`;
          document.getElementById('freeSpace').innerHTML = espacio;
          hideProgessBar();
      }else{
          let espacio = ``;
          espacio = `<a href="#" class="nav-link"  style="color: #011327;" >Espacio: --- </a>`;
          document.getElementById('freeSpace').innerHTML = espacio;
          hideProgessBar();
      }
      
  } catch(error){
      console.error(error)
      alert("se produjo un error a procesar la solicitud.");
      hideProgessBar();
  }
};

const creaZIP = async() => {
  showProgressBar();
  try{
      const response = await fetch("compresspdf");
      const data = await response.json();
      let datos = JSON.parse(data)
      if (datos.message == "Success"){
        console.log(datos)
        let espacio = ``;
        espacio = `<a href="http://10.32.26.35/administracion/descargazip/archivos_pdf.zip"><button type="button" class="button" onclick="hideButton()" id="descarga_ZIP">DESCARGAR</button></a>`;
        document.getElementById('descargaZIP').innerHTML = espacio;
        hideProgessBar();
      }else{
        hideProgessBar();
        alert("se produjo un error a procesar la solicitud.");
      }
      
  } catch(error){
      console.error(error);
      hideProgessBar();
      alert("se produjo un error a procesar la solicitud.");
  }
};

$("#descargaPDF").on("click",function(event){
  event.preventDefault();
  // resto de tu codigo
  creaZIP();
});

const borraZIP_PDF = async() => {
  showProgressBar();
  try{
      const response = await fetch("delete/zip-pdf");
      const data = await response.json();
      let datos = JSON.parse(data)
      if (datos.message == "Success"){
        let espacio = ``;
        espacio = `<div class="titulo-card" >Los archivos se borraron correctamente.</div>`;
        document.getElementById('notaPDF').innerHTML = espacio;
        hideProgessBar();
      }else{
        hideProgessBar();
        alert("se produjo un error a procesar la solicitud.");
      }
      
  } catch(error){
      console.error(error);
      hideProgessBar();
      alert("se produjo un error a procesar la solicitud.");
  }
};

$("#borrarPDF").on("click",function(event){
  event.preventDefault();
  // resto de tu codigo
  borraZIP_PDF();
});

const borraEXCEL = async() => {
  showProgressBar();
  try{
      const response = await fetch("delete/excel-files");
      const data = await response.json();
      let datos = JSON.parse(data)
      if (datos.message == "Success"){
        let espacio = ``;
        espacio = `<div class="titulo-card" >Los archivos se borraron correctamente.</div>`;
        document.getElementById('notaEXCEL').innerHTML = espacio;
        hideProgessBar();
      }else{
        hideProgessBar();
        alert("se produjo un error a procesar la solicitud.");
      }
      
  } catch(error){
      console.error(error);
      hideProgessBar();
      alert("se produjo un error a procesar la solicitud.");
  }
};

$("#borrarEXCEL").on("click",function(event){
  event.preventDefault();
  // resto de tu codigo
  borraEXCEL();
});


const borraImagenes = async() => {
  showProgressBar();
  try{
      const response = await fetch("delete/images");
      const data = await response.json();
      let datos = JSON.parse(data)
      if (datos.message == "Success"){
        let espacio = ``;
        espacio = `<div class="titulo-card" >Los archivos se borraron correctamente.</div>`;
        document.getElementById('notaJPEG').innerHTML = espacio;
        hideProgessBar();
      }else{
        hideProgessBar();
        alert("se produjo un error a procesar la solicitud.");
      }
      
  } catch(error){
      console.error(error);
      hideProgessBar();
      alert("se produjo un error a procesar la solicitud.");
  }
};

$("#borrarImagenes").on("click",function(event){
  event.preventDefault();
  // resto de tu codigo
  borraImagenes();
});

window.addEventListener("load", async () =>{
  await cargaEspacio();
});
