from django.shortcuts import render
from App.ZTime.forms import *
from App.ZTime.conexion import *
from datetime import datetime

# Create your views here.

def whileZetone():
    numero = 0
    while numero <= 10000:
        print(numero)
        numero = numero + 1

#whileZetone()

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

def index(request):
    return render (request, 'ZTime/inicio/index.html')

def verRegistros(request):
    if request.method == 'POST':
        form = form_ver_registros(request.POST)
        legajo = request.POST.get('legajo', 1)
        print(legajo)
        if form.is_valid():
            print("validó?")
            legajo = form.cleaned_data['legajo']
            departamento = form.cleaned_data['departamento']
            desde = form.cleaned_data['desde']
            hasta = form.cleaned_data['hasta']
            desdeSql = datetime.strptime(str(desde), "%Y-%m-%d").strftime("%d/%m/%Y")
            soloDiaDesde = datetime.strptime(str(desde), "%Y-%m-%d").strftime("%d")
            mesAñoDesde = datetime.strptime(str(desde), "%Y-%m-%d").strftime("%m/%Y")
            hastaSql = datetime.strptime(str(hasta), "%Y-%m-%d").strftime("%d/%m/%Y")
            soloDiaHasta = datetime.strptime(str(hasta), "%Y-%m-%d").strftime("%d")
            mesAñoHasta = datetime.strptime(str(hasta), "%Y-%m-%d").strftime("%m/%Y")

            print(soloDiaDesde)
            print(mesAñoDesde)
            print(soloDiaHasta)
            print(mesAñoHasta)
            print(legajo)
            print(departamento)
            print(desdeSql)
            print(hastaSql)


            try:
                ZT = ZetoneTime()
                cursorZT = ZT.cursor()
                sql4 = ("SELECT Legajo, Nombre, Fecha, F1, F2, F3,F4\n" +
                        "FROM TemporalHoras\n" +
                        "WHERE Legajo = '" + str(legajo) + "' AND (CONVERT(varchar(10), FechaHora, 103) >= '"+ str(desdeSql) +"') AND (CONVERT(varchar(10), FechaHora, 103) <= '"+ str(hastaSql) +"')")
                cursorZT.execute(sql4)
                consultaZT = cursorZT.fetchall()
                if consultaZT:
                    registro = []
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
                        resultado = {'legajo': i[0], 'nombre': i[1], 'fecha': i[2], 'f1': i[3], 'f2': i[4], 'f3': i[5], 'f4': i[6], 'dia': dia}
                        registro.append(resultado)
                    print(registro)
                    print("hola?")
                return render (request, 'ZTime/registros/viewRegister.html', {'registroHtml': registro})
            except Exception as e:
                print("Error")
                print(e)
            
        else:
            departamento = form.cleaned_data['departamento']
            desde = form.cleaned_data['desde']
            hasta = form.cleaned_data['hasta']
            desdeSql = datetime.strptime(str(desde), "%Y-%m-%d").strftime("%d/%m/%Y")
            soloDiaDesde = datetime.strptime(str(desde), "%Y-%m-%d").strftime("%d")
            hastaSql = datetime.strptime(str(hasta), "%Y-%m-%d").strftime("%d/%m/%Y")
            soloDiaHasta = datetime.strptime(str(hasta), "%Y-%m-%d").strftime("%d")

            print(soloDiaDesde)
            print(soloDiaHasta)
            print(legajo)
            print(departamento)
            print(desdeSql)
            print(hastaSql)
            print("No validó?")

            if departamento == "Todos":

                try:
                    ZT = ZetoneTime()
                    cursorZT = ZT.cursor()
                    sql4 = ("SELECT Legajo, Nombre, Fecha, F1, F2, F3,F4\n" +
                            "FROM TemporalHoras\n" +
                            "WHERE (CONVERT(varchar(10), FechaHora, 103) >= '"+ str(desdeSql) +"') AND (CONVERT(varchar(10), FechaHora, 103) <= '"+ str(hastaSql) +"')\n" +
                            "ORDER BY Legajo, Fecha , Nombre")
                    cursorZT.execute(sql4)
                    consultaZT = cursorZT.fetchall()
                    if consultaZT:
                        registro = []
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
                            resultado = {'legajo': i[0], 'nombre': i[1], 'fecha': i[2], 'f1': i[3], 'f2': i[4], 'f3': i[5], 'f4': i[6], 'dia': dia}
                            registro.append(resultado)
                        print(registro)
                        print("hola?")
                    return render (request, 'ZTime/registros/viewRegister.html', {'registroHtml': registro})
                except Exception as e:
                    print("Error")
                    print(e)
            



            return render (request, 'ZTime/registros/viewRegister.html')
    else:
        print("renderiza")
        return render (request, 'ZTime/registros/viewRegister.html')
