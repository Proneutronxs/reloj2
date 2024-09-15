
from django.db import connections
from django.http import JsonResponse
from App.ZTime.conexion import *
import requests
from requests.auth import HTTPBasicAuth
import json
import os
from django.http import HttpResponse, Http404
from PIL import Image
import base64
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# Create your views here.

################### CALIDAD EMPAQUE ############################

##COMPROBAR SI LA IMAGEN EXISTE EN LA TABLA
def verificar_existencia(id):
    try:
        app = zetoneApp()
        cursor = app.cursor()
        sql =("SELECT Bulto FROM imagenes_reporte_empaque WHERE Bulto='" + str(id) + "'")
        cursor.execute(sql)
        consulta = cursor.fetchone()
        if consulta:
            return 1
        else:
            return 0
    except Exception as e:
        print("Error")
        print(e)
        return 5
    finally:
        cursor.close()
        app.close()

### INSERTA EL NOMBRE DE LA CAJA 
def inserta_nombre_caja(bulto,nombre):
    try:
        app = zetoneApp()
        cursor = app.cursor()
        sql =("INSERT INTO imagenes_reporte_empaque (Bulto, Caja) VALUES ('" + str(bulto) + "','" + str(nombre) + "')")
        cursor.execute(sql)
        cursor.commit()
    except Exception as e:
        print("Error")
        print(e)
        return 5
    finally:
        cursor.close()
        app.close()

### GUARDA LA IMAGEN DE LA CAJA
@csrf_exempt
def image_caja(request):
    if request.method == 'POST' and request.POST.get('caja'):
        nombre_post = request.POST.get('id')
        imagen_codificada = request.POST.get('caja')
        imagen = base64.b64decode(imagen_codificada)
        nombre = "caja_image_" + str(nombre_post) + ".jpeg"
        with open('App/API/media/images/Calidad/reportes_empaque/' + nombre , "wb") as image:
            image.write(imagen)
        if verificar_existencia(nombre_post) == 0:
            inserta_nombre_caja(nombre_post, nombre)
        return JsonResponse({'message': 'Success'})
    else:
        return JsonResponse({'error': 'Error al subir la imagen.'})

### GUARDA LA IMAGEN DEL PLU
@csrf_exempt
def image_plu(request):
    if request.method == 'POST' and request.POST.get('plu'):
        nombre_post = request.POST.get('id')
        imagen_codificada = request.POST.get('plu')
        
        imagen = base64.b64decode(imagen_codificada)
        nombre = "plu_image_" + str(nombre_post) + ".jpeg"
        with open('App/API/media/images/Calidad/reportes_empaque/' + nombre , "wb") as image:
            image.write(imagen)
        if verificar_existencia(nombre_post) == 0:
            inserta_nombre_caja(nombre_post, nombre)
        return JsonResponse({'message': 'Success'})
    else:
        return JsonResponse({'error': 'Error al subir la imagen.'})

### GUARDA LA IMAGEN DEL PLU Y DE LA CAJA
@csrf_exempt
def image_caja_plu(request):
    if request.method == 'POST' and request.POST.get('caja'):
        nombre_post = request.POST.get('id')

        imagen_codificada_caja = request.POST.get('caja')
        imagen_caja = base64.b64decode(imagen_codificada_caja)
        nombre_caja = "caja_image_" + str(nombre_post) + ".jpeg"
        with open('App/API/media/images/Calidad/reportes_empaque/' + nombre_caja , "wb") as image_caja:
            image_caja.write(imagen_caja)

        imagen_codificada_plu = request.POST.get('plu')
        imagen_plu = base64.b64decode(imagen_codificada_plu)
        nombre_plu = "plu_image_" + str(nombre_post) + ".jpeg"
        with open('App/API/media/images/Calidad/reportes_empaque/' + nombre_plu , "wb") as image_plu:
            image_plu.write(imagen_plu)

        if verificar_existencia(nombre_post) == 0:
            inserta_nombre_caja(nombre_post, nombre_caja)
        return JsonResponse({'message': 'Success'})
    else:
        return JsonResponse({'error': 'Error al subir la imagen.'})
    

### MUESTRA LA IMAGEN DEL PLU O LA CAJA
def ver_caja(request, nombre):
    ruta_imagenes = 'App/API/media/images/Calidad/reportes_empaque/'
    
    ruta_completa = os.path.join(ruta_imagenes, nombre)
    
    if os.path.exists(ruta_completa):
        with open(ruta_completa, 'rb') as archivo_imagen:
            respuesta = HttpResponse(archivo_imagen.read(), content_type='image/jpeg')
            respuesta['Content-Disposition'] = 'inline; filename=' + os.path.basename(ruta_completa)
            return respuesta
    else:
        return HttpResponse(status=404)


####################### MADUREZ DE FRUTA #################################

### CONTROL DE PRESIONES
@csrf_exempt
def inserta_presiones(request):
    if request.method == 'POST' and request.POST.get('empaque'):
        empaque = request.POST.get('empaque')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        fruto = request.POST.get('fruto')
        presion = request.POST.get('presion')
        usuario = request.POST.get('usuario')
        try:
            app = zetoneApp()
            cursor = app.cursor()
            sql =("INSERT INTO Presiones (Empaque, Fecha, Hora, Fruto, Presion, Usuario) VALUES ('" + str(empaque) + "','" + str(fecha) + "','" + str(hora) + "','" + str(fruto) + "','" + str(presion) + "','" + str(usuario) + "')")
            cursor.execute(sql)
            cursor.commit()
        except Exception as e:
            print("Error")
            print(e)
            return 5
        finally:
            cursor.close()
            app.close()
        return JsonResponse({'message': 'Success'})
    else:
        return JsonResponse({'error': 'Error al guardar los datos.'})
    
#### BUSCA PRESIONES
@csrf_exempt
def busca_presiones(request):
    if request.method == 'POST' and request.POST.get('fecha'):
        fecha = request.POST.get('fecha')
        try:
            app = zetoneApp()
            cursor = app.cursor()
            sql =("SELECT DISTINCT CONVERT(char(5), Hora) AS Hora, Empaque FROM Presiones WHERE (Fecha='" + str(fecha) + "')")
            cursor.execute(sql)
            consulta = cursor.fetchall()
            if consulta:
                lista = []
                for i in consulta:
                    hora = str(i[0])
                    empaque = str(i[1])
                    if empaque == "1":
                        empaque = "PERA"
                    if empaque == "8":
                        empaque = "MANZANA"
                    conjunto = f"{empaque}: {hora}" ##str(empaque + ": " + hora)
                    resultado = {'horas': conjunto}
                    lista.append(resultado)
                print(lista)
                jsonList = json.dumps({'message': 'Success', 'listado':lista})
                print(jsonList)
                #return HttpResponse(jsonList)
                return JsonResponse(jsonList, safe=False)
            else:
                jsonList = json.dumps({'message': 'Not Found'}) 
                return JsonResponse(jsonList, safe=False)
        except Exception as e:
            print(e)
            error = str(e)
            jsonList = json.dumps({'error': error}) 
            return JsonResponse(jsonList, safe=False)
        finally:
            cursor.close()
            app.close()

### MUESTRA PRESIONES
@csrf_exempt
def muestra_presiones(request):
    if request.method == 'POST' and request.POST.get('empaque'):
        empaque = request.POST.get('empaque')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        try:
            app = zetoneApp()
            cursor = app.cursor()
            sql =("SELECT DISTINCT CONVERT(char(5), Hora) AS Hora, Presion FROM Presiones WHERE (Empaque='" + str(empaque) + "' AND Fecha='" + str(fecha) + "' AND Hora='" + str(hora) + "')")
            cursor.execute(sql)
            consulta = cursor.fetchall()
            if consulta:
                lista = []
                for i in consulta:
                    hora = str(i[0])
                    presion = str(i[1])
                    result = {'hora': hora, 'presion': presion}
                    lista.append(result)
                jsonList = json.dumps({'message': 'Success', 'listado':lista}) 
                return JsonResponse(jsonList, safe=False)
            else:
                jsonList = json.dumps({'message': 'Not Found'}) 
                return JsonResponse(jsonList, safe=False)
        except Exception as e:
            error = str(e)
            jsonList = json.dumps({'error': error}) 
            return JsonResponse(jsonList, safe=False)
        finally:
            cursor.close()
            app.close()

### MUESTRA PRESIONES
@csrf_exempt
def promedio_presiones(request):
    if request.method == 'POST' and request.POST.get('empaque'):
        empaque = request.POST.get('empaque')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        try:
            app = zetoneApp()
            cursor = app.cursor()
            sql =("SELECT Empaque, CONVERT(varchar(10), Fecha, 103) AS Fecha, CONVERT(char(5), Hora) AS Hora, MAX(Fruto) AS Frutos")
            cursor.execute(sql)
            consulta = cursor.fetchall()
            if consulta:
                lista = []
                for i in consulta:
                    hora = str(i[0])
                    presion = str(i[1])
                    result = {'hora': hora, 'presion': presion}
                    lista.append(result)
                jsonList = json.dumps({'message': 'Success', 'listado':lista}) 
                return JsonResponse(jsonList, safe=False)
            else:
                jsonList = json.dumps({'message': 'Not Found'}) 
                return JsonResponse(jsonList, safe=False)
        except Exception as e:
            error = str(e)
            jsonList = json.dumps({'error': error}) 
            return JsonResponse(jsonList, safe=False)
        finally:
            cursor.close()
            app.close()


@csrf_exempt
def pruebas_sql(request):
    if request.method == 'POST' and request.POST.get('legajo'):
        legajo = request.POST.get('legajo')
        try:
            registro = []
            ZT = ZetoneTime()
            cursorZT = ZT.cursor()
            sql_consulta = ("SELECT DISTINCT\n" +
                                         "LEFT(CONVERT(varchar, iclock_transaction_1.punch_time, 108), 2) AS soloHora, iclock_transaction_1.emp_code AS Legajo, LEFT(Legajos.Nombre, 28) AS Nombre, CONVERT(varchar(10), iclock_transaction_1.punch_time, 103) AS Fecha, \n" +
                                         "CONVERT(varchar, iclock_transaction_1.punch_time, 108) AS Hora, iclock_transaction_1.punch_time AS FechaHora\n" +
                         "FROM            servidordb.zkbiotime.dbo.iclock_transaction AS iclock_transaction_1 INNER JOIN\n" +
                                                 "Legajos ON iclock_transaction_1.emp_code = Legajos.Legajos\n" +
                         "WHERE      iclock_transaction_1.emp_code = '"+str(legajo)+"' AND TRY_CONVERT(DATE, iclock_transaction_1.punch_time) >= '20/03/2023' AND TRY_CONVERT(DATE, iclock_transaction_1.punch_time) <= '21/03/2023' AND \n" +
                                                     "(iclock_transaction_1.emp_code > '100099')\n" +
                         "ORDER BY Legajo, iclock_transaction_1.punch_time")
            cursorZT.execute(sql_consulta)
            consulta = cursorZT.fetchall()
            if consulta:
                for i in consulta:
                    resultado = {'legajo': str(i[1]), 'nombre': str(i[2]), 'fecha':str(i[3]), 'hora': str(i[4])}
                    registro.append(resultado)
                #print(registro)
                jsonList = json.dumps({'message':'Success', 'registros': registro}) 
                return JsonResponse({'message':'Success', 'registros': registro})
            
        except Exception as e:
            error = 'Error: ' + str(e)
            jsonList = json.dumps({'message':error}) 
            return JsonResponse(jsonList, safe=False)
        finally:
            cursorZT.close()
            ZT.close()



############## REPORTES DE CALIDAD EMPAQUE ##########



# NEXTCLOUD_URL = 'http://191.97.47.105/remote.php/webdav/Imagenes-Calidad/'
# NEXTCLOUD_USER = 'jchambi@zetone.com.ar'
# NEXTCLOUD_PASSWORD = 'Sideswipe348'

# def upload_to_nextcloud(file_path, file_name):
#     url = NEXTCLOUD_URL + file_name
#     with open(file_path, 'rb') as file_data:
#         response = requests.put(
#             url,
#             data=file_data,
#             auth=HTTPBasicAuth(NEXTCLOUD_USER, NEXTCLOUD_PASSWORD)
#         )
#     if response.status_code == 201:
#         return True, url    
#     else:
#         return False, response.content


# @csrf_exempt
# def upload_image_from_directory(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body.decode('utf-8'))
#             if 'filename' in data:
#                 file_name = data['filename']
#                 directory_path = 'App/API/media/images/Calidad/reportes_empaque/'  # Cambia esto al directorio correcto
#                 file_path = os.path.join(directory_path, file_name)                
#                 if os.path.exists(file_path):
#                     success, result = upload_to_nextcloud(file_path, file_name)
#                     if success:
#                         return JsonResponse({'status': 'success', 'url': result})
#                     else:
#                         return JsonResponse({'status': 'error', 'message': result})
#                 else:
#                     return JsonResponse({'status': 'error', 'message': 'File not found'})
#             else:
#                 return JsonResponse({'status': 'error', 'message': 'Invalid request: filename not found'})
#         except json.JSONDecodeError as e:
#             return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'})
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        if 'image' in data and 'filename' in data:
            image_data = data['image']
            file_name = data['filename']
            image_decoded = base64.b64decode(image_data)
            
            file_path = f'/tmp/{file_name}'
            with open(file_path, 'wb') as temp_file:
                temp_file.write(image_decoded)
            
            success, result = upload_to_nextcloud(file_path, file_name)
            os.remove(file_path) 

            if success:
                return JsonResponse({'status': 'success', 'url': result})
            else:
                return JsonResponse({'status': 'error', 'message': result})
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})





NEXTCLOUD_URL = 'http://191.97.47.114/remote.php/webdav/Imagenes-Calidad/'
NEXTCLOUD_USER = 'jchambi@zetone.com.ar'
NEXTCLOUD_PASSWORD = 'Sideswipe348'

def upload_to_nextcloud(file_path, file_name):
    url = NEXTCLOUD_URL + file_name
    with open(file_path, 'rb') as file_data:
        response = requests.put(
            url,
            data=file_data,
            auth=HTTPBasicAuth(NEXTCLOUD_USER, NEXTCLOUD_PASSWORD)
        )
    
    if response.status_code == 201:
        print("ESCRIBE")
        public_link = generate_public_link(file_name)
        if public_link:
            return True, public_link
        else:
            return False, 'Error al generar el enlace público'
    elif response.status_code == 204:
        print("SOBRE-ESCRIBE")
        public_link = generate_public_link(file_name)
        if public_link:
            return True, public_link
        else:
            return False, 'Error al generar el enlace público'
    else:
        return False, response.content.decode('utf-8')

def generate_public_link(file_name):
    params = {
        'shareType': 3,  # Enlace público
        'permissions': 1  # Solo lectura
    }
    headers = {
        'OCS-APIRequest': 'true',
        'Content-Type': 'application/json'
    }
    share_url = 'http://191.97.47.114/ocs/v2.php/apps/files_sharing/api/v1/shares/'
    response = requests.post(share_url, auth=HTTPBasicAuth(NEXTCLOUD_USER, NEXTCLOUD_PASSWORD), headers=headers, params=params)
    if response.status_code == 200:
        share_data = response.json()
        if 'ocs' in share_data and 'data' in share_data['ocs']:
            return share_data['ocs']['data']['url']
    return None

@csrf_exempt
def upload_image_from_directory(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            if 'filename' in data:
                file_name = data['filename']
                directory_path = 'App/API/media/images/Calidad/reportes_empaque/'  # Directorio donde está la imagen
                file_path = os.path.join(directory_path, file_name)
                
                if os.path.exists(file_path):
                    success, result = upload_to_nextcloud(file_path, file_name)
                    if success:
                        return JsonResponse({'status': 'success', 'url': result})
                    else:
                        return JsonResponse({'status': 'error', 'message': result})
                else:
                    return JsonResponse({'status': 'error', 'message': 'File not found'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid request: filename not found'})
        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})















