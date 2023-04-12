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
import matplotlib.pyplot as plt

from App.Empaque.forms import *
##LOGIN
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def indexEmpaque(request):
    return render (request, 'Empaque/Inicio/index.html')

@login_required
def reportes_camaras(request):
    return render (request, 'Empaque/Reportes/reportes.html')

def fecha_actual():
    hoy = datetime.now()
    dia = hoy.day
    mes = hoy.month
    if hoy.day < 10:
        dia = "0" + str(hoy.day)
    if hoy.month < 10:
        mes = "0" + str(hoy.month)
    return(str(dia) + "/" + str(mes) + "/" + str(hoy.year))

def fechaNombre(fecha):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    now = datetime.now()
    #stringFecha = str(now.day) + "-" + str(now.month) + "-" + str(now.year)
    di = datetime.strptime(str(fecha), "%Y-%m-%d")
    dianum = now.day
    mes = meses[now.month]
    año = now.year
    diaNombre = dias[di.weekday()]
    hora_actual = datetime.now().strftime("%H:%M:%S")
    fechaN = (diaNombre + ", " + str(dianum) + " de " + str(mes) + " del " + str(año) + " - " + str(hora_actual) +" Hs.")
    return fechaN

def consultaTopCaja(fecha):
    try:
        conexion = zetoneApp()
        cursor = conexion.cursor()
        sql5 = ("SELECT (SELECT TOP(1)IdCaja FROM DefectosCaja WHERE TRY_CONVERT(DATE, Fecha) ='" + str(fecha) + "') - 5")
        cursor.execute(sql5)
        consulta = cursor.fetchone()
        if consulta:
            id = str(consulta[0])
            return id
        else:
            id = "0"
            return
    except Exception as e:
            print(e)
    finally:
        cursor.close()
        conexion.close()

@csrf_exempt
def post_busqueda_reporte_camaras(request):
    form = form_ver_reportes_camara(request.POST)
    if form.is_valid():
        fecha = form.cleaned_data['fechaReporte']
        Tipo = (form.cleaned_data['hora'])##CAMBIÓ A EMPAQUE
        planta = form.cleaned_data['planta']
        if str(Tipo) == "Control Cámaras":
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
                    consulta_data_camaras = ("SELECT Camara, Especie, Envase, Temperatura FROM Control_Camaras WHERE ID_Reporte='" + id_reporte + "' ORDER BY Camara, Envase")
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
                    pdf.text(x=45, y=286, txt= str(fecha_actual()))## Traer fecha actual
                    pdf.set_font('Arial', 'B', 10)
                    pdf.rect(x=10,y=43,w=190,h=5)
                    pdf.text(x=16, y=47.5, txt= 'CÁMARA')
                    pdf.line(40,43,40,48)
                    pdf.text(x=55, y=47.5, txt= 'ESPECIE')
                    pdf.line(85,43,85,48)
                    pdf.text(x=100, y=47.5, txt= 'ENVASE')
                    pdf.line(130,43,130,48)
                    pdf.text(x=150, y=47.5, txt= 'TEMPERATURA') 
                    cantidad = 0
                    if consulta_camaras:
                        for i in consulta_camaras:
                            envase = str(i[2])
                            if envase == "SELECCIONE":
                                envase = "-"
                            pdf.set_font('Arial', '', 8)
                            pdf.cell(w=30, h=3, txt= str(i[0]), border='LBR', align='C', fill=0)
                            pdf.cell(w=45, h=3, txt= str(i[1]), border='BR', align='C', fill=0)
                            pdf.cell(w=45, h=3, txt= envase, border='BR', align='C', fill=0)
                            pdf.multi_cell(w=70, h=3, txt= str(i[3] + ' °C'), border='BR', align='C', fill=0)
                            cantidad = cantidad + 1

                        if cantidad > 76:
                            pdf.set_font('Times', 'I', 12)
                            pdf.text(x=12, y=40, txt= 'Fecha Control: ' + fecha)
                            pdf.text(x=65, y=40, txt= 'Hora Control: ' + hora + ' Hs.')
                            pdf.set_font('Arial', 'B', 10)
                            pdf.text(x=16.5, y=286, txt= user_name)
                            pdf.text(x=45, y=286, txt= str(fecha_actual()))## Traer fecha actual
                            pdf.set_font('Arial', 'B', 10)
                            pdf.rect(x=10,y=43,w=190,h=5)
                            pdf.text(x=16, y=47.5, txt= 'CÁMARA')
                            pdf.line(40,43,40,48)
                            pdf.text(x=55, y=47.5, txt= 'ESPECIE')
                            pdf.line(85,43,85,48)
                            pdf.text(x=100, y=47.5, txt= 'ENVASE')
                            pdf.line(130,43,130,48)
                            pdf.text(x=150, y=47.5, txt= 'TEMPERATURA')     
                            
                        ##OBSERVACIONES
                
                        pdf.add_page()
                        pdf.set_font('Times', 'I', 12)
                        pdf.text(x=12, y=40, txt= 'Fecha Control: ' + str(data_principal[1]))
                        pdf.text(x=65, y=40, txt= 'Hora Control: ' + str(data_principal[2]) + ' Hs.')
                        pdf.set_font('Arial', 'B', 10)
                        if user_name == "Nicole":
                            pdf.set_font('Times', 'BI', 10)
                            pdf.text(x=20, y=288, txt= 'Nicole')
                        else:
                            pdf.text(x=20, y=288, txt= user_name)#USER
                        pdf.text(x=45, y=286, txt= str(fecha_actual()))## Traer fecha actual
                        pdf.rect(x=10,y=43,w=190,h=5)
                        pdf.text(x=11, y=46.5, txt= 'OBSERVACIONES:')
                        ### CONTRUCTOR DE OBS
                        observaciones = str(data_principal[3])
                        lista_observaciones = observaciones.split("_")
                        for j in lista_observaciones:
                            pdf.set_font('Arial', '', 10)
                            pdf.multi_cell(w=0, h=5, txt= str(j) or "Sin Observaciones", border='LBR', align='L', fill=0)                        

                    ##CONSULTA IMAGENES
                    consulta_data_images = ("SELECT Fotos FROM Fotos_Control_Camaras WHERE ID_Reporte='" + id_reporte + "'")
                    cursorZetoApp.execute(consulta_data_images)
                    consulta_images = cursorZetoApp.fetchall()
                    if consulta_images:
                        ### IMAGENES
                        pdf.rect(x=10,y=98,w=190,h=5)
                        pdf.set_font('Arial', 'B', 10)
                        pdf.text(x=11, y=102, txt= 'IMÁGENES:')
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
                    pdf.output('App/Empaque/data/pdf/' + name_pdf  , 'F')
                    jsonList = json.dumps({'message': 'Success', 'pdf': name_pdf}) 
                    return JsonResponse(jsonList, safe=False)
                else:
                    jsonList = json.dumps({'message': 'No se encontraron Reportes para la fecha: ' + str(fecha)}) 
                    return JsonResponse(jsonList, safe=False)
            except Exception as e:
                error = "Ocurrió un error: " + str(e)
                jsonList = json.dumps({'message': error}) 
                return JsonResponse(jsonList, safe=False)
            finally:
                cursorZetoApp.close()
                ZetoApp.close()
        elif str(Tipo) == "Control Empaque":
            Top_Caja = consultaTopCaja(fecha)
            if Top_Caja != "0":
                try:
                    conexion = zetoneApp()
                    cursor = conexion.cursor()
                    consultaSQL = ("SELECT        Bulto.Id_bulto AS id, Marca.Nombre_marca AS Marca, Calidad.nombre_calidad AS Calidad, Variedad.nombre_variedad AS Variedad, Especie.nombre_especie AS Especie, Bulto.id_galpon AS Galpon, \n" +
                                                            "Envase.nombre_envase AS Envase, Calibre.nombre_calibre AS Calibre, USR_MCCUADRO.USR_CUAD_UMI AS UMI, USR_MCCUADRO.USR_CUAD_UP AS UP, Embalador.nombre_embalador AS Embalador, \n" +
                                                            "USR_MCLOTE.USR_LOTE_NUMERO AS Lote, CONVERT(varchar(10), Bulto.fecha_alta_bulto, 103) AS FechaEmbalado, CONVERT(varchar(5), Bulto.fecha_alta_bulto, 108) AS HoraEmbalado, numeroCaja, CONVERT(varchar(10), DefectosCaja.Fecha, 103) AS FechaControl, CONVERT(varchar(5), DefectosCaja.Hora, 108) AS HoraControl, PesoNeto, PesoBruto, PLU, Observaciones, Deformadas, TamañoIncorrecto, FaltaDeColor, Russeting, Heladas, roceBins, Asoleado, QuemadoPorSol, Fitotoxicidad, Rolado, Golpes, \n" +
                                                            "Heridas, HeridasViejas, Cracking, Bitterpit, Granizo, DañoPorInsecto, FaltaDePedunculo, DesvioDeClasificacion, SegundaFlor, Madurez, Deshidratacion, Decaimiento, MohoHumedo, MohoSeco, MohoAcuoso, Rameado, \n" +
                                                            "FirmezaPulpaMax, FirmezaPulpaMin, FirmezaPulpaPromedio, faltaDeBoro, Maquina, Usuario\n" +
                                    "FROM            servidordb.trazabilidad.dbo.Especie AS Especie INNER JOIN\n" +
                                                            "servidordb.trazabilidad.dbo.Variedad AS Variedad ON Especie.id_especie = Variedad.id_especie INNER JOIN\n" +
                                                            "servidordb.trazabilidad.dbo.Bulto AS Bulto INNER JOIN\n" +
                                                            "servidordb.trazabilidad.dbo.Configuracion AS Configuracion ON Bulto.id_configuracion = Configuracion.id_configuracion INNER JOIN\n" +
                                                            "servidordb.trazabilidad.dbo.Marca AS Marca ON Configuracion.id_marca = Marca.id_marca INNER JOIN\n" +
                                                            "servidordb.trazabilidad.dbo.Calidad AS Calidad ON Configuracion.id_calidad = Calidad.Id_calidad ON Variedad.Id_variedad = Configuracion.id_variedad INNER JOIN\n" +
                                                            "servidordb.trazabilidad.dbo.Envase AS Envase ON Configuracion.id_envase = Envase.id_envase INNER JOIN\n" +
                                                            "servidordb.trazabilidad.dbo.Calibre AS Calibre ON Configuracion.id_calibre = Calibre.Id_calibre INNER JOIN\n" +
                                                            "servidordb.trazabilidad.dbo.LoteEtiquetado AS LoteEtiquetado ON Bulto.id_loteEtiquetado = LoteEtiquetado.id_loteEtiquetado INNER JOIN\n" +
                                                            "servidordb.General.dbo.USR_MCLOTE AS USR_MCLOTE ON LoteEtiquetado.id_lote = USR_MCLOTE.USR_LOTE_NUMERO INNER JOIN\n" +
                                                            "servidordb.General.dbo.USR_MCCUADRO AS USR_MCCUADRO ON USR_MCLOTE.USR_CUAD_ALIAS = USR_MCCUADRO.USR_CUAD_ALIAS INNER JOIN\n" +
                                                            "servidordb.trazabilidad.dbo.Embalador AS Embalador ON Bulto.id_embalador = Embalador.Id_embalador INNER JOIN\n" +
                                                            "servidordb.General.dbo.USR_MCCHACRA AS USR_MCCHACRA ON USR_MCCUADRO.USR_CHAC_ALIAS = USR_MCCHACRA.USR_CHAC_ALIAS INNER JOIN\n" +
                                                            "DefectosCaja ON Bulto.Id_bulto = DefectosCaja.IdCaja\n" +
                                    "WHERE        (Bulto.Id_bulto > '" + str(Top_Caja) + "') AND  TRY_CONVERT(DATE, DefectosCaja.Fecha) ='" + str(fecha) + "'")
                    cursor.execute(consultaSQL)
                    consulta = cursor.fetchall()
                    if consulta:
                        pdf = Control_Cajas()
                        pdf.alias_nb_pages()
                        index = 0
                        for i in consulta:
                            if index == 0:
                                if str(i[5]) == "1":
                                    empaque = "Pera"
                                else:
                                    empaque = "Manzana"
                                pdf.add_page()
                                pdf.set_font('Arial', '', 7)
                                pdf.text(x=146, y=16.5, txt= str(fechaNombre(fecha)))
                                #pdf.text(x=165.5, y=19.5, txt= '10:23:33 Hs.')
                                ###DATOS PRINCIPALES CAJA
                                pdf.set_font('Arial', '', 10)
                                pdf.text(x=26, y=48, txt= str(i[14]))
                                pdf.text(x=56, y=48, txt= str(i[0]))
                                pdf.text(x=90, y=48, txt= str(i[15]))
                                pdf.text(x=122, y=48, txt= str(i[16]) + ' Hs.')
                                pdf.text(x=160, y=48, txt= empaque)
                                pdf.text(x=196, y=48, txt= str(i[52]))#MAQUINA

                                pdf.set_font('Arial', '', 8)
                                pdf.text(x=12, y=59, txt= str(i[3]))#VARIEDAD
                                pdf.text(x=46, y=59, txt= str(i[6]))#ENVASE
                                pdf.text(x=78, y=59, txt= str(i[1]))#MARCA
                                pdf.text(x=120, y=59, txt= str(i[7]))#TAMAÑO
                                pdf.text(x=12, y=69, txt= str(i[2]))#CATEGORÍA
                                pdf.text(x=46, y=69, txt= str(i[10]))#EMBALADOR
                                pdf.text(x=78, y=69, txt= str(i[9]))#UP
                                pdf.text(x=104, y=69, txt= str(i[12]) + ' ' + str(i[13]) +' Hs.')#FECHA HORA EMBALADO
                                pdf.text(x=22, y=79, txt= str(i[11]) + ' / ' + str(i[8]))#LOTE Y UMI
                                pdf.text(x=64, y=79, txt= str(i[19]))#PLU
                                pdf.text(x=86, y=79, txt= str(i[18]) + ' Kg.')# PESO BRUTO
                                pdf.text(x=116, y=79, txt= str(i[17]) + ' Kg.')#PESO NETO
                                ##DEFECTOS
                                ###IZQUIERDAAA
                                pdf.text(x=50, y=88.5, txt= str(i[21]))#DESFORMADAS
                                pdf.text(x=50, y=94, txt= str(i[22]))#T INCORRECTO
                                pdf.text(x=50, y=99, txt= str(i[23]))#F COLOR
                                pdf.text(x=50, y=104, txt= str(i[24]))#RUSSETING
                                pdf.text(x=50, y=109, txt= str(i[25]))#HELADAS
                                pdf.text(x=50, y=114, txt= str(i[26]))#ROC BINS
                                pdf.text(x=50, y=119, txt= str(i[27]))##ASOLEADo
                                pdf.text(x=50, y=124, txt= str(i[28]))#QUEMADO SOL
                                pdf.text(x=50, y=129, txt= str(i[29]))
                                pdf.text(x=50, y=134, txt= str(i[30]))
                                pdf.text(x=50, y=139, txt= str(i[31]))
                                pdf.text(x=50, y=144, txt= str(i[32]))
                                pdf.text(x=50, y=149, txt= str(i[33]))
                                ### DERECHA
                                pdf.text(x=129, y=88.5, txt= str(i[34]))
                                pdf.text(x=129, y=94, txt= str(i[35]))
                                pdf.text(x=129, y=99, txt= str(i[36]))
                                pdf.text(x=129, y=104, txt= str(i[37]))
                                pdf.text(x=129, y=109, txt= str(i[38]))
                                pdf.text(x=129, y=114, txt= str(i[39]))
                                pdf.text(x=129, y=119, txt= str(i[40]))
                                pdf.text(x=129, y=124, txt= str(i[41]))
                                pdf.text(x=129, y=129, txt= str(i[42]))
                                pdf.text(x=129, y=134, txt= str(i[43]))
                                pdf.text(x=118, y=139, txt= str(i[44]) + ' / ' + str(i[45]) + ' / ' + str(i[46]) )
                                pdf.text(x=118, y=144, txt= str(i[48]) + ' / ' + str(i[50]) + ' / ' + str(i[49]) )
                                pdf.text(x=129, y=149, txt= str(i[51]))
                                ## OBSERVACIONES
                                pdf.text(x=22, y=153, txt= str(i[20]))##OBSERVACION
                                pdf.set_font('Times', 'B', 10)
                                pdf.text(x=46, y=288, txt= str(fecha_actual()))
                                pdf.set_font('Times', 'I', 10)
                                user = str(i[53])
                                if str(datos[5]) == "Nicole" or str(datos[5]) == "nicole":
                                    pdf.set_font('Times', 'BI', 10)
                                    pdf.text(x=20, y=288, txt= 'Nicole')
                                else:
                                    pdf.text(x=20, y=288, txt= user)#USER
                                ###FOTOS
                                bulto = str(i[0])
                                try:
                                    pdf.image('App/API/media/images/Calidad/reportes_empaque/plu_image_' + bulto + '.jpeg', x=160, y=58, w=15, h=15)
                                except:
                                    pdf.set_font('Arial', '', 12)
                                    pdf.text(x=155, y=65, txt='NOT IMAGE')
                                try:
                                    pdf.image('App/API/media/images/Calidad/reportes_empaque/caja_image_' + bulto + '.jpeg', x=146, y=82, w=45, h=70)
                                except:
                                    pdf.set_font('Arial', '', 12)
                                    pdf.text(x=155, y=119, txt='NOT IMAGE')
                                index = index + 1
                            else:
                                if str(i[5]) == "1":
                                    empaque = "Pera"
                                else:
                                    empaque = "Manzana"
                                #CONDICIONAL CUANDO VALE 1
                                pdf.set_font('Arial', '', 10)
                                pdf.text(x=26, y=168, txt= str(i[14]))#CAJA
                                pdf.text(x=56, y=168, txt= str(i[0]))#BULTO
                                pdf.text(x=90, y=168, txt= str(i[15]))#FECHA CONTROL
                                pdf.text(x=122, y=168, txt= str(i[16]) + ' Hs.')#HORA CONTROL
                                pdf.text(x=160, y=168, txt= empaque)#EMPAQUE
                                pdf.text(x=196, y=168, txt= str(i[52]))#MÁQUINA

                                pdf.set_font('Arial', '', 8)
                                pdf.text(x=12, y=178, txt= str(i[3]))#VARIEDAD
                                pdf.text(x=47, y=178, txt= str(i[6]))#ENVASE
                                pdf.text(x=80, y=178, txt= str(i[1]))#MARCA
                                pdf.text(x=121, y=178, txt= str(i[7]))#TAMAÑO
                                pdf.text(x=12, y=188, txt= str(i[2]))#CATEGORÍA
                                pdf.text(x=47, y=188, txt= str(i[10]))#EMBALADOR
                                pdf.text(x=77, y=188, txt= str(i[9]))#UP
                                pdf.text(x=102, y=188, txt= str(i[12]) + ' ' + str(i[13]) +' Hs.')#FECHA HORA EMBALADO
                                pdf.text(x=22, y=198, txt= str(i[11]) + ' / ' + str(i[8]))#LOTE UMI
                                pdf.text(x=62, y=198, txt= str(i[19]))#PLU
                                pdf.text(x=86, y=198, txt= str(i[18]) + ' Kg.')#PESO BRUTO
                                pdf.text(x=114, y=198, txt= str(i[17]) + ' Kg.')#PESO NETO
                                ###IZQUIERDAAA
                                pdf.text(x=50, y=208, txt= str(i[21]))
                                pdf.text(x=50, y=213, txt= str(i[22]))
                                pdf.text(x=50, y=218, txt= str(i[23]))
                                pdf.text(x=50, y=223, txt= str(i[24]))
                                pdf.text(x=50, y=228, txt= str(i[25]))
                                pdf.text(x=50, y=233, txt= str(i[26]))
                                pdf.text(x=50, y=238, txt= str(i[27]))
                                pdf.text(x=50, y=243, txt= str(i[28]))
                                pdf.text(x=50, y=248, txt= str(i[29]))
                                pdf.text(x=50, y=253, txt= str(i[30]))
                                pdf.text(x=50, y=258, txt= str(i[31]))
                                pdf.text(x=50, y=263, txt= str(i[32]))
                                pdf.text(x=50, y=268, txt= str(i[33]))
                                ### DERECHA
                                pdf.text(x=129, y=208, txt= str(i[34]))
                                pdf.text(x=129, y=213, txt= str(i[35]))
                                pdf.text(x=129, y=218, txt= str(i[36]))
                                pdf.text(x=129, y=223, txt= str(i[37]))
                                pdf.text(x=129, y=228, txt= str(i[38]))
                                pdf.text(x=129, y=233, txt= str(i[39]))
                                pdf.text(x=129, y=238, txt= str(i[40]))
                                pdf.text(x=129, y=243, txt= str(i[41]))
                                pdf.text(x=129, y=248, txt= str(i[42]))
                                pdf.text(x=129, y=253, txt= str(i[43]))
                                pdf.text(x=118, y=258, txt= str(i[44]) + ' / ' + str(i[45]) + ' / ' + str(i[46]))
                                pdf.text(x=118, y=263, txt= str(i[48]) + ' / ' + str(i[50]) + ' / ' + str(i[49]))
                                pdf.text(x=129, y=268, txt= str(i[51]))
                                ## OBSERVACIONES
                                pdf.text(x=22, y=274, txt= str(i[20]))
                                ##FOTOS

                                bulto = str(i[0])
                                ruta_caja = 'App/API/media/images/Calidad/reportes_empaque/caja_image_' + bulto + '.jpeg'
                                ruta_plu = 'App/API/media/images/Calidad/reportes_empaque/plu_image_' + bulto + '.jpeg'
                                try:
                                    pdf.image('App/API/media/images/Calidad/reportes_empaque/plu_image_' + bulto + '.jpeg', x=160, y=178, w=15, h=15)
                                except:
                                    pdf.set_font('Arial', '', 12)
                                    pdf.text(x=155, y=188, txt='NOT IMAGE')
                                try:
                                    pdf.image('App/API/media/images/Calidad/reportes_empaque/caja_image_' + bulto + '.jpeg', x=146, y=201, w=45, h=70)
                                except:
                                    pdf.set_font('Arial', '', 12)
                                    pdf.text(x=155, y=235, txt='NOT IMAGE')
                                index = 0
                        name_pdf = "Control_Empaque_" + str(fecha) + ".pdf"
                        pdf.output('App/Empaque/data/pdf/' + name_pdf, 'F')
                        jsonList = json.dumps({'message': 'Success', 'pdf': name_pdf}) 
                        return JsonResponse(jsonList, safe=False)
                    else:
                        jsonList = json.dumps({'message': 'No se encontraron Reportes para la fecha: ' + str(fecha)}) 
                        return JsonResponse(jsonList, safe=False)
                except Exception as e:
                    error = "Ocurrió un error: " + str(e)
                    jsonList = json.dumps({'message': error}) 
                    return JsonResponse(jsonList, safe=False)
                finally:
                    cursor.close()
                    conexion.close()
            else:
                jsonList = json.dumps({'message': 'No se encontraron Reportes para la fecha: ' + str(fecha)}) 
                return JsonResponse(jsonList, safe=False)
        elif str(Tipo) == "Control Descarte":
            try:
                conexion = zetoneApp()
                cursor = conexion.cursor()
                sql5 = ("SELECT        DescarteLote.Lote, Variedad.USR_VAR_NOMBRE as Variedad, DescarteLote.Empaque, CONVERT(varchar(10), DescarteLote.Fecha, 103) AS Fecha, CONVERT(varchar(5), DescarteLote.Hora, 108) AS Hora, DescarteLote.cantBins, DescarteLote.obsDescarte, DescarteLote.Usuario, DefectosDescarte.Agamuzado,\n" +
                                                "DefectosDescarte.Amarillo, DefectosDescarte.Arañuela, DefectosDescarte.Bicho, DefectosDescarte.binsRotos, DefectosDescarte.binsSinLlenar, DefectosDescarte.Bitterpit, DefectosDescarte.Caliz, \n" +
                                                "DefectosDescarte.Carpocapsa, DefectosDescarte.Acuoso, DefectosDescarte.Mohoso, DefectosDescarte.Corcho, DefectosDescarte.Cucharita, DefectosDescarte.Cracking, DefectosDescarte.Quimico, \n" +
                                                "DefectosDescarte.Decaimiento, DefectosDescarte.Deformada, DefectosDescarte.Deshidratada, DefectosDescarte.Desvio, DefectosDescarte.faltaBoro, DefectosDescarte.faltaColor, DefectosDescarte.Fondo, \n" +
                                                "DefectosDescarte.frutoGrande, DefectosDescarte.FrutoChico, DefectosDescarte.golpes, DefectosDescarte.Granizo, DefectosDescarte.Helada, DefectosDescarte.Heridas, DefectosDescarte.heridaMaquina, \n" +
                                                "DefectosDescarte.heridaPedunculo, DefectosDescarte.Herinosis, DefectosDescarte.Lenticelosis, DefectosDescarte.Machucones, DefectosDescarte.madurezAvanzada, DefectosDescarte.madurezSalpicada, \n" +
                                                "DefectosDescarte.malCosechada, DefectosDescarte.Mezcla, DefectosDescarte.Piojo, DefectosDescarte.Podridas, DefectosDescarte.Psilido, DefectosDescarte.Pulgon, DefectosDescarte.Quemada, \n" +
                                                "DefectosDescarte.Rameada, DefectosDescarte.Roce, DefectosDescarte.Rolado, DefectosDescarte.Russeting, DefectosDescarte.Sarna, DefectosDescarte.Flor, DefectosDescarte.sinPedunculo, \n" +
                                                "DefectosDescarte.Trips\n" +
                        "FROM            DescarteLote INNER JOIN\n" +
                                                "DefectosDescarte ON DescarteLote.Lote = DefectosDescarte.Lote INNER JOIN\n" +
                                                "servidordb.general.dbo.usr_mclote AS Lote ON DescarteLote.Lote = Lote.USR_LOTE_NUMERO INNER JOIN\n" +
                                                "servidordb.general.dbo.usr_mcvaried AS Variedad ON Lote.USR_VAR_ALIAS = Variedad.USR_VAR_ALIAS\n"+
                        "WHERE        (TRY_CONVERT(DATE, DescarteLote.Fecha) = '" + str(fecha) + "')")
                cursor.execute(sql5)
                consulta = cursor.fetchall()
                if consulta:
                    index = 0
                    pdf = Reporte_Descarte()
                    pdf.alias_nb_pages()
                    for i in consulta:
                        if i[2] == 1:
                            empaque = "Pera"
                        else:
                            empaque = "Manzana"
                        if index == 0:
                            pdf.add_page()
                            ###IZQUIERDA
                            pdf.set_font('Arial', '', 7)
                            pdf.text(x=146, y=16.5, txt= str(fechaNombre(fecha)))
                            pdf.set_font('Arial', '', 10)
                            pdf.text(x=32, y=44, txt= empaque)
                            pdf.text(x=66, y=44, txt= str(i[3]))
                            pdf.text(x=25, y=49, txt= str(i[4]) + ' Hs.')
                            pdf.text(x=66, y=49, txt= str(i[0]))
                            pdf.text(x=32, y=54, txt= str(i[5]))
                            pdf.text(x=58, y=54, txt= str(i[1]))
                            ##DEFECTOS
                            pdf.set_font('Arial', '', 8)
                            pdf.text(x=68, y=63, txt= str(i[8]))
                            pdf.text(x=68, y=67, txt= str(i[9]))
                            pdf.text(x=68, y=71, txt= str(i[10]))
                            pdf.text(x=68, y=75, txt= str(i[11]))
                            pdf.text(x=68, y=79, txt= str(i[12]))
                            pdf.text(x=68, y=83, txt= str(i[13]))
                            pdf.text(x=68, y=87, txt= str(i[14]))
                            pdf.text(x=68, y=91, txt= str(i[15]))
                            pdf.text(x=68, y=95, txt= str(i[16]))
                            pdf.text(x=68, y=99, txt= str(i[17]))
                            pdf.text(x=68, y=103, txt= str(i[18]))
                            pdf.text(x=68, y=107, txt= str(i[19]))
                            pdf.text(x=68, y=111, txt= str(i[20]))
                            pdf.text(x=68, y=115, txt= str(i[21]))
                            pdf.text(x=68, y=119, txt= str(i[22]))
                            pdf.text(x=68, y=123, txt= str(i[23]))
                            pdf.text(x=68, y=127, txt= str(i[24]))
                            pdf.text(x=68, y=131, txt= str(i[25]))
                            pdf.text(x=68, y=135, txt= str(i[26]))
                            pdf.text(x=68, y=139, txt= str(i[27]))
                            pdf.text(x=68, y=143, txt= str(i[28]))
                            pdf.text(x=68, y=147, txt= str(i[29]))
                            pdf.text(x=68, y=151, txt= str(i[30]))
                            pdf.text(x=68, y=155, txt= str(i[31]))
                            pdf.text(x=68, y=159, txt= str(i[32]))
                            pdf.text(x=68, y=163, txt= str(i[33]))
                            pdf.text(x=68, y=167, txt= str(i[34]))
                            pdf.text(x=68, y=171, txt= str(i[35]))
                            pdf.text(x=68, y=175, txt= str(i[36]))
                            pdf.text(x=68, y=179, txt= str(i[37]))
                            pdf.text(x=68, y=183, txt= str(i[38]))
                            pdf.text(x=68, y=187, txt= str(i[39]))
                            pdf.text(x=68, y=191, txt= str(i[40]))
                            pdf.text(x=68, y=195, txt= str(i[41]))
                            pdf.text(x=68, y=199, txt= str(i[42]))
                            pdf.text(x=68, y=203, txt= str(i[43]))
                            pdf.text(x=68, y=207, txt= str(i[44]))
                            pdf.text(x=68, y=211, txt= str(i[45]))
                            pdf.text(x=68, y=215, txt= str(i[46]))
                            pdf.text(x=68, y=219, txt= str(i[47]))
                            pdf.text(x=68, y=223, txt= str(i[48]))
                            pdf.text(x=68, y=227, txt= str(i[49]))
                            pdf.text(x=68, y=231, txt= str(i[50]))
                            pdf.text(x=68, y=235, txt= str(i[51]))
                            pdf.text(x=68, y=239, txt= str(i[52]))
                            pdf.text(x=68, y=243, txt= str(i[53]))
                            pdf.text(x=68, y=247, txt= str(i[54]))
                            pdf.text(x=68, y=251, txt= str(i[55]))
                            pdf.text(x=68, y=255, txt= str(i[56]))
                            pdf.text(x=68, y=259, txt= str(i[57]))
                            pdf.text(x=20, y=267, txt= str(i[6]))
                            pdf.set_font('Arial', 'B', 10)
                            pdf.text(x=46, y=288, txt= str(i[3]))#FECHA
                            ## CONDICIONAL DE USER
                            if str(datos[5]) == "Nicole" or str(datos[5]) == "nicole":
                                pdf.set_font('Times', 'BI', 10)
                                pdf.text(x=20, y=288, txt= 'Nicole')
                            else:
                                pdf.text(x=20, y=288, txt= str(i[7]))
                            index = index + 1
                        else:
                            ##DERECHA
                            pdf.set_font('Arial', '', 10)
                            pdf.text(x=142, y=44, txt= empaque)
                            pdf.text(x=176, y=44, txt= str(i[3]))
                            pdf.text(x=135, y=49, txt= str(i[4]) + ' Hs.')
                            pdf.text(x=176, y=49, txt= str(i[0]))
                            pdf.text(x=142, y=54, txt= str(i[5]))
                            pdf.text(x=168, y=54, txt= str(i[1]))
                            ##DEFECTOS
                            pdf.set_font('Arial', '', 8)
                            pdf.text(x=178, y=63, txt= str(i[8]))
                            pdf.text(x=178, y=67, txt= str(i[9]))
                            pdf.text(x=178, y=71, txt= str(i[10]))
                            pdf.text(x=178, y=75, txt= str(i[11]))
                            pdf.text(x=178, y=79, txt= str(i[12]))
                            pdf.text(x=178, y=83, txt= str(i[13]))
                            pdf.text(x=178, y=87, txt= str(i[14]))
                            pdf.text(x=178, y=91, txt= str(i[15]))
                            pdf.text(x=178, y=95, txt= str(i[16]))
                            pdf.text(x=178, y=99, txt= str(i[17]))
                            pdf.text(x=178, y=103, txt= str(i[18]))
                            pdf.text(x=178, y=107, txt= str(i[19]))
                            pdf.text(x=178, y=111, txt= str(i[20]))
                            pdf.text(x=178, y=115, txt= str(i[21]))
                            pdf.text(x=178, y=119, txt= str(i[22]))
                            pdf.text(x=178, y=123, txt= str(i[23]))
                            pdf.text(x=178, y=127, txt= str(i[24]))
                            pdf.text(x=178, y=131, txt= str(i[25]))
                            pdf.text(x=178, y=135, txt= str(i[26]))
                            pdf.text(x=178, y=139, txt= str(i[27]))
                            pdf.text(x=178, y=143, txt= str(i[28]))
                            pdf.text(x=178, y=147, txt= str(i[29]))
                            pdf.text(x=178, y=151, txt= str(i[30]))
                            pdf.text(x=178, y=155, txt= str(i[31]))
                            pdf.text(x=178, y=159, txt= str(i[32]))
                            pdf.text(x=178, y=163, txt= str(i[33]))
                            pdf.text(x=178, y=167, txt= str(i[34]))
                            pdf.text(x=178, y=171, txt= str(i[35]))
                            pdf.text(x=178, y=175, txt= str(i[36]))
                            pdf.text(x=178, y=179, txt= str(i[37]))
                            pdf.text(x=178, y=183, txt= str(i[38]))
                            pdf.text(x=178, y=187, txt= str(i[39]))
                            pdf.text(x=178, y=191, txt= str(i[40]))
                            pdf.text(x=178, y=195, txt= str(i[41]))
                            pdf.text(x=178, y=199, txt= str(i[42]))
                            pdf.text(x=178, y=203, txt= str(i[43]))
                            pdf.text(x=178, y=207, txt= str(i[44]))
                            pdf.text(x=178, y=211, txt= str(i[45]))
                            pdf.text(x=178, y=215, txt= str(i[46]))
                            pdf.text(x=178, y=219, txt= str(i[47]))
                            pdf.text(x=178, y=223, txt= str(i[48]))
                            pdf.text(x=178, y=227, txt= str(i[49]))
                            pdf.text(x=178, y=231, txt= str(i[50]))
                            pdf.text(x=178, y=235, txt= str(i[51]))
                            pdf.text(x=178, y=239, txt= str(i[52]))
                            pdf.text(x=178, y=243, txt= str(i[53]))
                            pdf.text(x=178, y=247, txt= str(i[54]))
                            pdf.text(x=178, y=251, txt= str(i[55]))
                            pdf.text(x=178, y=255, txt= str(i[56]))
                            pdf.text(x=178, y=259, txt= str(i[57]))
                            pdf.text(x=130, y=267, txt= str(i[6]))
                            index = 0
                    ###IMPRIMO PDF
                    name_fecha = str(fecha).replace('-','')
                    name = "Control_Descarte_" + name_fecha + '.pdf'
                    pdf.output('App/Empaque/data/pdf/' + name, 'F')
                    jsonList = json.dumps({'message': 'Success', 'pdf': name}) 
                    return JsonResponse(jsonList, safe=False)
                else:
                    jsonList = json.dumps({'message': 'No se encontraron Reportes para la fecha: ' + str(fecha)}) 
                    return JsonResponse(jsonList, safe=False)
            except Exception as e:
                    error = "Ocurrió un error: " + str(e)
                    jsonList = json.dumps({'message': error}) 
                    return JsonResponse(jsonList, safe=False)
            finally:
                cursor.close()
                conexion.close()
        elif str(Tipo) == "Control Presiones":
            if  listaHoras(fecha) == 5:
                error = "Ocurrió un error en la conexión."
                jsonList = json.dumps({'message': error}) 
                return JsonResponse(jsonList, safe=False)
            elif listaHoras(fecha) == 0:
                jsonList = json.dumps({'message': 'No se encontraron Reportes para la fecha: ' + str(fecha)}) 
                return JsonResponse(jsonList, safe=False)
            else:
                ##CONSIGUIÓ LAS HORAS
                listado_de_horas = listaHoras(str(fecha))
                index = 0
                pdf = Reporte_Presiones()
                pdf.alias_nb_pages()
                for i in listado_de_horas:
                    hora = str(i)
                    hora_replace = hora.replace(':','')
                    lista_x = data_x(str(fecha),hora)
                    lista_y = data_y(str(fecha),hora)
                    Crea_grafico(lista_x,lista_y,hora_replace)
                    datos = data_Presiones(str(fecha),hora)
                    if datos[0] == "1":
                        empaque = "Pera"
                    else:
                        empaque = "Manzana"
                    if index == 0:
                        pdf.add_page()
                        ###ARRIBA
                        pdf.set_font('Arial', '', 7)
                        pdf.text(x=146, y=16.5, txt= str(fechaNombre(fecha)))
                        pdf.set_font('Arial', '', 10)
                        pdf.text(x=44, y=49, txt= empaque)
                        pdf.text(x=100, y=49, txt= datos[1])
                        pdf.text(x=160, y=49, txt= datos[2]+' Hs.')
                        pdf.text(x=76, y=64, txt= str(datos[3]))
                        pdf.text(x=165, y=64, txt= datos[4] + ' Lb.')
                        pdf.image('App/API/media/images/Calidad/reportes_presiones/grafico_presion_' + hora_replace + '.png', x=12, y=85, w=180, h=50)
                        pdf.set_font('Arial', 'B', 10)
                        pdf.text(x=46, y=288, txt= datos[1])
                        ## CONDICIONAL DE USER
                        if str(datos[5]) == "Nicole" or str(datos[5]) == "nicole":
                            pdf.set_font('Times', 'BI', 10)
                            pdf.text(x=20, y=288, txt= 'Nicole')
                        else:
                            pdf.text(x=20, y=288, txt= str(datos[5]))
                        index = index + 1
                    else:
                        ###ABAJO
                        pdf.set_font('Arial', '', 10)
                        pdf.text(x=44, y=169, txt= empaque)
                        pdf.text(x=100, y=169, txt= datos[1])
                        pdf.text(x=160, y=169, txt= datos[2] + ' Hs.')
                        pdf.text(x=76, y=184, txt= str(datos[3]))
                        pdf.text(x=165, y=184, txt= datos[4] + ' Lb.')
                        pdf.image('App/API/media/images/Calidad/reportes_presiones/grafico_presion_' + hora_replace + '.png', x=12, y=205, w=180, h=50)
                        index = 0
                name_fecha = str(fecha).replace('-','')
                name = "Control_Presiones_" + name_fecha + '.pdf'
                pdf.output('App/Empaque/data/pdf/' + name, 'F')
                delete_png_files()
                jsonList = json.dumps({'message': 'Success', 'pdf': name}) 
                return JsonResponse(jsonList, safe=False)
    else:
        error = "Ocurrió un error: "
        jsonList = json.dumps({'message': error}) 
        return JsonResponse(jsonList, safe=False)
    

def data_x(fecha,hora):
    try:
        conexion = zetoneApp()
        cursor = conexion.cursor()
        sql = ("SELECT Fruto FROM Presiones WHERE TRY_CONVERT(DATE, Fecha) ='" + fecha + "' AND Hora='" + str(hora) + "'")
        cursor.execute(sql)
        consulta = cursor.fetchall()
        if consulta:
            x_data = [] # FRUTOS
            for i in consulta:
                x_data.append(i[0])
        return x_data
    except Exception as e:
            print(e)
    finally:
        cursor.close()
        conexion.close()

def data_y(fecha,hora):
    try:
        conexion = zetoneApp()
        cursor = conexion.cursor()
        sql = ("SELECT CAST((ROUND(Presion, 0, 0)) AS INT) FROM Presiones WHERE TRY_CONVERT(DATE, Fecha) ='" + fecha + "' AND Hora='" + str(hora) + "'")
        cursor.execute(sql)
        consulta = cursor.fetchall()
        if consulta:
            y_data = [] # FRUTOS
            for i in consulta:
                y_data.append(i[0])
        return y_data
    except Exception as e:
            print(e)
    finally:
        cursor.close()
        conexion.close()

def Crea_grafico(lista_x,lista_y,hora):
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.plot(lista_x, lista_y, 'o-', label='Presiones')
    for x, y in zip(lista_x, lista_y):
        ax.scatter(x, y, color='black')
        ax.annotate(y, (x, y), textcoords="offset points", xytext=(0,5), ha='center')
    ax.set_xlabel("N° Fruto")
    ax.set_ylabel("Presión (Lb.)")
    ax.set_xticks(lista_x)
    ax.set_yticks(lista_y)
    ax.set_yticks(range(min(lista_y), max(lista_y)+1, 2))
    ax.legend()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    name_image = 'grafico_presion_' + str(hora)
    plt.savefig('App/API/media/images/Calidad/reportes_presiones/'+ name_image + '.png')

def listaHoras(fecha):
    try:
        conexion = zetoneApp()
        cursor = conexion.cursor()
        sql5 = ("SELECT DISTINCT CONVERT(char(5),Hora) FROM Presiones WHERE Fecha='" + str(fecha) + "'")
        cursor.execute(sql5)
        consulta = cursor.fetchall()
        if consulta:
            horasLista = []
            for i in consulta:
                hora = str(i[0])
                horasLista.append(hora)
            return horasLista
        else:
            return 0
    except Exception as e:
            return 5
    finally:
        cursor.close()
        conexion.close()

def data_Presiones(fecha,hora):
    try:
        conexion = zetoneApp()
        cursor = conexion.cursor()
        sql5 = ("SELECT Empaque, CONVERT(varchar(10), Fecha, 103) AS fecha, CONVERT(char(5),Hora) AS hora, MAX(Fruto) AS frutos, CONVERT(char(5),CAST(round(AVG(Presion),2) AS decimal(9,2))) AS Promedio, usuario\n"+
                "FROM Presiones\n" +
                "WHERE Fecha='" + str(fecha) + "' AND Hora='" + str(hora) + "'\n"
                "GROUP BY Empaque, Fecha, Hora, usuario")
        cursor.execute(sql5)
        consulta = cursor.fetchone()
        if consulta:
            lista_datos = []
            for i in consulta:
                dato = str(i)
                lista_datos.append(dato)
            return lista_datos
    except Exception as e:
            print(e)
    finally:
        cursor.close()
        conexion.close()

def delete_png_files():
    directory = "App/API/media/images/Calidad/reportes_presiones"
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            os.remove(os.path.join(directory, filename))

def descarga_pdf_control_camaras(request, filename):
    nombre = filename
    filename = 'App/Empaque/data/pdf/' + filename
    if os.path.exists(filename):
        response = serve(request, os.path.basename(filename), os.path.dirname(filename))
        response['Content-Disposition'] = f'attachment; filename="{nombre}"'
        return response
    else:
        raise Http404

def modelo():
    try:
        ZetoneApp = zetoneApp()
        cursorZetoneApp = ZetoneApp.cursor()
        Consulta_SQL = ("SELECT nombrePDF FROM Pdf_Generados WHERE nombrePDF=''")
        cursorZetoneApp.execute(Consulta_SQL)
        consultaPDF = cursorZetoneApp.fetchone()
        if consultaPDF:
            pdf = "Reporte_Camaras_Calidad_.pdf"
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