

const loginButton = document.getElementById("login-button");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");

const popup = document.getElementById("pop-pass");
const changePasswordForm = document.getElementById("changePasswordForm");


document.getElementById('login-button').addEventListener('click', function() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    fetch('pxs/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: 'username=' + encodeURIComponent(username) + '&password=' + encodeURIComponent(password)
    })
    .then(response => response.json())
    .then(data => {
        if (data.Message == 'success') {
            window.location.href = '/';
        } else if (data.Message == 'Change') {
            popup.style.display = "flex";
        } else {
            var Message = data.data;
            var Color = 'Red';
            mostrarInfo(Message,Color)
        }
    })
    .catch(error => {
        console.log(error);
        console.error('Error al iniciar sesión:', error);
    });
});


passwordInput.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
      // Si se presiona Enter, haz clic en el botón de inicio de sesión
      loginButton.click();
    }
});


document.getElementById('changePasswordButton').addEventListener('click', function() {
    change_password();    
});


const change_password = async () => {
    try {
        const form = document.getElementById("changePasswordForm");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("change-password/", options);
        const data = await response.json();
        if(data.Message=="Success"){
            var nota = data.Nota
            var color = "green";
            mostrarInfo(nota,color) 
            setTimeout(function() {
                window.location.href = 'logout/';
            }, 2000);
        }else {
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota,color) 
        }
    } catch (error) {
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        mostrarInfo(nota,color); 
    }
};

document.getElementById("closePopup").addEventListener("click", function() {
    document.getElementById("popup").classList.remove("active");
});

function mostrarInfo(Message,Color) {
    document.getElementById("popup").classList.add("active");
    const colorBorderMsg = document.getElementById("popup");
    const mensaje = document.getElementById("mensaje-pop-up");
    colorBorderMsg.style.border = `2px solid ${Color}`;
    mensaje.innerHTML = `<p style="color: black; font-size: 13px;"><b>${Message}</b></p>`;

    setTimeout(() => {
        document.getElementById("popup").classList.remove("active");
    }, 5000);
}






