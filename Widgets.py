from tkinter import *
from tkinter import font as tkFont
from PIL import Image, ImageTk

import os
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

def linea(contenedor, ancho, fila, cantidadColumnas, **kwargs):
    retorno = Canvas(contenedor, width=ancho, height=3,bg='white',highlightthickness=0)
    retorno.create_line(0, 1, ancho, 1, **kwargs)
    retorno.grid(row=fila,column=0,columnspan=cantidadColumnas,sticky=NW,pady=0,padx=0)
    return retorno

def botonPrincipal(contenedor, texto,command):
    retorno = Btn(contenedor, text=texto,imagenNormal='BotonPrincipal.png', wraplength=130, justify=CENTER, imagenHover='BotonSobre.png',command=command) 
    return retorno

def botonSecundario(contenedor, texto,command):
    retorno = Btn(contenedor, text=texto,imagenNormal='BotonSecundario.png', wraplength=130, justify=CENTER, imagenHover='BotonSobre.png',command=command) 
    return retorno

def botonMicroNaranja(contenedor, texto, command):
    return Btn(contenedor, text=texto,imagenNormal='BotonMicroNaranja.png', wraplength=95, justify=CENTER, imagenHover='BotonMicroHover.png',command=command) 

def botonMicroMorado(contenedor, texto, command):
    return Btn(contenedor, text=texto,imagenNormal='BotonMicroMorado.png', wraplength=95, justify=CENTER, imagenHover='BotonMicroHover.png',command=command) 

def igualarColumnas(contenedor, columnas):
    for columna in range(columnas):
        contenedor.columnconfigure(columna,weight=1)

#CLASES

class Btn(Button):

    def __init__(self, root, imagenNormal, imagenHover, *args, **kwargs):

        fuente = tkFont.Font(family=FUENTE_PRINCIPAL, size=11, weight=tkFont.BOLD) 
        
        super().__init__(root, fg='white',compound=CENTER,background=COLOR_FONDO,highlightbackground=COLOR_FONDO, font=fuente,highlightthickness=0,borderwidth=0, *args, **kwargs)
  
        img1 = Recursos.rutaArchivo('Recursos/Imagenes/'+imagenNormal)
        img2 = Recursos.rutaArchivo('Recursos/Imagenes/'+imagenHover)

        if os.path.exists(img1):
            self.img = ImageTk.PhotoImage(Image.open(img1))
            self['image'] = self.img
            self.bind('<Leave>', self.leave)

            if os.path.exists(img2):  
                self.img2 = ImageTk.PhotoImage(Image.open(img2))
                self.bind('<Enter>', self.enter) 
        else:
            self.configure(background=COLOR_MORADO_OSCURO, width=15, height=2,highlightthickness=1,borderwidth=1)    
        
    def enter(self, event):
        self.config(image=self.img2)

    def leave(self, event):
        self.config(image=self.img)

class Toggle(Button):
    def __init__(self, root, variableToggle,  *args, **kwargs):

        fuente = tkFont.Font(family=FUENTE_PRINCIPAL, size=11, weight=tkFont.BOLD)    
        super().__init__(root, fg='white',compound=CENTER,background=COLOR_FONDO,highlightbackground=COLOR_FONDO, font=fuente,highlightthickness=0,borderwidth=0, *args, **kwargs)
  
        self.imgSiRaw = Recursos.rutaArchivo('Recursos/Imagenes/ToggleSi.png')
        self.imgNoRaw = Recursos.rutaArchivo('Recursos/Imagenes/ToggleNo.png')
        

        if variableToggle == 0:
            if os.path.exists(self.imgNoRaw):
                self.imgNo = ImageTk.PhotoImage(Image.open(self.imgNoRaw))
                self['image'] = self.imgNo
            else:
                self.configure(background=COLOR_MORADO_OSCURO, width=15, height=2,highlightthickness=1,borderwidth=1)   
        else:
            if os.path.exists(self.imgSiRaw):
                self.imgSi = ImageTk.PhotoImage(Image.open(self.imgSiRaw))
                self['image'] = self.imgSi
            else:
                self.configure(background=COLOR_NARANJA_SUAVE, width=15, height=2,highlightthickness=1,borderwidth=1)   
            

    def switch(self,variableToggle, identificadorConfig):

        if variableToggle == 0:
            if os.path.exists(self.imgSiRaw):
                self.imgSi = ImageTk.PhotoImage(Image.open(self.imgSiRaw))
                self['image'] = self.imgSi
            else:
                self.configure(background=COLOR_MORADO_OSCURO, width=15, height=2,highlightthickness=1,borderwidth=1)  
            Recursos.modificarConfig('Ticket',identificadorConfig,'1')
        else:
            if os.path.exists(self.imgNoRaw):
                self.imgNo = ImageTk.PhotoImage(Image.open(self.imgNoRaw))
                self['image'] = self.imgNo
            else:
                self.configure(background=COLOR_NARANJA_SUAVE, width=15, height=2,highlightthickness=1,borderwidth=1)   
            Recursos.modificarConfig('Ticket',identificadorConfig,'0')
        Recursos.leerConfig()

class VentanaHija():
    def __init__(self,ventanaMadre,ancho,alto,titulo):
        self.ventanaMadre = ventanaMadre
        self.ventana = Toplevel(ventanaMadre)
        self.ventana.title(titulo)
        self.ventana.geometry(str(ancho)+"x"+str(alto))
        self.ventana.resizable(0, 0)
        self.ventana.configure(bg=COLOR_FONDO)
        rutaIcono = Recursos.rutaArchivo('Recursos/Imagenes/Pantuflas.ico')
        if os.path.exists(rutaIcono):
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
        linea1.grid(pady=(11,0))
        Label(self, text=titulo,font="Verdana 12 bold",bg=COLOR_MORADO_SUAVE,fg=COLOR_MORADO,anchor=CENTER).grid(row=1,column=0,sticky=EW)
        linea2 = linea(self,ancho,2,1)
        linea2.grid(pady=(0,2))
        self.contenido = Frame(self,width=ancho,background=COLOR_FONDO)
        self.contenido.grid(row=3,column=0,sticky=EW)

