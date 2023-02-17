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

//pagina cargar registros
function listadoCalcHoras(){
  $.ajax({
    url:"/registros/calculo",
    type:"get",
    dataType:"json",
    success: function(response){
      console.log(response)
    },
    error: function(response){
      console.log("js")
    }
  });
}



//window.onload = function(){
    //bultos();
  //setInterval('bultos()',1000);
//}

function verCalculoHoras() {

  var formCalchoras = new FormData(document.getElementById('formCalcHoras'));
  fetch("/resgistros/calculo/horas", {
    method: "POST",
    body: formCalchoras,
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
          //console.log(arrayData.registros)
          let listaregistros = ``;
            arrayData.registros.forEach((registros) =>{
                listaregistros += `
                <tr>
                  <td>${registros.legajo}</td>
                  <td>${registros.nombre}</td>
                  <td>${registros.dia}</td>
                  <td>${registros.fecha}</td>
                  <td>${registros.f1}</td>
                  <td>${registros.f2}</td>
                  <td>${registros.f3}</td>
                  <td>${registros.f4}</td>
                  <td>${registros.hm}</td>
                  <td>${registros.ht}</td>
                  <td>${registros.ex}</td>
                </tr>`;
            });
            document.getElementById('tableCalHoras').innerHTML = listaregistros;
        }else{
          alert(arrayData.message);
        }
      }catch(error){
        console.log(error);
      }
    }
  );  
}

$("#buscar_sinProceso").on("click",function(event){
  event.preventDefault();
  // resto de tu codigo
  var formHorasSinProceso = new FormData(document.getElementById('formHorasSinProceso'));
  fetch("/registros/sin/proceso", {
    method: "POST",
    body: formHorasSinProceso,
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
          //console.log(arrayData.registros)
          let listaregistros = ``;
            arrayData.registros.forEach((registros) =>{
                listaregistros += `
                <tr>
                <td>${registros.legajo}</td>
                <td>${registros.nombre}</td>
                <td>${registros.dia}</td>
                <td>${registros.fecha}</td>
                <td>${registros.hora}</td>
              </tr>`;
            });
            document.getElementById('tablasSinProceso').innerHTML = listaregistros;
         
        }else{
          alert(arrayData.message);
        }
      }catch(error){
        console.log(error);
      }
    }
  ); 
});

$("#exportRegister").on("click",function(event){
  event.preventDefault();

  let progressBar = `<div class="loaderZeto" id="progressBar"></div>`
  document.getElementById('descargaRegisros').innerHTML = progressBar;
  // resto de tu codigo
  var formHorasSinProceso = new FormData(document.getElementById('formHorasSinProceso'));
  fetch("/create/excel/registros", {
    method: "POST",
    body: formHorasSinProceso,
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
          //console.log(arrayData.excel)
          let descarga =  `<button class="button" onclick="hideButton()" id="descargaExcel"><a href="http://10.32.26.35/download-excel/${arrayData.excel}">Descargar</a></button>`;
          document.getElementById('descargaRegisros').innerHTML = descarga;
          //hideButton();
        }else{
          alert(arrayData.message);
        }
      }catch(error){
        console.log(error);
      }
    }
  ); 
});

$("#exportCalculo").on("click",function(event){
  let progressBar = `<div class="loaderZeto" id="progressBar"></div>`
  document.getElementById('descargaCalculo').innerHTML = progressBar;
  event.preventDefault();
  // resto de tu codigo
  var formHorasCalculo = new FormData(document.getElementById('formCalcHoras'));
  fetch("/create/excel/calculo", {
    method: "POST",
    body: formHorasCalculo,
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
          //console.log(arrayData.excel)
          hideProgessBar();
          let descarga =  `<button class="button" onclick="hideButton()" id="descargaExcel"><a href="http://10.32.26.35/download-excel/${arrayData.excel}">Descargar</a></button>`;
          document.getElementById('descargaCalculo').innerHTML = descarga;
        }else{
          alert(arrayData.message);
        }
      }catch(error){
        console.log(error);
      }
    }
  ); 
});

function hideButton() {
  var button = document.getElementById("descargaExcel");
  button.style.display = "none";
}

function hideProgessBar() {
  var button = document.getElementById("progressBar");
  button.style.display = "none";
}

$("#mostraCalcHoras").on("click",function(event){
  event.preventDefault();
  // resto de tu codigo
  verCalculoHoras();
});


function no_Disponible(){
  alert("Función aún no disponible.");
}

