from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.http import JsonResponse
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.static import serve
from App.ZTime.conexion import *
from App.Empaque.modelosPDF.modelosPDF import *
import os

from App.Empaque.forms import *
##LOGIN
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def indexEmpaque(request):
    return render (request, 'Empaque/Inicio/index.html')

@login_required
def reportes_camaras(request):
    return render (request, 'Empaque/Reportes/controlCamaras.html')

def fecha_actual():
    hoy = datetime.now()
    dia = hoy.day
    mes = hoy.month
    if hoy.day < 10:
        dia = "0" + str(hoy.day)
    if hoy.month < 10:
        mes = "0" + str(hoy.month)
    return(str(dia) + "/" + str(mes) + "/" + str(hoy.year))


@csrf_exempt
def post_busqueda_reporte_camaras(request):
    form = form_ver_reportes_camara(request.POST)
    if form.is_valid():
        fecha = form.cleaned_data['fechaReporte']
        hora = form.cleaned_data['hora']
        planta = form.cleaned_data['planta']
        try:
            data_principal = []
            ZetoApp = zetoneApp()
            cursorZetoApp = ZetoApp.cursor()
            consulta_data_principal = ("SELECT ID, CONVERT(VARCHAR(10), Fecha, 103) AS Fecha, Hora, Observaciones, Usuario FROM Reporte_Control_Camaras WHERE Fecha='" + str(fecha) + "'")
            cursorZetoApp.execute(consulta_data_principal)
            consulta_general = cursorZetoApp.fetchone()
            if consulta_general:
                data_principal.append(str(consulta_general[0])) ##ID
                data_principal.append(str(consulta_general[1])) ##FECHA
                data_principal.append(str(consulta_general[2])) ##HORA
                data_principal.append(str(consulta_general[3])) ##OBSERVACIONES
                data_principal.append(str(consulta_general[4])) ##USUARIO

                id_reporte = str(data_principal[0])
                fecha = str(data_principal[1])
                hora = str(data_principal[2])
                fecha_name = str(data_principal[1]).replace('/', '')
                hora_name = str(data_principal[2]).replace(':', '')
                lista_user = str(data_principal[4]).split('@')
                user_name = str(lista_user[0])
                consulta_data_camaras = ("SELECT Camara, Especie, Envase, Temperatura FROM Control_Camaras WHERE ID_Reporte='" + id_reporte + "'")
                cursorZetoApp.execute(consulta_data_camaras)
                consulta_camaras = cursorZetoApp.fetchall()
                pdf = control_camaras_PDF()
        
                pdf.alias_nb_pages()
                pdf.add_page()
                pdf.set_font('Times', 'I', 12)
                pdf.text(x=12, y=40, txt= 'Fecha Control: ' + str(data_principal[1]))
                pdf.text(x=65, y=40, txt= 'Hora Control: ' + str(data_principal[2]) + ' Hs.')
                pdf.set_font('Arial', 'B', 10)
                pdf.text(x=16.5, y=286, txt= user_name)
                pdf.text(x=45, y=286, txt= str(fecha_actual))## Traer fecha actual
                pdf.set_font('Arial', 'B', 10)
                pdf.rect(x=10,y=43,w=190,h=5)
                pdf.text(x=16, y=47.5, txt= 'CÁMARA')
                pdf.line(40,43,40,48)
                pdf.text(x=55, y=47.5, txt= 'ESPECIE')
                pdf.line(85,43,85,48)
                pdf.text(x=100, y=47.5, txt= 'ENVASE')
                pdf.line(130,43,130,48)
                pdf.text(x=150, y=47.5, txt= 'TEMPERATURA') 
                if consulta_camaras:
                    for i in consulta_camaras:
                        pdf.set_font('Arial', '', 8)
                        pdf.cell(w=30, h=3, txt= str(i[0]), border='LBR', align='C', fill=0)
                        pdf.cell(w=45, h=3, txt= str(i[1]), border='BR', align='C', fill=0)
                        pdf.cell(w=45, h=3, txt= str(i[2]), border='BR', align='C', fill=0)
                        pdf.multi_cell(w=70, h=3, txt= str(i[3] + ' °C'), border='BR', align='C', fill=0)

                pdf.set_font('Times', 'I', 12)
                pdf.text(x=12, y=40, txt= 'Fecha Control: ' + fecha)
                pdf.text(x=65, y=40, txt= 'Hora Control: ' + hora + ' Hs.')
                pdf.set_font('Arial', 'B', 10)
                pdf.text(x=16.5, y=286, txt= user_name)
                pdf.text(x=45, y=286, txt= str(fecha_actual))## Traer fecha actual    ##OBSERVACIONES
        
                pdf.add_page()
                pdf.set_font('Times', 'I', 12)
                pdf.text(x=12, y=40, txt= 'Fecha Control: ' + str(data_principal[1]))
                pdf.text(x=65, y=40, txt= 'Hora Control: ' + str(data_principal[2]) + ' Hs.')
                pdf.set_font('Arial', 'B', 10)
                pdf.text(x=16.5, y=286, txt= user_name)
                pdf.text(x=45, y=286, txt= str(fecha_actual))## Traer fecha actual
                pdf.rect(x=10,y=43,w=190,h=5)
                pdf.text(x=11, y=46.5, txt= 'OBSERVACIONES:')
                ### CONTRUCTOR DE OBS
                observaciones = str(data_principal[3])
                lista_observaciones = observaciones.split("-")
                for j in lista_observaciones:
                    pdf.set_font('Arial', '', 10)
                    pdf.multi_cell(w=0, h=5, txt= str(j) or "Sin Observaciones", border='LBR', align='L', fill=0)
                ### IMAGENES
                pdf.rect(x=10,y=98,w=190,h=5)
                pdf.set_font('Arial', 'B', 10)
                pdf.text(x=11, y=102, txt= 'IMÁGENES:')

                ##CONSULTA IMAGENES
                consulta_data_images = ("SELECT Fotos FROM Fotos_Control_Camaras WHERE ID_Reporte='" + id_reporte + "'")
                cursorZetoApp.execute(consulta_data_images)
                consulta_images = cursorZetoApp.fetchall()
                if consulta_images:
                    name_decoded_image = []
                    k_index = 0
                    for k in consulta_images:
                        nombre_foto = decode_base64_to_image(k_index,fecha_name, hora_name, id_reporte, k[0])
                        name_decoded_image.append(str(nombre_foto))
                        k_index = k_index + 1
                    valores_x = [10,80,150,10,80,150]
                    valores_y = [105,105,105,190,190,190]
                    cant_images = len(name_decoded_image)
                    if cant_images > 6:
                        cant_images = 6
                    index = 0
                    #for k in name_decoded_image:
                    while index < cant_images:
                        name_image = str(name_decoded_image[index])
                        pdf.image("App/Empaque/data/images/" + name_image, x = valores_x[index], y = valores_y[index], w = 50, h = 82, type = '', link = '')
                        index = index + 1
                    name_pdf = 'Reporte_Cámaras_' + fecha_name + "_" + hora_name + '.pdf'
                    pdf.output('App/Empaque/data/pdf/' + name_pdf, 'F')
                    jsonList = json.dumps({'message': 'Success', 'pdf': name_pdf}) 
                    return JsonResponse(jsonList, safe=False)
            else:
                jsonList = json.dumps({'message': 'No se encontraron Reportes para la fecha: ' + str(fecha)}) 
                return JsonResponse(jsonList, safe=False)
        except Exception as e:
            print(e)
            error = "Ocurrió un error: " + str(e)
            jsonList = json.dumps({'message': error}) 
            return JsonResponse(jsonList, safe=False)
        finally:
            cursorZetoApp.close()
            ZetoApp.close()

    

def descarga_pdf_control_camaras(request, filename):
    filename = 'App/Empaque/data/pdf/' + filename
    if os.path.exists(filename):
        response = serve(request, os.path.basename(filename), os.path.dirname(filename))
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        raise Http404

def modelo():
    try:
        ZetoneApp = zetoneApp()
        cursorZetoneApp = ZetoneApp.cursor()
        Consulta_SQL = ("SELECT nombrePDF FROM Pdf_Generados WHERE nombrePDF='" + str(fecha_sql) + "'")
        cursorZetoneApp.execute(Consulta_SQL)
        consultaPDF = cursorZetoneApp.fetchone()
        if consultaPDF:
            pdf = "Reporte_Camaras_Calidad_" + str(fecha_sql) + ".pdf"
            jsonList = json.dumps({'message':'Success', 'pdf': pdf}) 
            return JsonResponse(jsonList, safe=False)
        else:
            data_camaras = []
            try:
                ZetoApp = zetoneApp()
                cursorZetoApp = ZetoApp.cursor()
                consulta_data_camaras = ("SELECT Fecha, Hora, Observaciones, Usuario FROM Reporte_Control_Camaras WHERE Fecha='" + str(fecha) + "'")
                cursorZetoApp.execute(consulta_data_camaras)
                
            except Exception as e:
                print(e)
                error = str(e)
                jsonList = json.dumps({'message': error}) 
                return JsonResponse(jsonList, safe=False)
            finally:
                cursorZetoApp.close()
                ZetoApp.close()


            jsonList = json.dumps({'message':'Not Found'}) 
            return JsonResponse(jsonList, safe=False)
    except Exception as e:
        print(e)
        error = str(e)
        jsonList = json.dumps({'message': error}) 
        return JsonResponse(jsonList, safe=False)
    finally:
        cursorZetoneApp.close()
        ZetoneApp.close()


def recolecta_horas_control_camaras(request, fecha):
    try:
        ZetoneApp = zetoneApp()
        cursorZetoneApp = ZetoneApp.cursor()
        Consulta_SQL = ("SELECT Hora FROM Reporte_Control_Camaras WHERE Fecha='" + str(fecha) + "'")
        cursorZetoneApp.execute(Consulta_SQL)
        consulta_horas = cursorZetoneApp.fetchall()
        if consulta_horas:
            lista_horas = []
            for i in consulta_horas:
                lista_horas.append(i)
                print(i)
        else:
            jsonList = json.dumps({'message':'No se encontraron reportes'}) 
            return JsonResponse(jsonList, safe=False)
            
    except Exception as e:
        print(e)
        error = str(e)
        jsonList = json.dumps({'message': error}) 
        return JsonResponse(jsonList, safe=False)
    finally:
        cursorZetoneApp.close()
        ZetoneApp.close()    