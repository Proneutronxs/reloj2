
const loginPopup = document.getElementById('login-popup');

$("#login").on("click",function(event){
  event.preventDefault();
  // resto de tu codigo
  loginPopup.style.display = 'block';
});

$("#close-popup-login").on("click",function(event){
  event.preventDefault();
  // resto de tu codigo
  loginPopup.style.display = 'none';
});

function mostrar_inicio(){
  loginPopup.style.display = 'block';
}

function permiso_Zetonetime() {
  fetch("/user/permissions/modulo=ZetoneTime", {
    method: "GET"
  }).then(
    function(response){
      return response.json();      
    }
  ).then(
    function(data){
      //console.log(data)
      try {
        let arrayData = JSON.parse(data);//CONVIERTE EL JSON en ARRAY
        if(arrayData.permiso == 1){
          //console.log(arrayData.permiso)
          window.location.href = '/zetonetime/';
        }else{
          alert(arrayData.message);
        }
      }catch(error){
        console.log(error);
      }
    }
  );  
}

function permiso_ZetoneFrio() {
  fetch("/user/permissions/modulo=ZetoneFrio", {
    method: "GET"
  }).then(
    function(response){
      return response.json();      
    }
  ).then(
    function(data){
      //console.log(data)
      try {
        let arrayData = JSON.parse(data);//CONVIERTE EL JSON en ARRAY
        if(arrayData.permiso == 1){
          //console.log(arrayData.permiso)
          window.location.href = '/frigorifico/';
        }else{
          alert(arrayData.message);
        }
      }catch(error){
        console.log(error);
      }
    }
  );  
}

function permiso_ZetoneEmpaque() {
  fetch("/user/permissions/modulo=ZetoneEmpaque", {
    method: "GET"
  }).then(
    function(response){
      return response.json();      
    }
  ).then(
    function(data){
      //console.log(data)
      try {
        let arrayData = JSON.parse(data);//CONVIERTE EL JSON en ARRAY
        if(arrayData.permiso == 1){
          //console.log(arrayData.permiso)
          window.location.href = '/empaque/';
        }else{
          alert(arrayData.message);
        }
      }catch(error){
        console.log(error);
      }
    }
  );  
}