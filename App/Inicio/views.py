from django.shortcuts import render
from App.ZTime.conexion import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
import json

##LOGIN
from django.contrib.auth.decorators import login_required
from App.Inicio.models import UserProfile
from  django.contrib.auth import logout


# Create your views here.




@csrf_exempt
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            

            #print(request, user)
            login(request, user)
            
            # try:
            #     user_profile = UserProfile.objects.get(user=user)
            # except UserProfile.DoesNotExist:
            #     user_profile = UserProfile.objects.create(user=user)

            # if not user_profile.password_changed:
            #     data = "repassword/"
            #     return JsonResponse({'Message': 'Change', 'data': data})
            # else:
            data = "Se inicio sesion."
            return JsonResponse({'Message': 'success', 'data': data})
        
        else:
            data = "No se pudo iniciar sesión, verifique los datos."
            return JsonResponse({'Message': 'Error', 'data': data})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})

@login_required
@csrf_exempt
def cambiar_password(request):
    if request.method == 'POST':
        try:
            user = request.user
            current_password = request.POST.get('currentPassword')
            new_password = request.POST.get('newPassword')
            if not user.check_password(current_password):
                return JsonResponse({'Message': 'Error', 'Nota': 'La contraseña actual es incorrecta.'})
            if current_password == new_password:
                return JsonResponse({'Message': 'Error', 'Nota': 'La contraseña no puede ser igual a la actual.'})
            
            try:
                user_profile = UserProfile.objects.get(user=user)
                user_profile.password_changed = True
                user_profile.save()
                user.set_password(new_password)
                user.save()

                

                data = "Se cambió la contraseña correctamente."
                return JsonResponse({'Message': 'Success', 'Nota': data})
            
            except Exception as e:
                data = "El Usuario no Existe."
                return JsonResponse({'Message': 'Error', 'Nota': data})
            
        except Exception as e:
            data = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': data})
    else:
        data = "No se pudo resolver la petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})

##FUNCIÓN DE RETORNO DE USUARIO
def user_permissions(user, permissions):
    try:
        ZT = ZetoneTime()
        cursorZT = ZT.cursor()
        consulta_permisos = ("SELECT "+str(permissions)+" FROM Permisos WHERE Usuario='"+ str(user) +"'")
        cursorZT.execute(consulta_permisos)
        consultaZT = cursorZT.fetchone()
        if consultaZT:
            permiso = str(consultaZT[0])
            return permiso
        else:
            permiso = "0"
            return permiso
    except Exception as e:
        permiso = "0"
        return permiso
    finally:
        cursorZT.close()
        ZT.close()

# Create your views here.
#@login_required
def inicioSesion(request):
    return render (request, 'Inicio/index.html')


def repassword(request):
    return render (request, 'Inicio/repass.html')

@login_required
def inicioMenu(request):
    return render (request, 'Inicio/inicio.html')

@login_required
def newIndex(request):
    return render (request, 'Inicio/newIndex.html')



#FUNCION DE PERMISO GENERAL 
def json_premissions(request, modulo):
    usuario = str(request.user)
    modulo = str(modulo)
    permiso = user_permissions(usuario,modulo)
    if permiso == "1":
        jsonList = json.dumps({'message': 'No tiene permisos para acceder a este sector.', 'permiso':permiso}) 
        return JsonResponse(jsonList, safe=False)
    else:
        jsonList = json.dumps({'message': 'No tiene permisos para acceder a este sector.', 'permiso':permiso}) 
        return JsonResponse(jsonList, safe=False)