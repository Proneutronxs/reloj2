
from django.db import connections
from django.http import JsonResponse
from App.ZTime.conexion import *
#import requests
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


# public void guardarPunto(){
#     Calendar c = Calendar.getInstance();

#     SimpleDateFormat df_hora = new SimpleDateFormat("HH:mm:ss");
#     String formattedDate_hora = df_hora.format(c.getTime());

#     SimpleDateFormat fecha = new SimpleDateFormat("yyyy-MM-dd");
#     String solofecha = fecha.format(c.getTime());

#     try {
#         AdminSQLiteOpenHelper dbHelper = new AdminSQLiteOpenHelper(MainActivity.this);
#         SQLiteDatabase sqlite = dbHelper.getWritableDatabase();
#         ContentValues values = new ContentValues();
#         values.put("legajo", num_legajo.getText().toString());
#         values.put("planta", txtplanta.getText().toString());
#         values.put("punto", txt_scan.getText().toString());
#         values.put("fecha", solofecha);
#         values.put("hora", formattedDate_hora);
#         values.put("paso", detector.getText().toString());
#         sqlite.insert("Datos", null, values);

#         Toast.makeText(this, "GUARDADO", Toast.LENGTH_SHORT).show();

#     }catch (Exception e) {

#         Toast.makeText(getApplicationContext(),e.getMessage(), Toast.LENGTH_LONG).show();
#     }
# }



#BaseDeDatos.execSQL("CREATE TABLE Datos(legajo char, planta int, punto char, fecha text, hora text, paso char)");



# E/WindowManager: android.view.WindowLeaked: Activity com.example.myzetto.activitydb has leaked window DecorView@384038[Guardando] that was originally added here
#         at android.view.ViewRootImpl.<init>(ViewRootImpl.java:417)
#         at android.view.WindowManagerGlobal.addView(WindowManagerGlobal.java:331)
#         at android.view.WindowManagerImpl.addView(WindowManagerImpl.java:93)
#         at android.app.Dialog.show(Dialog.java:316)
#         at com.example.myzetto.activitydb.exportar(activitydb.java:121)
#         at java.lang.reflect.Method.invoke(Native Method)
#         at android.view.View$DeclaredOnClickListener.onClick(View.java:4693)
#         at android.view.View.performClick(View.java:5610)
#         at android.view.View$PerformClick.run(View.java:22265)
#         at android.os.Handler.handleCallback(Handler.java:751)
#         at android.os.Handler.dispatchMessage(Handler.java:95)
#         at android.os.Looper.loop(Looper.java:154)
#         at android.app.ActivityThread.main(ActivityThread.java:6077)
#         at java.lang.reflect.Method.invoke(Native Method)
#         at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:866)
#         at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:756)
# E/WindowManager: android.view.WindowLeaked: Activity com.example.myzetto.activitydb has leaked window DecorView@5001d76[Guardando Registros] that was originally added here
#         at android.view.ViewRootImpl.<init>(ViewRootImpl.java:417)
#         at android.view.WindowManagerGlobal.addView(WindowManagerGlobal.java:331)
#         at android.view.WindowManagerImpl.addView(WindowManagerImpl.java:93)
#         at android.app.Dialog.show(Dialog.java:316)
#         at com.example.myzetto.activitydb$crearBodyRegistros.onPreExecute(activitydb.java:348)
#         at android.os.AsyncTask.executeOnExecutor(AsyncTask.java:613)
#         at android.os.AsyncTask.execute(AsyncTask.java:560)
#         at com.example.myzetto.activitydb.exportar(activitydb.java:141)
#         at java.lang.reflect.Method.invoke(Native Method)
#         at android.view.View$DeclaredOnClickListener.onClick(View.java:4693)
#         at android.view.View.performClick(View.java:5610)
#         at android.view.View$PerformClick.run(View.java:22265)
#         at android.os.Handler.handleCallback(Handler.java:751)
#         at android.os.Handler.dispatchMessage(Handler.java:95)
#         at android.os.Looper.loop(Looper.java:154)
#         at android.app.ActivityThread.main(ActivityThread.java:6077)
#         at java.lang.reflect.Method.invoke(Native Method)
#         at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:866)
#         at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:756)


# public void exportar(View view) {
#         ProgressDialog tProgress = new ProgressDialog(activitydb.this);
#         tProgress.setMessage("Espere por favor ...");
#         tProgress.setTitle("Guardando");
#         tProgress.show();
#         new crearBodyRegistros(new VolleyCallback2() {
#             @Override
#             public void onSuccess(String response) {
#                 if (response.equals("Success")){
#                     tProgress.dismiss();
#                     error(response);
#                 }else {
#                     tProgress.dismiss();
#                     error(response);

#                 }
#             }
#             @Override
#             public void onError() {
#                 tProgress.dismiss();
#                 String e = "No se estableció la conexión, por favor verifique su conexión a internet.";
#                 error(e);

#             }
#         }, tProgress).execute();
#         //new exportar().execute();
#     }


# private class crearBodyRegistros extends AsyncTask<String, Void, Void> {
#         private ProgressDialog tProgress = null;
#         private VolleyCallback2 callback;
#         private String respuesta;
#         public crearBodyRegistros(VolleyCallback2 callback, ProgressDialog tProgress) {
#             this.callback = callback;
#             this.tProgress = tProgress;
#         }
#         @Override
#         protected void onPreExecute() {
#             super.onPreExecute();
#             tProgress = new ProgressDialog(activitydb.this);
#             tProgress.setMessage("Espere por favor ...");
#             tProgress.setTitle("Guardando Registros");
#             tProgress.show();
#         }

#         @Override
#         protected Void doInBackground(String... strings) {

#             RequestQueue requestQueue = Volley.newRequestQueue(activitydb.this);
#             String url = "http://191.97.47.105:8000/api/rondin-empaque/recibe-fichadas/";
#             JSONArray dataArray = new JSONArray();

#             AdminSQLiteOpenHelper dbHelper = new AdminSQLiteOpenHelper(activitydb.this);
#             SQLiteDatabase sqlite = dbHelper.getReadableDatabase();
#             String[] columns = {"legajo", "punto", "fecha", "hora", "paso"};
#             Cursor cursor = sqlite.query("legajos", columns, null, null, null, null, null);

#             while (cursor.moveToNext()) {
#                 @SuppressLint("Range") String legajo = cursor.getString(cursor.getColumnIndex("legajo"));
#                 @SuppressLint("Range") String punto = cursor.getString(cursor.getColumnIndex("punto"));
#                 @SuppressLint("Range") String fecha = cursor.getString(cursor.getColumnIndex("fecha"));
#                 @SuppressLint("Range") String hora = cursor.getString(cursor.getColumnIndex("hora"));
#                 @SuppressLint("Range") String paso = cursor.getString(cursor.getColumnIndex("paso"));


#                 JSONObject dataObj = new JSONObject();
#                 try {
#                     //legajo,planta,punto,fecha,hora,paso
#                     dataObj.put("Legajo", legajo);
#                     dataObj.put("Planta", tb_planta.getText().toString());
#                     dataObj.put("Punto", punto);
#                     dataObj.put("Fecha", fecha);
#                     dataObj.put("Hora", hora);
#                     dataObj.put("Paso", paso);

#                     dataArray.put(dataObj);
#                 } catch (JSONException e) {
#                     e.printStackTrace();
#                     respuesta = String.valueOf(e);
#                 }
#             }
#             cursor.close();
#             dbHelper.close();

#             JSONObject requestBody = new JSONObject();
#             try {
#                 requestBody.put("Data", dataArray);
#             } catch (JSONException e) {
#                 e.printStackTrace();
#                 respuesta = String.valueOf(e);
#             }

#             JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, url, requestBody,
#                     new Response.Listener<JSONObject>() {
#                         @Override
#                         public void onResponse(JSONObject response) {
#                             try {
#                                 String message = response.getString("Message");
#                                 if (message.equals("Success")) {
#                                     String nota = response.getString("Nota");
#                                     respuesta = nota;
#                                 } else {
#                                     String nota = response.getString("Nota");
#                                     respuesta = nota;
#                                 }
#                             } catch (JSONException e) {
#                                 e.printStackTrace();
#                                 respuesta = String.valueOf(e);
#                             }
#                             callback.onSuccess(respuesta);
#                         }
#                     },
#                     new Response.ErrorListener() {
#                         @Override
#                         public void onErrorResponse(VolleyError error) {
#                             error.printStackTrace();
#                             respuesta = String.valueOf(error);
#                             callback.onError();
#                         }
#                     });

#             requestQueue.add(jsonObjectRequest);
#             return null;
#         }

#         @Override
#         protected void onPostExecute(Void result) {
#             tProgress.dismiss();
#         }
#     }
# E/SQLiteLog: (1) no such table: legajos
# E/AndroidRuntime: FATAL EXCEPTION: AsyncTask #1
#     Process: com.example.myzetto, PID: 5830
#     java.lang.RuntimeException: An error occurred while executing doInBackground()
#         at android.os.AsyncTask$3.done(AsyncTask.java:318)
#         at java.util.concurrent.FutureTask.finishCompletion(FutureTask.java:354)
#         at java.util.concurrent.FutureTask.setException(FutureTask.java:223)
#         at java.util.concurrent.FutureTask.run(FutureTask.java:242)
#         at android.os.AsyncTask$SerialExecutor$1.run(AsyncTask.java:243)
#         at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1133)
#         at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:607)
#         at java.lang.Thread.run(Thread.java:761)
#      Caused by: android.database.sqlite.SQLiteException: no such table: legajos (code 1): , while compiling: SELECT legajo, punto, fecha, hora, paso FROM legajos
#         at android.database.sqlite.SQLiteConnection.nativePrepareStatement(Native Method)
#         at android.database.sqlite.SQLiteConnection.acquirePreparedStatement(SQLiteConnection.java:889)
#         at android.database.sqlite.SQLiteConnection.prepare(SQLiteConnection.java:500)
#         at android.database.sqlite.SQLiteSession.prepare(SQLiteSession.java:588)
#         at android.database.sqlite.SQLiteProgram.<init>(SQLiteProgram.java:58)
#         at android.database.sqlite.SQLiteQuery.<init>(SQLiteQuery.java:37)
#         at android.database.sqlite.SQLiteDirectCursorDriver.query(SQLiteDirectCursorDriver.java:44)
#         at android.database.sqlite.SQLiteDatabase.rawQueryWithFactory(SQLiteDatabase.java:1318)
#         at android.database.sqlite.SQLiteDatabase.queryWithFactory(SQLiteDatabase.java:1165)
#         at android.database.sqlite.SQLiteDatabase.query(SQLiteDatabase.java:1036)
#         at android.database.sqlite.SQLiteDatabase.query(SQLiteDatabase.java:1204)
#         at com.example.myzetto.activitydb$crearBodyRegistros.doInBackground(activitydb.java:357)
#         at com.example.myzetto.activitydb$crearBodyRegistros.doInBackground(activitydb.java:334)
#         at android.os.AsyncTask$2.call(AsyncTask.java:304)
