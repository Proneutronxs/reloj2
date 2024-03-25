from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import datetime 

from django.db import connections
from django.http import JsonResponse

# Create your views here.

def rrhh(request):
    return render (request, 'RRHH/inicio/index.html')

def departamentos(request):
    return render (request, 'RRHH/Departamentos/departamentos.html')

def horarios(request):
    return render (request, 'RRHH/Horarios/horarios.html')

@csrf_exempt
def llamaDepartamentos(request):
    if request.method == 'GET':
        try:
            with connections['PS_Time'].cursor() as cursor:
                sql = "SELECT ID_Departamento AS ID, Departamento AS DEPTO FROM P_Departamentos ORDER BY Departamento"
                cursor.execute(sql)
                consulta = cursor.fetchall()
                if consulta:
                    data = []
                    for i in consulta:
                        idDepto = str(i[0])
                        nombre = str(i[1])
                        datos = {'idDepto':idDepto, 'nombre':nombre}
                        data.append(datos)
                    return JsonResponse({'Message': 'Success', 'Datos': data})
                else:
                    data = "No se encontrarón Departamentos."
                    return JsonResponse({'Message': 'Error', 'Nota': data})
        except Exception as e:
            data = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': data})
        finally:
            cursor.close()
            connections['PS_Time'].close()
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})


@csrf_exempt
def guardaDepartamento(request):
    if request.method == 'POST':
        departamento = str(request.POST.get('nombreDepto')).upper()
        try:
            with connections['PS_Time'].cursor() as cursor:
                sql = "INSERT INTO P_Departamentos (Departamento) VALUES (%s)"
                cursor.execute(sql,[departamento])

            data = "El Departamento se guardó correctamente."
            return JsonResponse({'Message': 'Success', 'Nota': data})
        except Exception as e:
            data = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': data})
        finally:
            cursor.close()
            connections['PS_Time'].close()
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})
    

@csrf_exempt
def guardaTurno(request):
    if request.method == 'POST':
        tipoHorario = request.POST.get('ComboxTipoHorario')
        descripcionTurno = request.POST.get('descripcionTurno')
        if tipoHorario == '1':
            entrada = request.POST.get('entrada')
            salida = request.POST.get('salida')
            try:
                with connections['PS_Time'].cursor() as cursor:
                    sql = "INSERT INTO P_Turnos (ID_Horario, DescripTurno, H1, H2) VALUES (%s,%s,%s,%s)"
                    cursor.execute(sql, [tipoHorario, descripcionTurno, entrada, salida])
                data = "El Departamento se guardó correctamente."
                return JsonResponse({'Message': 'Success', 'Nota': data})
            except Exception as e:
                data = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': data})
            finally:
                cursor.close()
                connections['PS_Time'].close()
        else:
            entradaMañana = request.POST.get('entrada-mañana')
            salidaMañana = request.POST.get('salida-mañana')
            entradaTarde = request.POST.get('entrada-tarde')
            salidaTarde = request.POST.get('salida-tarde')
            try:
                with connections['PS_Time'].cursor() as cursor:
                    sql = "INSERT INTO P_Turnos (ID_Horario, DescripTurno, H1, H2, H3, H4) VALUES (%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql, [tipoHorario, descripcionTurno, entradaMañana, salidaMañana, entradaTarde, salidaTarde])
                data = "El Departamento se guardó correctamente."
                return JsonResponse({'Message': 'Success', 'Nota': data})
            except Exception as e:
                data = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': data})
            finally:
                cursor.close()
                connections['PS_Time'].close()
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})
    

@csrf_exempt
def llamaLegajos_Departamentos(request):
    if request.method == 'POST':
        tipoSelector = request.POST.get('ComboxAsignarPor')
        if tipoSelector == 'D':
            try:
                with connections['PS_Time'].cursor() as cursor:
                    sql = "SELECT ID_Departamento AS ID, Departamento AS DEPTO FROM P_Departamentos ORDER BY Departamento"
                    cursor.execute(sql)
                    consulta = cursor.fetchall()
                    if consulta:
                        data = []
                        for i in consulta:
                            idDepto = str(i[0])
                            departamento = str(i[1])
                            datos = {'idDepto':idDepto, 'departamento':departamento}
                            data.append(datos)
                        return JsonResponse({'Message': 'Success', 'Tipo':'Departamentos', 'Datos': data})
                    else:
                        data = "No se encontrarón Departamentos."
                        return JsonResponse({'Message': 'Error', 'Nota': data})
            except Exception as e:
                data = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': data})
            finally:
                cursor.close()
                connections['PS_Time'].close()
        elif tipoSelector == 'L':
            try:
                with connections['PS_Time'].cursor() as cursor:
                    sql = "SELECT        P_Legajos.Legajo AS LEGAJO, CONVERT(VARCHAR(22), P_Legajos.Nombres) AS NOMBRES, P_Departamentos.Departamento AS DEPARTAMENTO, " \
                                            "ISNULL(P_Turnos.DescripTurno, '----') AS HORARIO " \
                            "FROM            P_Legajos INNER JOIN " \
                                                    "P_Departamentos ON P_Legajos.CodDepto = P_Departamentos.ID_Departamento LEFT JOIN " \
                                                    "P_Turnos ON P_Legajos.CodHorario = P_Turnos.ID_Turnos " \
                            "WHERE        (P_Legajos.EstadoActivo = '1') " \
                            "ORDER BY P_Legajos.Nombres"
                    cursor.execute(sql)
                    consulta = cursor.fetchall()
                    if consulta:
                        data = []
                        for i in consulta:
                            legajo = str(i[0])
                            nombre = str(i[1])
                            departamento = str(i[2])
                            horario = str(i[3])
                            datos = {'legajo':legajo, 'nombre':nombre, 'departamento':departamento, 'horario':horario}
                            data.append(datos)
                        return JsonResponse({'Message': 'Success', 'Tipo':'Legajos', 'Datos': data})
                    else:
                        data = "No se encontrarón Empleados."
                        return JsonResponse({'Message': 'Error', 'Nota': data})
            except Exception as e:
                data = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': data})
            finally:
                cursor.close()
                connections['PS_Time'].close()
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})


@csrf_exempt
def llamaTurnosHorarios(request):
    if request.method == 'GET':
        try:
            with connections['PS_Time'].cursor() as cursor:
                sql = "SELECT ID_Turnos AS ID, DescripTurno AS DESCRIPCION FROM P_Turnos ORDER BY DescripTurno"
                cursor.execute(sql)
                consulta = cursor.fetchall()
                if consulta:
                    data = []
                    for i in consulta:
                        idTurno = str(i[0])
                        descripTurno = str(i[1])
                        datos = {'idTurno':idTurno, 'descripTurno':descripTurno}
                        data.append(datos)
                    return JsonResponse({'Message': 'Success', 'Datos': data})
                else:
                    data = "No se encontrarón Turnos Creados."
                    return JsonResponse({'Message': 'Error', 'Nota': data})
        except Exception as e:
            data = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': data})
        finally:
            cursor.close()
            connections['PS_Time'].close()
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})


@csrf_exempt
def guardaFormulario(request):
    if request.method == 'POST':
        comentario = str(request.POST.get('comment')).upper()
        # try:
        #     with connections['PS_Time'].cursor() as cursor:
        #         sql = "INSERT INTO P_Departamentos (Departamento) VALUES (%s)"
        #         cursor.execute(sql,[departamento])

        #     data = "El Departamento se guardó correctamente."
            
        # except Exception as e:
        #     data = str(e)
        #     return JsonResponse({'Message': 'Error', 'Nota': data})
        # finally:
        #     cursor.close()
        #     connections['PS_Time'].close()
        return JsonResponse({'Message': 'Success', 'Nota': comentario})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})


































