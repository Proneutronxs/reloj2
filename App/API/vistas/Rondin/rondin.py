
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




# PreparedStatement pat = conexionBD().prepareStatement("insert into Registro (sereno,planta,punto,fecha,hora,pasos) values(?,?,?,?,?,?)");


@csrf_exempt
def insert_fichada_rondin(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            datos = json.loads(body)['Data']
            print(datos)
            for item in datos:
                legajo = item['Legajo']
                planta = item['Planta']
                punto = item['Punto']
                fecha = item['Fecha']
                hora = item['Hora']
                paso = item['Paso']
                insertaFichadaSql(legajo,planta,punto,fecha,hora,paso)
            nota = "Los registros se guardaron exitosamente."
            return JsonResponse({'Message': 'Success', 'Nota': nota})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    


def insertaFichadaSql(sereno,planta,punto,fecha,hora,pasos):
    try:
        with connections['MyZetto'].cursor() as cursor:
            sql = "INSERT INTO Registro (sereno,planta,punto,fecha,hora,pasos) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (sereno,planta,punto,fecha,hora,pasos)
            cursor.execute(sql, values)  
    except Exception as e:
        error = str(e)
        print(error)
    finally:
        cursor.close()
        connections['MyZetto'].close()     


# AdminSQLiteOpenHelper dbHelper = new AdminSQLiteOpenHelper(activitydb.this);
# SQLiteDatabase sqlite = dbHelper.getReadableDatabase();
# String[] columns = {"legajo", "punto", "fecha", "hora", "paso"};
# Cursor cursor = sqlite.query("legajos", columns, null, null, null, null, null);

# while (cursor.moveToNext()) {
#     @SuppressLint("Range") String legajo = cursor.getString(cursor.getColumnIndex("legajo"));
#     @SuppressLint("Range") String punto = cursor.getString(cursor.getColumnIndex("punto"));
#     @SuppressLint("Range") String fecha = cursor.getString(cursor.getColumnIndex("fecha"));
#     @SuppressLint("Range") String hora = cursor.getString(cursor.getColumnIndex("hora"));
#     @SuppressLint("Range") String paso = cursor.getString(cursor.getColumnIndex("paso"));
    

#     JSONObject dataObj = new JSONObject();
#     try {
#         //legajo,planta,punto,fecha,hora,paso
#         dataObj.put("Legajo", legajo);
#         dataObj.put("Planta", tb_planta.getText().toString());
#         dataObj.put("Punto", punto);
#         dataObj.put("Fecha", fecha);
#         dataObj.put("Hora", hora);
#         dataObj.put("Paso", paso);

#         dataArray.put(dataObj);
#     } catch (JSONException e) {
#         e.printStackTrace();
#         respuesta = String.valueOf(e);
#     }
# }
# cursor.close();
# dbHelper.close();

# JSONObject requestBody = new JSONObject();
# try {
#     requestBody.put("Data", dataArray);
# } catch (JSONException e) {
#     e.printStackTrace();
#     respuesta = String.valueOf(e);
# }