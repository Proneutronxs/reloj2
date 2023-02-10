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
  fetch("/json", {
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
      console.log(data)
      try {
        let arrayData = JSON.parse(data);//CONVIERTE EL JSON en ARRAY
        if(arrayData.message == "Success"){
          console.log(arrayData.registros)
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
          alert("No se encontraron fichadas");
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
          console.log(arrayData.registros)
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
          alert("No se encontraron fichadas");
        }
      }catch(error){
        console.log(error);
      }
    }
  ); 
});

$("#mostraCalcHoras").on("click",function(event){
  event.preventDefault();
  // resto de tu codigo
  verCalculoHoras();
});

$("#exportRegister").on("click",function(event){
  event.preventDefault();
  no_Disponible();
});


function no_Disponible(){
  alert("Función aún no disponible.");
}

