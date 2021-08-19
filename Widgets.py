from tkinter import *
from tkinter import font as tkFont
from PIL import Image, ImageTk

import Recursos

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
MARGEN_X = 20
FUENTE_PRINCIPAL = "Verdana"
FILAS_MAX = 20
COLUMNA_MAX = 4

def linea(contenedor, ancho, fila, cantidadColumnas):
    retorno = Canvas(contenedor, width=ancho, height=3,bg='white',highlightthickness=0)
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

#CLASES

class Btn(Button):

    def __init__(self, root, imagenNormal, imagenHover, *args, **kwargs):

        fuente = tkFont.Font(family=FUENTE_PRINCIPAL, size=12, weight=tkFont.BOLD) 
        
        super().__init__(root, fg='white',compound=CENTER,background=COLOR_FONDO,highlightbackground=COLOR_FONDO, font=fuente,highlightthickness=0,borderwidth=0, *args, **kwargs)

        img1 = Recursos.rutaArchivo('Imagenes/'+imagenNormal)
        img2 = Recursos.rutaArchivo('Imagenes/'+imagenHover)

        self.img = ImageTk.PhotoImage(Image.open(img1))
        self.img2 = ImageTk.PhotoImage(Image.open(img2))

        self['image'] = self.img
        
        self.bind('<Enter>', self.enter)
        self.bind('<Leave>', self.leave)
        
    def enter(self, event):
        self.config(image=self.img2)

    def leave(self, event):
        self.config(image=self.img)

class VentanaHija():
    def __init__(self,ventanaMadre,ancho,alto,titulo):
        self.ventanaMadre = ventanaMadre
        self.ventana = Toplevel(ventanaMadre)
        self.ventana.title(titulo)
        self.ventana.geometry(str(ancho)+"x"+str(alto))
        self.ventana.resizable(0, 0)
        self.ventana.configure(bg=COLOR_FONDO)
        rutaIcono = Recursos.rutaArchivo('Imagenes/Pantuflas.ico')
        self.ventana.iconbitmap(rutaIcono)

        altoLinea = 1
        self.altoContenedor = alto-altoLinea-ventanaMadre.altoFrameInferior


        frameLinea = Frame(self.ventana,height=altoLinea,width=ancho, background=COLOR_FONDO)
        frameLinea.pack(fill='both',side=TOP)

        self.contenedor = Frame(self.ventana,height=self.altoContenedor,width=ancho, background=COLOR_FONDO)
        self.contenedor.pack(fill=BOTH, expand=True,side=TOP)
        self.contenedor.propagate(False)
        
        self.frameInferior = Frame(self.ventana,height=ventanaMadre.altoFrameInferior,width=ancho, background=COLOR_FONDO)
        self.frameInferior.pack(fill=BOTH, expand=True,side=BOTTOM)
        self.frameInferior.propagate(False)

        linea(frameLinea,ancho,0,1)

class Seccion(Frame):
    def __init__( self, parent, titulo, **options ):

        Frame.__init__( self, parent, **options )

        ancho = self.cget('width')
        
        
        linea1 = linea(self,ancho,0,1)
        linea1.grid(pady=(15,0))
        Label(self, text=titulo,font="Verdana 12 bold",bg=COLOR_MORADO_SUAVE,fg=COLOR_MORADO,anchor=CENTER).grid(row=1,column=0,sticky=EW)
        linea(self,ancho,2,1)
        #self.contenido.grid_columnconfigure(0,weight=1)
        self.contenido = Frame(self,width=ancho,background=COLOR_FONDO)
        self.contenido.grid(row=3,column=0,sticky=EW)

