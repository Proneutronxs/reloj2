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
          let descarga =  `<a href="http://191.97.47.105:8000/empaque/reportes/donwload/${arrayData.pdf}"><button type="button" class="button" onclick="hideButton()" id="descargaPDF">Descargar</button></a>`;
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
  var button = document.getElementById("descargaPDF");
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



