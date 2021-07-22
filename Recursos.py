import os.path
from tkinter import *
from tkinter import font as tkFont
from PIL import Image, ImageTk
import serial
from threading import Thread
from threading import Semaphore
from time import sleep
import ctypes
import math
from configparser import ConfigParser


#CONSTANTES
TITULO = 'MASAfarmabox 1.0'
ANCHO_VENTANA = 900
ALTO_FRAME_SUPERIOR = 60
ALTO_FRAME_TITULOS = 50
ALTO_FRAME_INFERIOR = 70
ALTO_FRAME_MEDIO = 530
ALTO_RAYA = 3
COLOR_MORADO = '#76608A'
COLOR_MORADO_SUAVE = '#C5ADF2'
COLOR_MORADO_MUY_SUAVE = '#FCF2FF'
COLOR_MORADO_OSCURO = '#432D57'
COLOR_NARANJA = '#FF9933'
COLOR_NARANJA_SUAVE ='#FCD2A2'
COLOR_NARANJA_MUY_SUAVE ='#FCEFEA'
COLOR_FONDO = 'white'
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
delayScanner = 0

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
    puertoScanner1 = configParser.get('Scanner1', 'PUERTO')
    puertoScanner2= configParser.get('Scanner2', 'PUERTO')
    baudScanner1 = configParser.get('Scanner1', 'BAUD')
    baudScanner2 = configParser.get('Scanner2', 'BAUD')
    nombreBase = configParser.get('Base', 'ARCHIVO')
    delayScanner = float(configParser.get('Sincronizacion', 'TOLERANCIA'))

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
    yFarmabox = 190
    interlineado = 30
    sizeFuenteFB = 28

    tsclibrary.setup("SIZE 100 mm, 63 mm")
    tsclibrary.sendcommandW("DIRECTION 1")
    tsclibrary.sendcommandW("GAP 0,0")
    tsclibrary.sendcommandW("CLS")
    tsclibrary.windowsfontW("600","10","34","0", "0", "0", "Arial","Recepción : "+str(recepcion.nroRecepcion))
    tsclibrary.windowsfontW("10","10","34","0", "0", "0", "Arial",recepcion.fecha)
    tsclibrary.windowsfontW("10","60","34","0", "0", "0", "Arial",recepcion.transportista[1])
    tsclibrary.windowsfontW("135","130","50","0", "0", "1", "Arial","Chicos")
    tsclibrary.windowsfontW("540","130","50","0", "0", "1", "Arial","Grandes")

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
    tsclibrary.sendcommandW("FEED 400")
    tsclibrary.closeport()


#CLASES
class Recepcion:
    def __init__(self,transportista) -> None:
        self.transportista = transportista
        self.listaFarmaboxChico = []
        self.listaFarmaboxGrande = []
        self.tapas = 0
        self.rechazados = 0
    
    def agregarFarmabox(self, ventana, nroFB):
        nroCubeta = int(nroFB)
        if esCubetaChica(nroCubeta):
            if nroCubeta in self.listaFarmaboxChico:
                self.farmaboxRechazado(ventana,nroCubeta,nroCubeta)
            else:
                self.listaFarmaboxChico.append(nroCubeta)
                ventana.nuevoFarmaboxChico(nroFB,self.cantidadChicos())
        else:
            if nroCubeta in self.listaFarmaboxGrande:
                self.farmaboxRechazado(ventana,nroCubeta,nroCubeta)
            else:
                self.listaFarmaboxGrande.append(nroCubeta)
                ventana.nuevoFarmaboxGrande(nroFB,self.cantidadGrandes())


    def agregarTapas(self,tapas):
        self.tapas = tapas

    def farmaboxRechazado(self,ventana,nroFBA, nroFBB):
        self.rechazados += 1
        ventana.nuevoRechazado()

    def cantidadChicos(self):
        return len(self.listaFarmaboxChico)
    
    def cantidadGrandes(self):
        return len(self.listaFarmaboxGrande)
    
    def setNroRecepcion(self, nroRecepcion):
        self.nroRecepcion = nroRecepcion
    
    def setFecha(self,fecha):
        self.fecha = fecha

    def chicosOrdenados(self):
        self.listaFarmaboxChico.sort()
        return self.listaFarmaboxChico

    def grandesOrdenados(self):
        self.listaFarmaboxGrande.sort()
        return self.listaFarmaboxGrande
   
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

class ManagerScanner():
    def __init__(self,ventana):
        self.ventana = ventana
        self.semaforo = Semaphore()
        self.lectura = False
        self.dato = 0
        self.lector1 = LectorPuerto(puertoScanner1,baudScanner1,self)
        self.lector2 = LectorPuerto(puertoScanner2,baudScanner2,self)

        if self.lector1 != None :
            self.lector1.iniciar()

        if self.lector2 != None :
            self.lector2.iniciar()      
    
    def recibirDato(self,dato):
        sleep(delayScanner)
        self.ventana.recibirDatos(self.dato,dato)
        self.dato = 0

class LectorPuerto():
    def __init__(self,com,baud,managerScanner):
        self.com = com
        self.baudrate = int(baud)
        self.manager = managerScanner

    def iniciar(self):
        self.hilo = Thread(target=self.hiloLector)
        self.hilo.daemon = True
        self.hilo.start()

    def hiloLector(self):
        self.puerto = serial.Serial(self.com,self.baudrate)
        self.abrirPuerto()
        self.escuchar() 

    def terminarHilo(self):
        if self.puerto != None:
            self.puerto.close()
        self.hilo.join()

    def abrirPuerto(self):
        try:
            self.puerto.close()
            self.puerto.open()
        except Exception as e:
            print("Error al abrir puerto Serial: " + str(e))
            exit()

    def escuchar(self):
        if self.puerto.isOpen():
            print("Puerto Serial "+self.com+" abierto")
            dato = []
            try:
                while True:

                    c = self.puerto.read()
            
                    if c.decode('Ascii') != '\r':
                        dato.append(c.decode('Ascii'))
                    else :
                        numeroGenerado = int(''.join(dato))
                        self.manager.semaforo.acquire()

                        if self.manager.lectura:
                            self.manager.dato = numeroGenerado
                            dato = []
                            self.manager.semaforo.release()
                        else:    
                            self.manager.lectura = True
                            self.manager.semaforo.release()
                            self.manager.recibirDato(numeroGenerado)
                            self.manager.lectura = False
                            dato = []
                        
            except Exception as e1:
                print ("Error en comunicación...: " + str(e1))

        else:
            print("No se puede abrir el puerto Serial ")
            exit()