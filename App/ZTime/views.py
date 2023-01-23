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

def calcRegistros(request):
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
                        resultado = {'legajo': i[0], 'nombre': i[1], 'fecha': i[2], 'f1': i[3], 'f2': i[4], 'f3': i[5], 'f4': i[6], 'dia': dia, 'hm':i[7], 'ht': i[8], 'ex': i[9]}
                        registro.append(resultado)
                    #print(registro)
                    print("hola?")
                    return render (request, 'ZTime/registros/viewRegister.html', {'registroHtml': registro})
                else:
                    print("no hay nada")
                    return render (request, 'ZTime/registros/viewRegister.html')
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
                registro = []
                try:
                    ZT = ZetoneTime()
                    cursorZT = ZT.cursor()
                    sql4 = ("SELECT Legajo, Nombre, Fecha, F1, F2, F3,F4, HorasF1F2, HorasF3F4, HorasDeMas\n" +
                            "FROM TemporalHoras\n" +
                            "WHERE Fecha >= '"+ str(desdeSql) +"' AND Fecha <= '"+ str(hastaSql) +"'\n" +
                            "ORDER BY Legajo, Fecha , Nombre")
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
                            resultado = {'legajo': i[0], 'nombre': i[1], 'fecha': i[2], 'f1': i[3], 'f2': i[4], 'f3': i[5], 'f4': i[6], 'dia': dia, 'hm':i[7], 'ht': i[8], 'ex': i[9]}
                            registro.append(resultado)
                        #print(registro)
                        print("hola?")
                    return render (request, 'ZTime/registros/viewRegister.html', {'registroHtml': registro})
                except Exception as e:
                    print("Error")
                    print(e)
            else:
                return render (request, 'ZTime/registros/viewRegister.html')
    else:
        print("renderiza")
        return render (request, 'ZTime/registros/viewRegister.html')


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
            hastaSql = datetime.strptime(str(hasta), "%Y-%m-%d").strftime("%d/%m/%Y")
            try:
                registro = []
                ZT = ZetoneTime()
                cursorZT = ZT.cursor()
                sql4 = ("SELECT DISTINCT\n" +
                                        "LEFT(CONVERT(varchar, iclock_transaction_1.punch_time, 108), 2) AS soloHora, iclock_transaction_1.emp_code AS Legajo, LEFT(Legajos.Nombre, 28) AS Nombre, CONVERT(varchar(10), iclock_transaction_1.punch_time, 103) AS Fecha, \n" +
                                        "CONVERT(varchar, iclock_transaction_1.punch_time, 108) AS Hora, iclock_transaction_1.punch_time AS FechaHora\n" +
                        "FROM            servidordb.zkbiotime.dbo.iclock_transaction AS iclock_transaction_1 INNER JOIN\n" +
                                                "Legajos ON iclock_transaction_1.emp_code = Legajos.Legajos\n" +
                        "WHERE      iclock_transaction_1.emp_code = '"+str(legajo)+"' AND (CONVERT(varchar(10), iclock_transaction_1.punch_time, 103) >= '"+str(desdeSql)+"') AND (CONVERT(varchar(10), iclock_transaction_1.punch_time, 103) <= '"+str(hastaSql)+"') AND \n" +
                                                    "(iclock_transaction_1.emp_code > '100099')\n" +
                        "ORDER BY Legajo, FechaHora")
                cursorZT.execute(sql4)
                consultaZT = cursorZT.fetchall()
                if consultaZT:
                    for i in consultaZT:
                        dia = fechaNombre(str(i[3]))
                        resultado = {'legajo': i[1], 'nombre': i[2], 'fecha': i[3], 'hora': i[4], 'dia': dia}
                        registro.append(resultado)
                    #print(registro)
                    print("hola?")
                    return render (request, 'ZTime/registros/ver.html', {'registroHtml': registro})
                else:
                    print("no hay nada")
                    return render (request, 'ZTime/registros/ver.html')
            except Exception as e:
                print("Error")
                print(e)
        else:
            departamento = form.cleaned_data['departamento']
            desde = form.cleaned_data['desde']
            hasta = form.cleaned_data['hasta']
            desdeSql = datetime.strptime(str(desde), "%Y-%m-%d").strftime("%d/%m/%Y")
            hastaSql = datetime.strptime(str(hasta), "%Y-%m-%d").strftime("%d/%m/%Y")
            print("no valido")
            if departamento == "Todos":
                print("")
                try:
                    registro = []
                    ZT = ZetoneTime()
                    cursorZT = ZT.cursor()
                    sql4 = ("SELECT DISTINCT\n" +
                                            "LEFT(CONVERT(varchar, iclock_transaction_1.punch_time, 108), 2) AS soloHora, iclock_transaction_1.emp_code AS Legajo, LEFT(Legajos.Nombre, 28) AS Nombre, CONVERT(varchar(10), iclock_transaction_1.punch_time, 103) AS Fecha, \n" +
                                            "CONVERT(varchar, iclock_transaction_1.punch_time, 108) AS Hora, iclock_transaction_1.punch_time AS FechaHora\n" +
                            "FROM            servidordb.zkbiotime.dbo.iclock_transaction AS iclock_transaction_1 INNER JOIN\n" +
                                                    "Legajos ON iclock_transaction_1.emp_code = Legajos.Legajos\n" +
                            "WHERE      (CONVERT(varchar(10), iclock_transaction_1.punch_time, 103) >= '"+str(desdeSql)+"') AND (CONVERT(varchar(10), iclock_transaction_1.punch_time, 103) <= '"+str(hastaSql)+"') AND \n" +
                                                        "(iclock_transaction_1.emp_code > '100099')\n" +
                            "ORDER BY Legajo, FechaHora")
                    cursorZT.execute(sql4)
                    consultaZT = cursorZT.fetchall()
                    if consultaZT:
                        for i in consultaZT:
                            dia = fechaNombre(str(i[3]))
                            resultado = {'legajo': i[1], 'nombre': i[2], 'fecha': i[3], 'hora': i[4], 'dia': dia}
                            registro.append(resultado)
                        #print(registro)
                        print("hola?")
                        return render (request, 'ZTime/registros/ver.html', {'registroHtml': registro})
                    else:
                        print("no hay nada")
                        return render (request, 'ZTime/registros/ver.html')
                except Exception as e:
                    print("Error")
                    print(e)
    return render (request, 'ZTime/registros/ver.html')