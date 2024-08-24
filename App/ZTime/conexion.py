import pyodbc

server3 = "191.97.47.114"
db3 = "ZetoneTime"
user3 = "sa"
psw3 = "Sideswipe348"

def ZetoneTime():
    try:
        Cox = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' + server3 +'; DATABASE=' + db3 + '; UID=' + user3 + '; PWD=' + psw3)
       #print("Conectado")
        return Cox
    except Exception as e:
        print(e)

server = "10.32.26.8"
db = "zkbiotime"
user = "sa"
psw = "Florencia1976"

def zkbiotime():
    try:
        Cox = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' + server +'; DATABASE=' + db + '; UID=' + user + '; PWD=' + psw)
       #print("Conectado")
        return Cox
    except Exception as e:
        print(e)


serverApp = "191.97.47.114"
dbApp = "Zetoneapp"
userApp = "sa"
pswApp = "Sideswipe348"

def zetoneApp():
    try:
        Cox = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' + serverApp +'; DATABASE=' + dbApp + '; UID=' + userApp + '; PWD=' + pswApp)
       #print("Conectado")
        return Cox
    except Exception as e:
        print(e)