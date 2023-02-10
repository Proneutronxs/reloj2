from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from App.ZTime.forms import *
from App.ZTime.conexion import *
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
import mimetypes
import os

# Create your views here.

def fechaNombre(fecha):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    now = datetime.now()
    #stringFecha = str(now.day) + "-" + str(now.month) + "-" + str(now.year)
    di = datetime.strptime(str(fecha), "%d/%m/%Y")
    dianum = now.day
    mes = meses[now.month]
    año = now.year
    diaNombre = dias[di.weekday()]
    #fecha = (diaNombre + ", " + str(dianum) + " de " + str(mes) + " del " + str(año))
    return diaNombre

### RENDERIZADO 

def index(request):
    return render (request, 'ZTime/inicio/index.html')

def renderCalcHoras(resquest):
    return render (resquest, 'ZTime/registros/viewRegister.html')


def renderVerRegistros(resquest):
    return render (resquest, 'ZTime/registros/ver.html')

# def calcRegistros(request):
#     if request.method == 'POST':
#         form = form_ver_registros(request.POST)
#         legajo = request.POST.get('legajo', 1)
#         print(legajo)
#         if form.is_valid():
#             print("validó?")
#             legajo = form.cleaned_data['legajo']
#             departamento = form.cleaned_data['departamento']
#             desde = form.cleaned_data['desde']
#             hasta = form.cleaned_data['hasta']
#             desdeSql = datetime.strptime(str(desde), "%Y-%m-%d").strftime("%d/%m/%Y")
#             soloDiaDesde = datetime.strptime(str(desde), "%Y-%m-%d").strftime("%d")
#             mesAñoDesde = datetime.strptime(str(desde), "%Y-%m-%d").strftime("%m/%Y")
#             hastaSql = datetime.strptime(str(hasta), "%Y-%m-%d").strftime("%d/%m/%Y")
#             soloDiaHasta = datetime.strptime(str(hasta), "%Y-%m-%d").strftime("%d")
#             mesAñoHasta = datetime.strptime(str(hasta), "%Y-%m-%d").strftime("%m/%Y")
#             try:
#                 registro = []
#                 ZT = ZetoneTime()
#                 cursorZT = ZT.cursor()
#                 sql4 = ("SELECT Legajo, Nombre, Fecha, F1, F2, F3, F4, HorasF1F2, HorasF3F4, HorasDeMas\n" +
#                         "FROM TemporalHoras\n" +
#                         "WHERE Legajo = '" + str(legajo) + "' AND Fecha >= '"+ str(desdeSql) +"' AND Fecha <= '"+ str(hastaSql) +"'")
#                 cursorZT.execute(sql4)
#                 consultaZT = cursorZT.fetchall()
#                 if consultaZT:
#                     for i in consultaZT:
#                         dia = fechaNombre(str(i[2]))
#                         if i[3] == None:
#                             i[3] = "-"
#                         if i[4] == None:
#                             i[4] = "-"
#                         if i[5] == None:
#                             i[5] = "-"
#                         if i[6] == None:
#                             i[6] = "-"
#                         if i[7] == None:
#                             i[7] = "-"
#                         if i[8] == None:
#                             i[8] = "-"
#                         if i[9] == None:
#                             i[9] = "-"
#                         resultado = {'legajo': str(i[0]), 'nombre': i[1], 'fecha': i[2], 'f1': i[3], 'f2': i[4], 'f3': i[5], 'f4': i[6], 'dia': dia, 'hm':i[7], 'ht': i[8], 'ex': i[9]}
#                         registro.append(resultado)
#                     jsonList = json.dumps(registro)
#                     print(jsonList)
#                     print("hola?")
#                     return render (request, 'ZTime/registros/viewRegister.html', {'registroHtml': registro})
#                 else:
#                     print("no hay nada")
#                     return render (request, 'ZTime/registros/viewRegister.html')
#             except Exception as e:
#                 print("Error")
#                 print(e)
            
#         else:
#             departamento = form.cleaned_data['departamento']
#             desde = form.cleaned_data['desde']
#             hasta = form.cleaned_data['hasta']
#             desdeSql = datetime.strptime(str(desde), "%Y-%m-%d").strftime("%d/%m/%Y")
#             soloDiaDesde = datetime.strptime(str(desde), "%Y-%m-%d").strftime("%d")
#             hastaSql = datetime.strptime(str(hasta), "%Y-%m-%d").strftime("%d/%m/%Y")
#             soloDiaHasta = datetime.strptime(str(hasta), "%Y-%m-%d").strftime("%d")

#             print(soloDiaDesde)
#             print(soloDiaHasta)
#             print(legajo)
#             print(departamento)
#             print(desdeSql)
#             print(hastaSql)
#             print("No validó?")


#             if departamento == "Todos":
#                 registro = []
#                 try:
#                     ZT = ZetoneTime()
#                     cursorZT = ZT.cursor()
#                     sql4 = ("SELECT Legajo, Nombre, Fecha, F1, F2, F3,F4, HorasF1F2, HorasF3F4, HorasDeMas\n" +
#                             "FROM TemporalHoras\n" +
#                             "WHERE Fecha >= '"+ str(desdeSql) +"' AND Fecha <= '"+ str(hastaSql) +"'\n" +
#                             "ORDER BY Legajo, Fecha , Nombre")
#                     cursorZT.execute(sql4)
#                     consultaZT = cursorZT.fetchall()
#                     if consultaZT:
#                         for i in consultaZT:
#                             dia = fechaNombre(str(i[2]))
#                             if i[3] == None:
#                                 i[3] = "-"
#                             if i[4] == None:
#                                 i[4] = "-"
#                             if i[5] == None:
#                                 i[5] = "-"
#                             if i[6] == None:
#                                 i[6] = "-"
#                             if i[7] == None:
#                                 i[7] = "-"
#                             if i[8] == None:
#                                 i[8] = "-"
#                             if i[9] == None:
#                                 i[9] = "-"
#                             resultado = {'legajo': i[0], 'nombre': i[1], 'fecha': i[2], 'f1': i[3], 'f2': i[4], 'f3': i[5], 'f4': i[6], 'dia': dia, 'hm':i[7], 'ht': i[8], 'ex': i[9]}
#                             registro.append(resultado)
#                         #print(registro)
#                         print("hola?")
#                     return render (request, 'ZTime/registros/viewRegister.html', {'registroHtml': registro})
#                 except Exception as e:
#                     print("Error")
#                     print(e)
#             else:
#                 return render (request, 'ZTime/registros/viewRegister.html')
#     else:
#         print("renderiza")
#         return render (request, 'ZTime/registros/viewRegister.html')


# def verRegistros(request):
#     if request.method == 'POST':
#         form = form_ver_registros(request.POST)
#         legajo = request.POST.get('legajo', 1)
#         print(legajo)
#         if form.is_valid():
#             print("validó?")
#             legajo = form.cleaned_data['legajo']
#             departamento = form.cleaned_data['departamento']
#             desde = form.cleaned_data['desde']
#             hasta = form.cleaned_data['hasta']
#             desdeSql = datetime.strptime(str(desde), "%Y-%m-%d").strftime("%d/%m/%Y")
#             hastaSql = datetime.strptime(str(hasta), "%Y-%m-%d").strftime("%d/%m/%Y")
#             try:
#                 registro = []
#                 ZT = ZetoneTime()
#                 cursorZT = ZT.cursor()
#                 sql4 = ("SELECT DISTINCT\n" +
#                                         "LEFT(CONVERT(varchar, iclock_transaction_1.punch_time, 108), 2) AS soloHora, iclock_transaction_1.emp_code AS Legajo, LEFT(Legajos.Nombre, 28) AS Nombre, CONVERT(varchar(10), iclock_transaction_1.punch_time, 103) AS Fecha, \n" +
#                                         "CONVERT(varchar, iclock_transaction_1.punch_time, 108) AS Hora, iclock_transaction_1.punch_time AS FechaHora\n" +
#                         "FROM            servidordb.zkbiotime.dbo.iclock_transaction AS iclock_transaction_1 INNER JOIN\n" +
#                                                 "Legajos ON iclock_transaction_1.emp_code = Legajos.Legajos\n" +
#                         "WHERE      iclock_transaction_1.emp_code = '"+str(legajo)+"' AND (CONVERT(varchar(10), iclock_transaction_1.punch_time, 103) >= '"+str(desdeSql)+"') AND (CONVERT(varchar(10), iclock_transaction_1.punch_time, 103) <= '"+str(hastaSql)+"') AND \n" +
#                                                     "(iclock_transaction_1.emp_code > '100099')\n" +
#                         "ORDER BY Legajo, FechaHora")
#                 cursorZT.execute(sql4)
#                 consultaZT = cursorZT.fetchall()
#                 if consultaZT:
#                     for i in consultaZT:
#                         dia = fechaNombre(str(i[3]))
#                         resultado = {'legajo': i[1], 'nombre': i[2], 'fecha': i[3], 'hora': i[4], 'dia': dia}
#                         registro.append(resultado)
#                     #print(registro)
#                     print("hola?")
#                     return render (request, 'ZTime/registros/ver.html', {'registroHtml': registro})
#                 else:
#                     print("no hay nada")
#                     return render (request, 'ZTime/registros/ver.html')
#             except Exception as e:
#                 print("Error")
#                 print(e)
#         else:
#             departamento = form.cleaned_data['departamento']
#             desde = form.cleaned_data['desde']
#             hasta = form.cleaned_data['hasta']
#             desdeSql = datetime.strptime(str(desde), "%Y-%m-%d").strftime("%d/%m/%Y")
#             hastaSql = datetime.strptime(str(hasta), "%Y-%m-%d").strftime("%d/%m/%Y")
#             print("no valido")
#             if departamento == "Todos":
#                 print("")
#                 try:
#                     registro = []
#                     ZT = ZetoneTime()
#                     cursorZT = ZT.cursor()
#                     sql4 = ("SELECT DISTINCT\n" +
#                                             "LEFT(CONVERT(varchar, iclock_transaction_1.punch_time, 108), 2) AS soloHora, iclock_transaction_1.emp_code AS Legajo, LEFT(Legajos.Nombre, 28) AS Nombre, CONVERT(varchar(10), iclock_transaction_1.punch_time, 103) AS Fecha, \n" +
#                                             "CONVERT(varchar, iclock_transaction_1.punch_time, 108) AS Hora, iclock_transaction_1.punch_time AS FechaHora\n" +
#                             "FROM            servidordb.zkbiotime.dbo.iclock_transaction AS iclock_transaction_1 INNER JOIN\n" +
#                                                     "Legajos ON iclock_transaction_1.emp_code = Legajos.Legajos\n" +
#                             "WHERE      (CONVERT(varchar(10), iclock_transaction_1.punch_time, 103) >= '"+str(desdeSql)+"') AND (CONVERT(varchar(10), iclock_transaction_1.punch_time, 103) <= '"+str(hastaSql)+"') AND \n" +
#                                                         "(iclock_transaction_1.emp_code > '100099')\n" +
#                             "ORDER BY Legajo, FechaHora")
#                     cursorZT.execute(sql4)
#                     consultaZT = cursorZT.fetchall()
#                     if consultaZT:
#                         for i in consultaZT:
#                             dia = fechaNombre(str(i[3]))
#                             resultado = {'legajo': i[1], 'nombre': i[2], 'fecha': i[3], 'hora': i[4], 'dia': dia}
#                             registro.append(resultado)
#                         #print(registro)
#                         print("hola?")
#                         return render (request, 'ZTime/registros/ver.html', {'registroHtml': registro})
#                     else:
#                         print("no hay nada")
#                         return render (request, 'ZTime/registros/ver.html')
#                 except Exception as e:
#                     print("Error")
#                     print(e)
#             elif departamento == "Empaque":
#                 print("")
#                 try:
#                     registro = []
#                     ZT = ZetoneTime()
#                     cursorZT = ZT.cursor()
#                     sql4 = ("SELECT DISTINCT \n" +
#                                                     "LEFT(CONVERT(varchar, iclock_transaction_1.punch_time, 108), 2) AS soloHora, iclock_transaction_1.emp_code AS Legajo, LEFT(Legajos.Nombre, 28) AS Nombre, CONVERT(varchar(10), iclock_transaction_1.punch_time, 103) \n" +
#                                                     "AS Fecha, CONVERT(varchar, iclock_transaction_1.punch_time, 108) AS Hora, iclock_transaction_1.punch_time AS FechaHora, Legajos_1.Clase\n" +
#                             "FROM            servidordb.zkbiotime.dbo.iclock_transaction AS iclock_transaction_1 INNER JOIN\n" +
#                                                     "Legajos ON iclock_transaction_1.emp_code = Legajos.Legajos INNER JOIN\n" +
#                                                     "Legajos AS Legajos_1 ON iclock_transaction_1.emp_code = Legajos_1.Legajos\n" +
#                             "WHERE        (CONVERT(varchar(10), iclock_transaction_1.punch_time, 103) >= '"+str(desdeSql)+"') AND (CONVERT(varchar(10), iclock_transaction_1.punch_time, 103) <= '"+str(hastaSql)+"') AND (iclock_transaction_1.emp_code > '100099') AND Legajos.Clase = 'Galpon'\n" +
#                             "ORDER BY Legajo, FechaHora")
#                     cursorZT.execute(sql4)
#                     consultaZT = cursorZT.fetchall()
#                     if consultaZT:
#                         for i in consultaZT:
#                             dia = fechaNombre(str(i[3]))
#                             resultado = {'legajo': i[1], 'nombre': i[2], 'fecha': i[3], 'hora': i[4], 'dia': dia}
#                             registro.append(resultado)
#                         #print(registro)
#                         #print("hola?")
#                         return render (request, 'ZTime/registros/ver.html', {'registroHtml': registro})
#                     else:
#                         #print("no hay nada")
#                         return render (request, 'ZTime/registros/ver.html')
#                 except Exception as e:
#                     print("Error")
#                     print(e)
#     return render (request, 'ZTime/registros/ver.html')

def pruebaHTML(request):
    return render (request, 'prueba/prueba.html')

def prueba(request):
    try:
        ZT = ZetoneTime()
        cursorZT = ZT.cursor()
        sql4 =("SELECT        numero_bulto\n" +
                "FROM            servidordb.Trazabilidad.dbo.Bulto\n" +
                "WHERE Id_bulto = (SELECT MAX(Id_bulto) FROM servidordb.Trazabilidad.dbo.Bulto)")
        cursorZT.execute(sql4)
        consultaZT = cursorZT.fetchall()
        if consultaZT:
            for i in consultaZT:
                print(i[0])
                data = {'bultos': str(i[0])}
                print(data)
            
            cursorZT.commit()
            cursorZT.close()
            ZT.close()
        return JsonResponse(data)
    except Exception as e:
        print("Error")
        print(e)
        data = {'bultos': 'error'}
        return JsonResponse(data)

@csrf_exempt
def calculoHorasJson(request):
    form = form_ver_registros(request.POST)
    if form.is_valid():
        legajo = form.cleaned_data['legajo']
        departamento = form.cleaned_data['departamento']
        desde = form.cleaned_data['desde']
        hasta = form.cleaned_data['hasta']
        print(legajo)
        print(departamento)
        print(desde)
        print(hasta)
        desdeSql = datetime.strptime(str(desde), "%Y-%m-%d").strftime("%d/%m/%Y")
        hastaSql = datetime.strptime(str(hasta), "%Y-%m-%d").strftime("%d/%m/%Y")
        try:
            registro = []
            ZT = ZetoneTime()
            cursorZT = ZT.cursor()
            sql4 = ("SELECT Legajo, Nombre, Fecha, F1, F2, F3, F4, HorasF1F2, HorasF3F4, HorasDeMas\n" +
                    "FROM TemporalHoras\n" +
                    "WHERE Legajo = '" + str(legajo) + "' AND Fecha >= '"+ str(desdeSql) +"' AND Fecha <= '"+ str(hastaSql) +"'")
            cursorZT.execute(sql4)
            consultaZT = cursorZT.fetchall()
            if consultaZT:
                for i in consultaZT:
                    dia = fechaNombre(str(i[2]))
                    if i[3] == None:
                        i[3] = "-"
                    if i[4] == None:
                        i[4] = "-"
                    if i[5] == None:
                        i[5] = "-"
                    if i[6] == None:
                        i[6] = "-"
                    if i[7] == None:
                        i[7] = "-"
                    if i[8] == None:
                        i[8] = "-"
                    if i[9] == None:
                        i[9] = "-"
                    resultado = {'legajo': str(i[0]), 'nombre': i[1], 'dia': dia, 'fecha': i[2], 'f1': i[3], 'f2': i[4], 'f3': i[5], 'f4': i[6], 'hm':i[7], 'ht': i[8], 'ex': i[9]}
                    registro.append(resultado)

                cursorZT.close()
                ZT.close()
                jsonList = json.dumps({'message': 'Success', 'registros':registro}) 
                return JsonResponse(jsonList, safe=False)
            else:
                cursorZT.close()
                ZT.close()
                print("no hay nada")
                jsonList = json.dumps({'message':'Not Found'}) 
                return JsonResponse(jsonList, safe=False)
        except Exception as e:
            print("Error")
            print(e)
            data = [{'info': 'error'}]
            return JsonResponse(data, safe=False)
    else:
        departamento = form.cleaned_data['departamento']
        if departamento == "Seleccione":
            data = [{'info': 'error'}]
            return JsonResponse(data, safe=False)

def downloadRegister(request):
    form = form_export_registros(request.POST)
    
    if form.is_valid():
        legajo = form.cleaned_data['legajo']
        departamento = form.cleaned_data['departamento']
        desde = form.cleaned_data['desde']
        hasta = form.cleaned_data['hasta']
        export = form.cleaned_data['export']
        desdeSql = datetime.strptime(str(desde), "%Y-%m-%d").strftime("%d/%m/%Y")
        hastaSql = datetime.strptime(str(hasta), "%Y-%m-%d").strftime("%d/%m/%Y")
        print(legajo)
        print(departamento)
        print(desdeSql)
        print(hastaSql)
        print(export)
        try:
            Asistencia = ZetoneTime()
            cursor_asis = Asistencia.cursor()
            querySQL = ("SELECT        Temporal.Legajo AS Legajo, DetalleLegajos.Nombre AS Nombre, Temporal.EM AS EntradaMañana, Temporal.SM AS SalidaMañana, Temporal.ET AS EntradaTarde, Temporal.ST AS SalidaTarde, DetalleLegajos.Clase AS Clase, DetalleLegajos.Categoria AS Categoria\n" +
                        "FROM            Temporal INNER JOIN\n" +
                                                "DetalleLegajos ON Temporal.Legajo = DetalleLegajos.Legajo\n" +
                        "ORDER BY DetalleLegajos.Nombre")
            cursor_asis.execute(querySQL)
            consulta_asis = cursor_asis.fetchall()
            if consulta_asis:
                listaLegajo = []
                listaNombre = []
                entradaMañana = []
                salidaMañana = []
                entradaTarde = []
                salidaTarde = []
                listaClase = []
                listaCategoria = []
                for i in consulta_asis:
                    listaLegajo.append(str(i[0]))
                    listaNombre.append(str(i[1]))
                    entradaMañana.append(str(i[2]))
                    salidaMañana.append(str(i[3]))
                    entradaTarde.append(str(i[4]))
                    salidaTarde.append(str(i[5]))
                    listaClase.append(str(i[6]))
                    listaCategoria.append(str(i[7]))
                
                #print(listaHora)

                data_null = {}
                def_null = pd.DataFrame(data_null)
                def_null.to_excel('Reporte_Asistencia_'+ desde +'.xlsx')

                write = pd.ExcelWriter('Reporte_Asistencia_'+ desde +'.xlsx')

                Columnas = {'Legajo': listaLegajo, 'Nombre y Apellido': listaNombre, 'Entrada Mañana': entradaMañana, 'Salida Mañana': salidaMañana, 'Entrada Tarde': entradaTarde, 'Salida Tarde': salidaTarde, 'Sector': listaClase, 'Categoría': listaCategoria}
                df_Columnas = pd.DataFrame(Columnas)

                df_Columnas.to_excel(write, 'Asistencia', index=False)
                write.save()
                write.close()
                Asistencia.close()

        except Exception as e:
            print(e)

        data = [{'info': 'sin Datos'}]
        return JsonResponse(data, safe=False)
    else:
        departamento = form.cleaned_data['departamento']
        if departamento == "Seleccione":
            desde = form.cleaned_data['desde']
            hasta = form.cleaned_data['hasta']
            export = form.cleaned_data['export']
            desdeSql = datetime.strptime(str(desde), "%Y-%m-%d").strftime("%d/%m/%Y")
            hastaSql = datetime.strptime(str(hasta), "%Y-%m-%d").strftime("%d/%m/%Y")
            print(departamento)
            print(desdeSql)
            print(hastaSql)
            print(export)
            Asistencia.close()

            data = [{'info': 'sin Datos'}]
            return JsonResponse(data, safe=False)

    data = [{'info': 'sin Datos'}]
    return JsonResponse(data, safe=False)


def download_Excel(self):

    try:
        f = open('App/ZTime/data/excel/prueba.xlsx', 'rb')
        response = HttpResponse(content=f)
        response['Content-Type'] = 'application/pdf'
        return response
    except Exception as e:
        print(e)
        respuesta = 'Error'
        lista_estado= [{'Info':e, 'Info2': respuesta}]
        estado = [lista_estado]
        return HttpResponse(estado)


def descargar_archivo(request): 
 
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
 
    filename = 'vikosur.pdf'
    filepath = BASE_DIR + '/ZTime/data/excel/' + filename 
 
    path = open(filepath, 'r') 
 
    mime_type, _ = mimetypes.guess_type(filepath)
    
    response = HttpResponse(path, content_type = mime_type)
 
    response['Content-Disposition'] = f"attachment; filename={filename}"
 
    return response


@csrf_exempt
def ver_registros_sin_proceso(request):
    form = form_ver_registros(request.POST)
    if form.is_valid():
        legajo = form.cleaned_data['legajo']
        departamento = form.cleaned_data['departamento']
        desde = form.cleaned_data['desde']
        hasta = form.cleaned_data['hasta']
        print(legajo)
        print(departamento)
        print(desde)
        print(hasta)
        desdeSql = datetime.strptime(str(desde), "%Y-%m-%d").strftime("%d/%m/%Y")
        hastaSql = datetime.strptime(str(hasta), "%Y-%m-%d").strftime("%d/%m/%Y")
        try:
            registro = []
            ZT = ZetoneTime()
            cursorZT = ZT.cursor()
            sql_consulta = ("SELECT DISTINCT\n" +
                                         "LEFT(CONVERT(varchar, iclock_transaction_1.punch_time, 108), 2) AS soloHora, iclock_transaction_1.emp_code AS Legajo, LEFT(Legajos.Nombre, 28) AS Nombre, CONVERT(varchar(10), iclock_transaction_1.punch_time, 103) AS Fecha, \n" +
                                         "CONVERT(varchar, iclock_transaction_1.punch_time, 108) AS Hora, iclock_transaction_1.punch_time AS FechaHora\n" +
                         "FROM            servidordb.zkbiotime.dbo.iclock_transaction AS iclock_transaction_1 INNER JOIN\n" +
                                                 "Legajos ON iclock_transaction_1.emp_code = Legajos.Legajos\n" +
                         "WHERE      iclock_transaction_1.emp_code = '"+str(legajo)+"' AND (CONVERT(varchar(10), iclock_transaction_1.punch_time, 103) >= '"+str(desdeSql)+"') AND (CONVERT(varchar(10), iclock_transaction_1.punch_time, 103) <= '"+str(hastaSql)+"') AND \n" +
                                                     "(iclock_transaction_1.emp_code > '100099')\n" +
                         "ORDER BY Legajo, FechaHora")
            cursorZT.execute(sql_consulta)
            consulta = cursorZT.fetchall()
            if consulta:
                for i in consulta:
                    dia = fechaNombre(str(i[3]))
                    resultado = {'legajo': str(i[1]), 'nombre': str(i[2]), 'dia': dia, 'fecha':str(i[3]), 'hora': str(i[4])}
                    registro.append(resultado)
                print(registro)
                jsonList = json.dumps({'message':'Success', 'registros': registro}) 
                return JsonResponse(jsonList, safe=False)
            else:
                jsonList = json.dumps({'message':'Not Found'}) 
                return JsonResponse(jsonList, safe=False)
        except Exception as e:
            jsonList = json.dumps({'message':'error'}) 
            return JsonResponse(jsonList, safe=False)
        finally:
            cursorZT.close()
            ZT.close()