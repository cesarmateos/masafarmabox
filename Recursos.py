import os.path
from tkinter import *
from tkinter import font as tkFont
from tkinter.tix import INTEGER
from PIL import Image, ImageTk
import ctypes
import math
from configparser import ConfigParser


#Colores
COLOR_MORADO = '#76608A'
COLOR_MORADO_SUAVE = '#C5ADF2'
COLOR_MORADO_MUY_SUAVE = '#FCF2FF'
COLOR_MORADO_OSCURO = '#432D57'
COLOR_NARANJA = '#FF9933'
COLOR_NARANJA_SUAVE ='#FCD2A2'
COLOR_NARANJA_MUY_SUAVE ='#FCEFEA'
COLOR_FONDO = 'white'


#Otras Constantes
TITULO = 'MASAfarmabox 1.0'
ALTO_RAYA = 3
MARGEN_X = 20
FUENTE_PRINCIPAL = "Verdana"
FILAS_MAX = 20
COLUMNA_MAX = 4


#VARIABLES GLOBALES CONFIG
puertoScanner1 = ''
puertoScanner2 = ''
baudScanner1 = ''
baudScanner2 = ''
nombreBase = ''
delayScanner = 0.1
feed = 350
backfeed = 200

#FUNCIONES
def leerConfig():
    configParser = ConfigParser()   
    rutaConfig = rutaArchivo('config.ini')
    configParser.read(rutaConfig)

    global puertoScanner1
    global puertoScanner2
    global baudScanner1
    global baudScanner2
    global nombreBase
    global delayScanner
    global feed
    global backfeed
    puertoScanner1 = configParser.get('Scanner1', 'PUERTO')
    puertoScanner2= configParser.get('Scanner2', 'PUERTO')
    baudScanner1 = configParser.get('Scanner1', 'BAUD')
    baudScanner2 = configParser.get('Scanner2', 'BAUD')
    nombreBase = configParser.get('Base', 'ARCHIVO')
    delayScanner = float(configParser.get('Sincronizacion', 'TOLERANCIA'))
    feed = configParser.get('Impresora','feed')
    backfeed = configParser.get('Impresora','feed')

def modificarConfig(grupo,item,dato):
    configParser = ConfigParser()  
    rutaConfig = rutaArchivo('config.ini')

    configParser.read(rutaConfig)
    archivo = open(rutaConfig, 'w')
    configParser.set(grupo, item, dato)
    configParser.write(archivo)
    archivo.close()    

def rutaArchivo(archivo):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(BASE_DIR, archivo)

def esCubetaChica(cubeta):
    moducloCubeta = cubeta % 100000
    if moducloCubeta > 40000:
        return False
    return True

def linea(contenedor, ancho, fila, cantidadColumnas):
    retorno = Canvas(contenedor, width=ancho, height=ALTO_RAYA,bg='white',highlightthickness=0)
    retorno.create_line(0, 1, ancho, 1)
    retorno.grid(row=fila,column=0,columnspan=cantidadColumnas,sticky=N,pady=(0,0))
    return retorno

def botonPrincipal(contenedor, texto,command):
    retorno = Btn(contenedor, text=texto,imagenNormal='BotonMini.png', wraplength=150, justify=CENTER, imagenHover='BotonMiniHover.png',command=command) 
    return retorno

def botonSecundario(contenedor, texto,command):
    retorno = Btn(contenedor, text=texto,imagenNormal='BotonMiniGris.png', wraplength=180, justify=CENTER, imagenHover='BotonMiniHover.png',command=command) 
    return retorno

def botonMicro(contenedor, texto, command):
    return Btn(contenedor, text=texto,imagenNormal='BotonMicro.png', wraplength=95, justify=CENTER, imagenHover='BotonMicroHover.png',command=command) 

def igualarColumnas(contenedor, columnas):
    for columna in range(columnas):
        contenedor.columnconfigure(columna,weight=1)

def imprimirTicket(recepcion):
    rutaLibreria = rutaArchivo("Libs/TSCLIB.dll")
    tsclibrary = ctypes.WinDLL(rutaLibreria);

    tsclibrary.openportW("USB");

    xChicos1 = 10
    xChicos2 = 140
    xChicos3 = 270
    xGrandes1 = 420
    xGrandes2 = 550
    xGrandes3 = 680
    yFarmabox = 180
    interlineado = 30
    sizeFuenteFB = 28

    tsclibrary.setup("SIZE 100 mm, 63 mm")
    tsclibrary.sendcommandW("DIRECTION 1")
    tsclibrary.sendcommandW("GAP 0,0")
    tsclibrary.sendcommandW("CLS")
    tsclibrary.sendcommandW("BACKFEED "+backfeed)
    tsclibrary.windowsfontW("10","10","34","0", "0", "0", "Arial",recepcion.transportista[1]+ " - "+ recepcion.transportista[4])
    tsclibrary.windowsfontW("590","10","34","0", "0", "0", "Arial","Recep: "+str(recepcion.nroRecepcion).zfill(8))
    tsclibrary.windowsfontW("10","50","34","0", "0", "0", "Arial",recepcion.transportista[2])
    tsclibrary.windowsfontW("50","55","26","0", "0", "0", "Arial","("+ recepcion.transportista[3]+")")
    tsclibrary.windowsfontW("545","50","34","0", "0", "0", "Arial",recepcion.fecha)
    tsclibrary.windowsfontW("135","120","50","0", "0", "1", "Arial","Chicos")
    tsclibrary.windowsfontW("540","120","50","0", "0", "1", "Arial","Grandes")

    columnaMasLarga = math.ceil(max(recepcion.cantidadChicos(),recepcion.cantidadGrandes())/3)


    for i, farmabox in enumerate(recepcion.chicosOrdenados()):
        if i < columnaMasLarga:
            tsclibrary.windowsfontW(str(xChicos1),str(yFarmabox + interlineado*i),str(sizeFuenteFB),"0", "0", "0", "Arial",str(farmabox)) 
        elif i < columnaMasLarga *2:
            tsclibrary.windowsfontW(str(xChicos2),str(yFarmabox + interlineado*(i-columnaMasLarga)),str(sizeFuenteFB),"0", "0", "0", "Arial",str(farmabox))
        else :
            tsclibrary.windowsfontW(str(xChicos3),str(yFarmabox + interlineado*(i-columnaMasLarga*2)),str(sizeFuenteFB),"0", "0", "0", "Arial",str(farmabox))
   
    for i, farmabox in enumerate(recepcion.grandesOrdenados()):
        if i < columnaMasLarga:
            tsclibrary.windowsfontW(str(xGrandes1-25),str(yFarmabox + interlineado*i),str(sizeFuenteFB),"0", "0", "0", "Arial","║")
            tsclibrary.windowsfontW(str(xGrandes1),str(yFarmabox + interlineado*i),str(sizeFuenteFB),"0", "0", "0", "Arial",str(farmabox))
        elif i < columnaMasLarga *2:
            tsclibrary.windowsfontW(str(xGrandes2),str(yFarmabox + interlineado*(i-columnaMasLarga)),str(sizeFuenteFB),"0", "0", "0", "Arial",str(farmabox))
        else :
            tsclibrary.windowsfontW(str(xGrandes3),str(yFarmabox + interlineado*(i-columnaMasLarga*2)),str(sizeFuenteFB),"0", "0", "0", "Arial",str(farmabox))


    tsclibrary.windowsfontW(str(xChicos1),str(yFarmabox + interlineado*(columnaMasLarga+1)),str(sizeFuenteFB),"0", "0", "0", "Arial","Total Chicos : "+str(recepcion.cantidadChicos()))
    tsclibrary.windowsfontW(str(xChicos1),str(yFarmabox + interlineado*(columnaMasLarga+2)),str(sizeFuenteFB),"0", "0", "0", "Arial","Total Grandes : "+str(recepcion.cantidadGrandes()))
    tsclibrary.windowsfontW(str(xChicos1),str(yFarmabox + interlineado*(columnaMasLarga+3)),str(sizeFuenteFB),"0", "0", "0", "Arial","Tapas : "+str(recepcion.tapas))

    tsclibrary.printlabelW("1","1")
    tsclibrary.sendcommandW("FEED "+feed)
    tsclibrary.closeport()


#CLASES

class Btn(Button):

    def __init__(self, root, imagenNormal, imagenHover, *args, **kwargs):

        fuente = tkFont.Font(family=FUENTE_PRINCIPAL, size=12, weight=tkFont.BOLD) 
        
        super().__init__(root, fg='white',compound=CENTER,background=COLOR_FONDO,highlightbackground=COLOR_FONDO, font=fuente,highlightthickness=0,borderwidth=0, *args, **kwargs)

        img1 = rutaArchivo('Imagenes/'+imagenNormal)
        img2 = rutaArchivo('Imagenes/'+imagenHover)

        self.img = ImageTk.PhotoImage(Image.open(img1))
        self.img2 = ImageTk.PhotoImage(Image.open(img2))

        self['image'] = self.img
        
        self.bind('<Enter>', self.enter)
        self.bind('<Leave>', self.leave)
        
    def enter(self, event):
        self.config(image=self.img2)

    def leave(self, event):
        self.config(image=self.img)

class ScrollableFrame(Frame):
    
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class VentanaHija():
    def __init__(self,ventanaMadre,ancho,alto,titulo):
        self.ventanaMadre = ventanaMadre
        self.ventana = Toplevel(ventanaMadre)
        self.ventana.title(titulo)
        self.ventana.geometry(str(ancho)+"x"+str(alto))
        self.ventana.resizable(0, 0)
        self.ventana.configure(bg=COLOR_FONDO)
        rutaIcono = rutaArchivo('Imagenes/Pantuflas.ico')
        self.ventana.iconbitmap(rutaIcono)
        self.altoLinea = 1
        frameLinea = Frame(self.ventana,height=self.altoLinea,width=ancho, background=COLOR_FONDO)
        frameLinea.pack(fill='both')
        self.contenedor = Frame(self.ventana,height=alto-self.altoLinea,width=ancho, background=COLOR_FONDO)
        self.contenedor.pack(fill='both', expand=True)
        linea(frameLinea,ancho,0,1)
