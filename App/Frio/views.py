from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
import psutil
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import zipfile
from django.http import HttpResponse, Http404

# Create your views here.

@login_required
def indexFrio(request):
    return render (request, 'Frio/Inicio/index.html')#### AHORA PASA A SER ADMINISTRACIÓN

@login_required
def control_camaras(request):
    return render (request, 'Frio/ControlCamaras/ControlTemp.html')


###VISTAS DE ADMINISTRACIÓN DE LA PAGINA


###ESPACIO DISPONIBLE
@csrf_exempt
def espacioUsado(request):
    try:
        disk_usage = psutil.disk_usage('/')
        total_gb = disk_usage.total / (1024 ** 3)
        used_gb = disk_usage.used / (1024 ** 3)
        free_gb = disk_usage.free / (1024 ** 3)
        datos = (f"Uso: {used_gb:.2f} Gb. / Total: {total_gb:.2f} Gb.")
        jsonList = json.dumps({'message': 'Success', 'datos': datos}) 
        return JsonResponse(jsonList, safe=False)
    except Exception as e:
        error = str(e)
        jsonList = json.dumps({'message': error}) 
        return JsonResponse(jsonList, safe=False)
    
###GENERAR ZIP DE PDF
@csrf_exempt
def zipPDF(request):
    pdf_folder_path = 'App/Empaque/data/pdf'
    zip_file_path = 'App/Empaque/data/pdf/archivos_pdf.zip'
    try:
        pdf_files = [os.path.join(pdf_folder_path, f) for f in os.listdir(pdf_folder_path) if f.endswith('.pdf')]
        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            for pdf_file in pdf_files:
                zip_file.write(pdf_file, os.path.basename(pdf_file), compress_type=zipfile.ZIP_DEFLATED)
        zip = "archivos_pdf.zip"
        jsonList = json.dumps({'message': 'Success', 'zip': zip}) 
        return JsonResponse(jsonList, safe=False)
    except Exception as e:
        error = str(e)
        jsonList = json.dumps({'message': error}) 
        return JsonResponse(jsonList, safe=False)
    
@csrf_exempt
def download_zip(request,zip_name):
    file_full_path = 'App/Empaque/data/pdf/' + str(zip_name)
    if os.path.exists(file_full_path):
        with open(file_full_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_full_path)
            return response
    else:
        raise Http404

###BORRA ARCHIVOS PDF Y ZIP   
@csrf_exempt
def borrar_pdf_zip(request):
    directory = 'App/Empaque/data/pdf'
    try:
        for file in os.listdir(directory):
            if file.endswith('.pdf') or file.endswith('.zip'):
                os.remove(os.path.join(directory, file))
        jsonList = json.dumps({'message': 'Success'}) 
        return JsonResponse(jsonList, safe=False)
    except Exception as e:
        error = str(e)
        jsonList = json.dumps({'message': error}) 
        return JsonResponse(jsonList, safe=False)
    
###BORRA ARCHIVOS EXCEL
@csrf_exempt
def delete_xlsx(request):
    try:
        for filename in os.listdir('App/ZTime/data/excel/'):
            if filename.endswith(".xlsx"):
                os.remove(os.path.join('App/ZTime/data/excel/', filename))
        jsonList = json.dumps({'message':'Success'}) 
        return JsonResponse(jsonList, safe=False)
    except Exception as e:
        error = str(e)
        jsonList = json.dumps({'message':error}) 
        return JsonResponse(jsonList, safe=False)
    
@csrf_exempt
def borrar_imagenes(request):
    directory_1 = 'App/API/media/images/Calidad/reportes_empaque'
    directory_2 = 'App/API/media/images/Calidad/reportes_empaque'
    try:
        for file in os.listdir(directory_1):
            if file.endswith('.jpeg'):
                os.remove(os.path.join(directory_1, file))
        jsonList = json.dumps({'message': 'Success'}) 
        return JsonResponse(jsonList, safe=False)
    except Exception as e:
        error = str(e)
        jsonList = json.dumps({'message': error}) 
        return JsonResponse(jsonList, safe=False)
    

    