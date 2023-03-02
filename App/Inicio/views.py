from django.shortcuts import render
from App.ZTime.conexion import *
from django.http import JsonResponse
import json

##LOGIN
from django.contrib.auth.decorators import login_required
from  django.contrib.auth import logout



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
        print(e)
        permiso = "0"
        return permiso
    finally:
        cursorZT.close()
        ZT.close()

# Create your views here.
def Index_inicio(request):
    return render (request, 'Inicio/index.html')

@login_required
def inicio(request):
    return render (request, 'Inicio/inicio.html')


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