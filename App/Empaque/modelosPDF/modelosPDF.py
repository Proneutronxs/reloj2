from fpdf import FPDF
import base64


###DECODIFICADOR DE IMAGENES
def decode_base64_to_image(index, fecha, hora, id, base64_string):
    image_bytes = base64.b64decode(base64_string)
    nombre_imagen = "image_" + str(index) + "_" + str(fecha) + "_" + str(hora) + "_" + str(id) + ".JPEG"
    with open("App/Empaque/data/images/" + nombre_imagen, "wb") as image:
        image.write(image_bytes)
    return nombre_imagen


##CONTROL DE CAMARAS
class control_camaras_PDF(FPDF):
    def header(self):
        self.set_font('Arial', '', 15)
        self.rect(x=10,y=14,w=190,h=19)
        self.image('App/Empaque/data/images/Logo.png', x=10, y=17, w=10, h=6)
        self.text(x=21, y=22, txt= 'EMPRESA ZETONE')
        self.line(72,14,72,26)
        self.set_font('Arial', 'B', 13)
        self.text(x=74, y=22, txt= 'DEPARTAMENTO DE CALIDAD')
        self.set_font('Arial', '', 10)
        self.text(x=146, y=18, txt= 'Tipo de Documento:')
        self.set_font('Arial', 'B', 10)
        self.text(x=180, y=25, txt= 'REPORTE')
        self.line(10,26,200,26)
        self.set_font('Arial', '', 10)
        self.text(x=16, y=31, txt= 'Título de Documento:')
        self.set_font('Arial', 'B', 13)
        self.text(x=82, y=31, txt= 'CONTROL DE CÁMARAS')
        self.line(145,14,145,33)
        self.set_font('Arial', 'B', 10)
        self.text(x=146, y=32, txt= 'Código: s/n')
        self.set_font('Times', 'I', 12)
        self.text(x=146, y=40, txt= 'Establecimiento: Planta Uno')
        self.line(10,41,200,41)
        #self.set_font('Arial', 'B', 10)
        #self.line(140,39,140,44)
        #self.text(x=155, y=43, txt= 'OBSERVACIONES')
        self.ln(38)

    def footer(self):
        self.set_font('Arial', 'B', 10)
        self.set_y(-18)
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'R')
        self.rect(x=10,y=276,w=190,h=15.5)
        self.text(x=18, y=280, txt= 'Realizó:')
        self.line(40,276,40,291)
        self.text(x=48, y=280, txt= 'Fecha:')
        self.line(70,276,70,291)
        self.text(x=100, y=280, txt= 'Revisó:')
        self.text(x=92, y=286, txt= 'Eduardo Córdoba')
        self.line(150,276,150,291)
        self.text(x=152.5, y=280, txt= 'Versión:')
        self.text(x=156.5, y=286, txt= '0.1')
        self.line(170,276,170,291)
        self.ln(250)