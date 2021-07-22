from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from winsound import Beep
import BaseDatos
import Recursos
import Recepcion
import os
import sys


class Ventana(Tk):

    def __init__(self, *args, **kwargs):

        Tk.__init__(self, *args, **kwargs)
        
        #Color del fondo
        self.configure(bg=Recursos.COLOR_FONDO)

        #Obtengo resolución Monitor
        screen_width = Tk.winfo_screenwidth(self)
        screen_height = Tk.winfo_screenheight(self)

        # Tamaño Ventana
        self.anchoVentana = 900
        self.altoFrameSuperior = 65
        self.altoFrameMedio = 530
        self.altoFrameInferior = 70
        self.altoFrameTitulos = 50

        #Calculo margen del ancho al posicionar la ventana
        margenPosicional = str(int((screen_width - self.anchoVentana)/ 2))

         # Título e Ícono
        self.title(Recursos.TITULO)
        rutaIcono = Recursos.rutaArchivo('Imagenes/Pantuflas.ico')
        self.iconbitmap(rutaIcono)

        altoVentana = self.altoFrameInferior + self.altoFrameMedio + self.altoFrameSuperior
        self.geometry(str(self.anchoVentana)+"x"+str(altoVentana)+"+"+margenPosicional+"+10")
        self.resizable(False, False)

        #---Frame Superior----
        self.frameSuperior = Frame(self,bg=Recursos.COLOR_FONDO,height=self.altoFrameInferior)
        self.frameSuperior.pack(side = TOP, fill = BOTH, expand = TRUE)
        self.frameSuperior.propagate(False)

        #Linea Superior
        Recursos.linea(self.frameSuperior,self.anchoVentana,0,2)
          
        #Encabezado Top Izquierdo
        self.encabezado = StringVar()   
        self.subtitulo = StringVar()   
        Label(self.frameSuperior, textvariable=self.encabezado,font=(Recursos.FUENTE_PRINCIPAL, 16),background=Recursos.COLOR_FONDO).grid(row=0,column=0,sticky=W,pady=(5,0),padx=Recursos.MARGEN_X)
        Label(self.frameSuperior, textvariable=self.subtitulo,font=(Recursos.FUENTE_PRINCIPAL, 9),background=Recursos.COLOR_FONDO).grid(row=1,column=0,sticky=W,padx=Recursos.MARGEN_X)

        #Logo
        imagenLogo = PhotoImage(file=Recursos.rutaArchivo('Imagenes/Logo.png'))
        logo = Label(self.frameSuperior, image=imagenLogo,bg=Recursos.COLOR_FONDO)
        logo.photo = imagenLogo
        logo.grid(row=0,column=1,rowspan=2,sticky=N+S+E,pady=10,padx=Recursos.MARGEN_X)


        #---Frame contenedor de Widgets---
        self.contenedor = Frame(self,bg=Recursos.COLOR_FONDO,height=self.altoFrameMedio) 
        self.contenedor.pack(side = TOP, fill = X, expand = True)
        self.contenedor.propagate(False)

        #---Frame inferior---
        self.frameInferior = Frame(self,bg=Recursos.COLOR_FONDO,height=self.altoFrameInferior) 
        self.frameInferior.pack(side = BOTTOM, fill = BOTH, expand = TRUE,padx=Recursos.MARGEN_X,pady=10)
        self.frameInferior.propagate(False)

        #Lanzo la pantalla principal
        self.pantallaInicial()

        #Declaro la variable en la que se guarda el dato del segundo escaner
        self.dato2 = 0

    def pantallaInicial(self):

        #Limpio pantalla de widgets anteriores
        self.limpiarFrame()

        self.pantalla = 1


        #-------------FRAME CONTENEDOR PRINCIPAL------------
        #Texto
        Label(self.contenedor, text="Escanear código QR o ingresar manualmente",font=(Recursos.FUENTE_PRINCIPAL, 15),bg=Recursos.COLOR_FONDO).place(x=210,y=200)
        
        #Entrada de QR
        entradaQR = Entry(self.contenedor, font=(Recursos.FUENTE_PRINCIPAL,20), width=20,highlightthickness=2)
        entradaQR.focus_set()
        entradaQR.place(x=235,y=250)  

        #Boton Lupa
        botonLupa = Recursos.Btn(self.contenedor, imagenNormal='Lupa.png', imagenHover='LupaHover.png', command=lambda : self.validarTransportista(entradaQR))
        botonLupa.place(x=600,y=245) 

        #Activo el enter
        self.bind('<Return>', lambda event : self.enterPricipal(self,entradaQR))


        #-------------FRAME INFERIOR------------
        #Boton Recepciones            
        botonRecepciones = Recursos.botonPrincipal(self.frameInferior,'Recepciones',self.pantallaRecepciones)
        #botonRecepciones = Recursos.botonPrincipal(self.frameInferior,'Recepciones',lambda : PantallaRecepciones(self))
        botonRecepciones.pack(side=RIGHT, anchor=SE)

        #Boton Configuración       
        botonConfiguración = Recursos.botonPrincipal(self.frameInferior,'Configuración',self.pantallaConfiguracion)
        botonConfiguración.pack(side=LEFT, anchor=SW)
  
    def pantallaCargaRecepcion(self,recepcion):
        self.pantalla = 2

        #Limpio pantalla de widgets anteriores
        self.limpiarFrame()

        #Variable al pedo
        contenedorGeneral = self.contenedor

        #Variable de la recepción    
        self.recepcion = recepcion

        #Genero Encabezado
        self.encabezado.set(recepcion.transportista[1]+ " - "+ recepcion.transportista[4])
        self.subtitulo.set("Radio : " +recepcion.transportista[2]+"  ("+recepcion.transportista[3]+")")

        #Creo los 3 frames
        frameTitulos = Frame(contenedorGeneral,height=self.altoFrameTitulos,background=Recursos.COLOR_FONDO)
        frameTitulos.pack(side=TOP,padx=Recursos.MARGEN_X)
        altoFrameNroFarmabox = self.altoFrameMedio - (self.altoFrameTitulos*2)
        frameMedio = Frame(contenedorGeneral,height=altoFrameNroFarmabox,background=Recursos.COLOR_FONDO)
        frameMedio.pack(fill=BOTH,expand=True,padx=Recursos.MARGEN_X,side=TOP)
        frameTotales = Frame(contenedorGeneral,height=self.altoFrameTitulos,background=Recursos.COLOR_FONDO)
        frameTotales.pack(fill=Y,expand=False,padx=Recursos.MARGEN_X,side=BOTTOM)

        
        anchoLinea = self.anchoVentana-Recursos.MARGEN_X*2

        #-------------FRAME TITULOS------------ 
        #Linea1
        Recursos.linea(frameTitulos,anchoLinea,0,2) 
        
        #Títulos
        #Recursos.igualarColumnas(frameTitulos,2)
        Label(frameTitulos, text="Chicos",font=(Recursos.FUENTE_PRINCIPAL, 19),bg=Recursos.COLOR_NARANJA_SUAVE,fg=Recursos.COLOR_NARANJA,anchor=CENTER).grid(row=1,column=0,sticky=EW)
        Label(frameTitulos, text="Grandes",font=(Recursos.FUENTE_PRINCIPAL, 19),bg=Recursos.COLOR_MORADO_SUAVE,fg=Recursos.COLOR_MORADO,anchor=CENTER).grid(row=1,column=1,sticky=EW)

        #Linea2
        Recursos.linea(frameTitulos,anchoLinea,2,2) 
 

        #-------------FRAME MEDIO------------
        anchoFrameCubetas = (self.anchoVentana-Recursos.MARGEN_X*2)/2
        frameChicos = Frame(frameMedio,background=Recursos.COLOR_NARANJA_MUY_SUAVE,height=altoFrameNroFarmabox,width=anchoFrameCubetas)
        frameChicos.pack(fill='both',expand=True,side=LEFT)
        frameChicos.propagate(False)
        frameGrandes = Frame(frameMedio,background=Recursos.COLOR_MORADO_MUY_SUAVE,height=altoFrameNroFarmabox,width=anchoFrameCubetas)
        frameGrandes.propagate(False)
        frameGrandes.pack(fill='both',expand=True,side=RIGHT)
        
     
        # Creo Canvas dentro de Frame
        canvasChicos = Canvas(frameChicos, bg=Recursos.COLOR_NARANJA_MUY_SUAVE,borderwidth=0,highlightthickness=0,width=anchoFrameCubetas-45,height=altoFrameNroFarmabox)
        canvasGrandes = Canvas(frameGrandes, bg=Recursos.COLOR_MORADO_MUY_SUAVE,borderwidth=0,highlightthickness=0,width=anchoFrameCubetas-45,height=altoFrameNroFarmabox)
        canvasChicos.pack(side=LEFT,fill=BOTH,expand=TRUE)
        canvasGrandes.pack(side=LEFT,fill=BOTH,expand=TRUE)

        #Creo Frame dentro de Canvas
        self.frameScrollChicos = Frame(canvasChicos,background=Recursos.COLOR_NARANJA_MUY_SUAVE)
        self.frameScrollGrandes = Frame(canvasGrandes,background=Recursos.COLOR_MORADO_MUY_SUAVE)

        #Armo Scroll y Linkeo
        scrollChicos = Scrollbar(frameChicos,orient=VERTICAL, command=canvasChicos.yview)
        scrollChicos.pack(side=RIGHT,fill=Y)
        canvasChicos.configure(yscrollcommand=scrollChicos.set)
        canvasChicos.create_window((1,1), window=self.frameScrollChicos, anchor=NW, tags="self.frameChicos")

        scrollGrandes = Scrollbar(frameGrandes,orient=VERTICAL, command=canvasGrandes.yview)
        scrollGrandes.pack(side=RIGHT,fill=Y)
        canvasGrandes.configure(yscrollcommand=scrollGrandes.set)
        canvasGrandes.create_window((1,1), window=self.frameScrollGrandes, anchor=NW, tags="self.frameGrandes")

        #Refresh en cada agregado de celda
        self.frameScrollChicos.bind("<Configure>", lambda event: canvasChicos.config(scrollregion=canvasChicos.bbox("all")))
        self.frameScrollGrandes.bind("<Configure>", lambda event: canvasGrandes.config(scrollregion=canvasGrandes.bbox("all")))
        
        Recursos.igualarColumnas(self.frameScrollChicos,Recursos.COLUMNA_MAX)



        #-------------FRAME TOTALES------------
        Recursos.igualarColumnas(frameTotales,8)

        #DeclaroVariables de los marcadores
        self.marcadorCH = StringVar()
        self.marcadorGR = StringVar()
        self.marcadorTapas = StringVar()
        self.marcadorRechazados = StringVar()

        #Linea3
        Recursos.linea(frameTotales,anchoLinea,0,8) 
        
        #Textos
        Label(frameTotales, text="Total Chicos: ",font=(Recursos.FUENTE_PRINCIPAL, 15),bg=Recursos.COLOR_FONDO,fg='#FF9933').grid(row=1,column=0,sticky=E,pady=5)
        Label(frameTotales, text="Total Grandes: ",font=(Recursos.FUENTE_PRINCIPAL, 15),bg=Recursos.COLOR_FONDO,fg='#FF9933').grid(row=1,column=4,sticky=E,pady=5)
        Label(frameTotales, text="Total Tapas: ",font=(Recursos.FUENTE_PRINCIPAL, 15),bg=Recursos.COLOR_FONDO,fg='#FF9933').grid(row=1,column=2,sticky=E,pady=5)
        Label(frameTotales, text="Rechazados: ",font=(Recursos.FUENTE_PRINCIPAL, 15),bg=Recursos.COLOR_FONDO,fg='#FF9933').grid(row=1,column=6,sticky=E,pady=5)

        #Marcadores Dinámicos
        Label(frameTotales, textvariable=self.marcadorCH,font=(Recursos.FUENTE_PRINCIPAL, 15),bg=Recursos.COLOR_FONDO).grid(row=1,column=1,sticky=W,padx=(15,0),pady=5)
        Label(frameTotales, textvariable=self.marcadorGR,font=(Recursos.FUENTE_PRINCIPAL, 15),bg=Recursos.COLOR_FONDO).grid(row=1,column=5,sticky=W,padx=(15,0),pady=5)
        Label(frameTotales, textvariable=self.marcadorTapas,font=(Recursos.FUENTE_PRINCIPAL, 15),bg=Recursos.COLOR_FONDO).grid(row=1,column=3,sticky=W,padx=(15,0),pady=5)
        Label(frameTotales, textvariable=self.marcadorRechazados,font=(Recursos.FUENTE_PRINCIPAL, 15),bg=Recursos.COLOR_FONDO,fg='red').grid(row=1,column=7,sticky=W,padx=(15,0),pady=5)

        #Linkeo Marcadores con Contador
        self.marcadorCH.set(str(self.recepcion.cantidadChicos()))
        self.marcadorGR.set(str(self.recepcion.cantidadGrandes()))
        self.marcadorTapas.set(str(self.recepcion.tapas))
        self.marcadorRechazados.set(str(self.recepcion.rechazados))

        #Linea4
        Recursos.linea(frameTotales,anchoLinea,2,8) 
        
        #-------------FRAME INFERIOR------------
        #Boton Cancelar
        botonCancelar = Recursos.botonSecundario(self.frameInferior,'Cancelar',self.lanzarVentanaCancelaRecepcion)
        botonCancelar.grid(row=3,column=0,columnspan=2,sticky=W)

        #Boton Tapas
        botonTapas = Recursos.botonPrincipal(self.frameInferior,'Ingresar Tapas',self.lanzarVentanaTapas)         
        botonTapas.grid(row=3,column=2,columnspan=2,sticky=EW,padx=13)

        #Boton Farmabox   
        botonFarmabox = Recursos.botonPrincipal(self.frameInferior,'Ingresar Farmabox',self.lanzarVentanaFarmabox)       
        botonFarmabox.grid(row=3,column=4,columnspan=2,sticky=EW,padx=(0,13))

        #Boton Finalizar
        botonFinalizar = Recursos.botonPrincipal(self.frameInferior,'Finalizar',self.lanzarVentanaFinalizarCarga)         
        botonFinalizar.grid(row=3,column=6,columnspan=2,sticky=E)
     
    def pantallaRecepciones(self):
        self.pantalla = 3

        #Limpio pantalla de widgets anteriores
        self.limpiarFrame()
        
        #-------------FRAME SUPERIOR------------
        #Titulo
        self.encabezado.set("Buscar Recepciones")


        #-------------FRAME INFERIORR------------
        #Boton Finalizar
        botonFinalizar = Recursos.botonPrincipal(self.frameInferior,'Finalizar',self.pantallaInicial)         
        botonFinalizar.pack(anchor=SE)

    def pantallaConfiguracion(self):
        self.pantalla = 4

        #Limpio pantalla de widgets anteriores
        self.limpiarFrame()

        

        #-------------FRAME SUPERIOR------------
        #Titulo
        self.encabezado.set("Configuración")



        #-------------FRAME MEDIO------------
        anchoFrame = self.anchoVentana-Recursos.MARGEN_X*2

        

        #Armo un Frame con márgenes
        frameMedio = Frame(self.contenedor,height=self.altoFrameMedio,width=anchoFrame,background=Recursos.COLOR_FONDO)
        frameMedio.pack(fill=BOTH,expand=True,padx=Recursos.MARGEN_X,side=TOP)

        cantidadColumnas = 9
        padySeparador = 10
        Recursos.igualarColumnas(frameMedio,cantidadColumnas)

        #Valores Puertos COM
        valoresCOM = []
        for i in range (1,21):
            valoresCOM.append("COM"+str(i))

        #Valores Puertos Baud Rates
        valoresBaudios = [1200,1800,2400,4800,7200,9600,14400,19200,38400,57600,115200,128000]


        #Titulo Scanner 1
        linea1 = Recursos.linea(frameMedio,anchoFrame,0,cantidadColumnas)
        linea1.grid(pady=(padySeparador,0))
        Label(frameMedio, text=" Scanner 1",font=(Recursos.FUENTE_PRINCIPAL, 12),bg=Recursos.COLOR_MORADO_SUAVE,fg=Recursos.COLOR_MORADO,anchor=W).grid(row=1,column=0,columnspan=cantidadColumnas,sticky=EW)
        Recursos.linea(frameMedio,anchoFrame,2,cantidadColumnas)
        
        #Puerto Scanner 1
        Label(frameMedio, text="Puerto :",font="Verdana 10 bold",bg=Recursos.COLOR_FONDO,anchor=W).grid(row=3,column=0,sticky=E)
        textoPuertoScanner1Variable = StringVar()
        textoPuertoScanner1Variable.set(Recursos.puertoScanner1)
        puertoScanner1 = Label(frameMedio, textvariable=textoPuertoScanner1Variable,font=(Recursos.FUENTE_PRINCIPAL, 10),bg=Recursos.COLOR_FONDO,anchor=W)
        puertoScanner1.grid(row=3,column=1,sticky=W,padx=5)
        botonCambiarSerial1 = Recursos.botonMicro(frameMedio,"Cambiar",lambda: self.cambiarValorConfiguracion(frameMedio,textoPuertoScanner1Variable,botonCambiarSerial1,3,1,valoresCOM,'Scanner1', 'puerto'))
        botonCambiarSerial1.grid(row=3,column=2,sticky=W)

        #Baudrate Scanner 1
        Label(frameMedio, text="Baud Rate (bits por seg):",font="Verdana 10 bold",bg=Recursos.COLOR_FONDO,anchor=W).grid(padx=(20,0),row=3,column=3,columnspan=4,sticky=E)
        textoBaud1 = StringVar()
        textoBaud1.set(Recursos.baudScanner1)
        baudScanner1 = Label(frameMedio, textvariable=textoBaud1,font=(Recursos.FUENTE_PRINCIPAL, 10),bg=Recursos.COLOR_FONDO,anchor=W)
        baudScanner1.grid(row=3,column=7,sticky=W,padx=5)
        botonCambiarBaud1 = Recursos.botonMicro(frameMedio,"Cambiar",lambda: self.cambiarValorConfiguracion(frameMedio,textoBaud1,botonCambiarBaud1,3,7,valoresBaudios,'Scanner1', 'baud'))
        botonCambiarBaud1.grid(row=3,column=8,sticky=W)

        #Titulo Scanner 2
        linea2 = Recursos.linea(frameMedio,anchoFrame,4,cantidadColumnas) 
        linea2.grid(pady=(padySeparador,0))
        Label(frameMedio, text=" Scanner 2",font=(Recursos.FUENTE_PRINCIPAL, 12),bg=Recursos.COLOR_MORADO_SUAVE,fg=Recursos.COLOR_MORADO,anchor=W).grid(row=5,column=0,columnspan=cantidadColumnas,sticky=EW)
        Recursos.linea(frameMedio,anchoFrame,6,cantidadColumnas)

        #Puerto Scanner 2
        Label(frameMedio, text="Puerto :",font="Verdana 10 bold",bg=Recursos.COLOR_FONDO,anchor=W).grid(row=7,column=0,sticky=E)
        textoPuertoScanner2Variable = StringVar()
        textoPuertoScanner2Variable.set(Recursos.puertoScanner2)
        puertoScanner2 = Label(frameMedio, textvariable=textoPuertoScanner2Variable,font=(Recursos.FUENTE_PRINCIPAL, 10),bg=Recursos.COLOR_FONDO,anchor=W)
        puertoScanner2.grid(row=7,column=1,sticky=W,padx=5)
        botonCambiarSerial2 = Recursos.botonMicro(frameMedio,"Cambiar",lambda: self.cambiarValorConfiguracion(frameMedio,textoPuertoScanner2Variable,botonCambiarSerial2,7,1,valoresCOM,'Scanner2', 'PUERTO'))
        botonCambiarSerial2.grid(row=7,column=2,sticky=W)

        #Baudrate Scanner 2
        Label(frameMedio, text="Baud Rate (bits por seg):",font="Verdana 10 bold",bg=Recursos.COLOR_FONDO,anchor=W).grid(padx=(20,0),row=7,column=3,columnspan=4,sticky=E)
        textoBaud2 = StringVar()
        textoBaud2.set(Recursos.baudScanner2)
        baudScanner2 = Label(frameMedio, textvariable=textoBaud2,font=(Recursos.FUENTE_PRINCIPAL, 10),bg=Recursos.COLOR_FONDO,anchor=W)
        baudScanner2.grid(row=7,column=7,sticky=W,padx=5)
        botonCambiarBaud2 = Recursos.botonMicro(frameMedio,"Cambiar",lambda: self.cambiarValorConfiguracion(frameMedio,textoBaud2,botonCambiarBaud2,7,7,valoresBaudios,'Scanner2', 'BAUD'))
        botonCambiarBaud2.grid(row=7,column=8,sticky=W)

        #Titulo Sincronización
        linea3 = Recursos.linea(frameMedio,anchoFrame,8,cantidadColumnas) 
        linea3.grid(pady=(padySeparador,0))
        Label(frameMedio, text=" Sincronización Scanners",font=(Recursos.FUENTE_PRINCIPAL, 12),bg=Recursos.COLOR_MORADO_SUAVE,fg=Recursos.COLOR_MORADO,anchor=W).grid(row=9,column=0,columnspan=cantidadColumnas,sticky=EW)
        Recursos.linea(frameMedio,anchoFrame,10,cantidadColumnas)

        #Tolreancia
        valoresTolerancia = []
        for i in range (1,11):
            valoresTolerancia.append(str(round(i*0.05,2)))

        Label(frameMedio, text="Tolerancia (segundos): ",font="Verdana 10 bold",bg=Recursos.COLOR_FONDO,anchor=W).grid(padx=(20,0),row=11,column=0,columnspan=2,sticky=E)
        textoTolereancia = StringVar()
        textoTolereancia.set(Recursos.delayScanner)
        tolerancia = Label(frameMedio, textvariable=textoTolereancia,font=(Recursos.FUENTE_PRINCIPAL, 10),bg=Recursos.COLOR_FONDO,anchor=W)
        tolerancia.grid(row=11,column=2,sticky=W,padx=5)
        botonCambiarTolerancia = Recursos.botonMicro(frameMedio,"Cambiar",lambda: self.cambiarValorConfiguracion(frameMedio,textoTolereancia,botonCambiarTolerancia,11,2,valoresTolerancia,'Sincronizacion', 'tolerancia'))
        botonCambiarTolerancia.grid(row=11,column=3,sticky=W)

        #Titulo Base
        linea4 = Recursos.linea(frameMedio,anchoFrame,12,cantidadColumnas) 
        linea4.grid(pady=(padySeparador,0))
        Label(frameMedio, text=" Base de Datos",font=(Recursos.FUENTE_PRINCIPAL, 12),bg=Recursos.COLOR_MORADO_SUAVE,fg=Recursos.COLOR_MORADO,anchor=W).grid(row=13,column=0,columnspan=cantidadColumnas,sticky=EW)
        Recursos.linea(frameMedio,anchoFrame,14,cantidadColumnas)

        #Titulo Impresora
        linea5 = Recursos.linea(frameMedio,anchoFrame,17,cantidadColumnas) 
        linea5.grid(pady=(padySeparador,0))
        Label(frameMedio, text=" Impresora",font=(Recursos.FUENTE_PRINCIPAL, 12),bg=Recursos.COLOR_MORADO_SUAVE,fg=Recursos.COLOR_MORADO,anchor=W).grid(row=18,column=0,columnspan=cantidadColumnas,sticky=EW)
        Recursos.linea(frameMedio,anchoFrame,19,cantidadColumnas)

        #Backfeed
        valoresFeed = []
        for i in range (1,50):
            valoresFeed.append(str(i*10))

        Label(frameMedio, text="Retroseso Etiqueta Anterior: ",font="Verdana 10 bold",bg=Recursos.COLOR_FONDO,anchor=W).grid(padx=(20,0),row=20,column=0,columnspan=2,sticky=E)
        textoBackFeed = StringVar()
        textoBackFeed.set(Recursos.delayScanner)
        backFeed = Label(frameMedio, textvariable=textoBackFeed,font=(Recursos.FUENTE_PRINCIPAL, 10),bg=Recursos.COLOR_FONDO,anchor=W)
        backFeed.grid(row=20,column=2,sticky=W,padx=5)
        botonCambiarBackFeed = Recursos.botonMicro(frameMedio,"Cambiar",lambda: self.cambiarValorConfiguracion(frameMedio,textoBackFeed,botonCambiarBackFeed,20,2,valoresFeed,'Impresora', 'backfeed'))
        botonCambiarBackFeed.grid(row=20,column=3,sticky=W)
        
        Label(frameMedio, text="Alimento Etiqueta Posterior: ",font="Verdana 10 bold",bg=Recursos.COLOR_FONDO,anchor=W).grid(padx=(20,0),row=20,column=4,columnspan=2,sticky=E)
        textoFeed = StringVar()
        textoFeed.set(Recursos.delayScanner)
        feed = Label(frameMedio, textvariable=textoFeed,font=(Recursos.FUENTE_PRINCIPAL, 10),bg=Recursos.COLOR_FONDO,anchor=W)
        feed.grid(row=20,column=6,sticky=W,padx=5)
        botonCambiarFeed = Recursos.botonMicro(frameMedio,"Cambiar",lambda: self.cambiarValorConfiguracion(frameMedio,textoFeed,botonCambiarFeed,20,6,valoresFeed,'Impresora', 'feed'))
        botonCambiarFeed.grid(row=20,column=7,sticky=W)




        #-------------FRAME INFERIOR------------
        #Boton Recepciones            
        botonGuardar = Recursos.botonPrincipal(self.frameInferior,'Reiniciar',self.reiniciar)
        botonGuardar.pack(side=LEFT, anchor=SW)

        #Boton Configuración       
        botonFinalizar = Recursos.botonPrincipal(self.frameInferior,'Finalizar',self.pantallaInicial)
        botonFinalizar.pack(side=RIGHT, anchor=SE)

    def cambiarValorConfiguracion(self,contenedor, textoVariable,botonCambiar,fila,columna,valores,grupo,item):
        lista = Combobox(contenedor,values=valores,state='readonly',width=10)
        lista.current(0)
        lista.grid(row=fila,column=columna,sticky=W)
        botonCambiar.grid_remove()
        botonGuardar = Recursos.botonMicro(contenedor,"Guardar",lambda: self.guardarCambios(botonGuardar,botonCambiar,textoVariable,lista,grupo,item))
        botonGuardar.grid(row=fila,column=columna+1,sticky=W)

    def guardarCambios(self,botonGuardar,botonCambiar,textoVariable,lista,grupo,item):
        botonCambiar.grid()
        botonGuardar.destroy()
        dato = str(lista.get())
        lista.destroy()
        textoVariable.set(dato)
        Recursos.modificarConfig(grupo,item,dato)
   
    def limpiarFrame(self):
        self.encabezado.set("")
        self.subtitulo.set("")

        for widgets in self.contenedor.winfo_children():
            widgets.destroy()
        for widgets in self.frameInferior.winfo_children():
            widgets.destroy()

    def validarTransportista(self,entradaQR):
        nroTransportista = entradaQR.get()
        entradaQR.delete(0, 'end')
        tuplaResultadoQuery = BaseDatos.encontrarTransportista(nroTransportista)
        if (tuplaResultadoQuery == None):
            messagebox.showinfo(message="El transportista "+nroTransportista+" no existe", title="Transportista no encontrado")
        else:
            transportista = list(tuplaResultadoQuery)
            self.limpiarFrame()
            #--Frame Inferior--
            botonFinalizar = Recursos.botonPrincipal(self.frameInferior,'Iniciar Recepción',lambda: self.pantallaCargaRecepcion(Recepcion.Recepcion(transportista)))        
            botonFinalizar.pack(anchor=SE)

            #--Frame Medio--
            Label(self.contenedor, text=transportista[1]+" - "+transportista[4],font=(Recursos.FUENTE_PRINCIPAL, 20),bg=Recursos.COLOR_FONDO).pack(anchor=CENTER,side=TOP,pady=(180,20))
            frameRadio = Frame(self.contenedor,background=Recursos.COLOR_FONDO)
            frameRadio.pack(anchor=CENTER,side=TOP)
            Label(frameRadio, text="Radio",font=(Recursos.FUENTE_PRINCIPAL, 13),bg=Recursos.COLOR_FONDO).grid(column=0,row=0,padx=3)
            textoCodRadio = StringVar()
            textoCodRadio.set(transportista[2]+": "+transportista[3])
            radioElegido = Label(frameRadio, textvariable=textoCodRadio,font=(Recursos.FUENTE_PRINCIPAL, 13),bg=Recursos.COLOR_FONDO)
            radioElegido.grid(column=1,row=0)
            botonCambiar = Recursos.botonMicro(frameRadio,"Cambiar",lambda: self.cambiarValorRadio(frameRadio,radioElegido,textoCodRadio,botonCambiar,transportista))
            botonCambiar.grid(row=0,column=2,sticky=W,padx=10)

    def cambiarValorRadio(self,contenedor, radioElegido,textoVariable,botonCambiar,transportista):
        radios = BaseDatos.obtenerRadios()
        valores = [valores[0]+" - "+valores[1] for valores in radios]
        radioElegido.grid_remove()
        lista = Combobox(contenedor,values=valores,state='readonly',width=40)
        lista.current(0)
        lista.grid(row=0,column=1,sticky=W)
        botonCambiar.grid_remove()
        botonGuardar = Recursos.botonMicro(contenedor,"Guardar",lambda: self.guardarCambiosRadio(botonGuardar,botonCambiar,radioElegido,textoVariable,lista,radios,transportista))
        botonGuardar.grid(row=0,column=2,sticky=W,padx=10)    
        
    def guardarCambiosRadio(self,botonGuardar,botonCambiar,radioElegido,textoVariable,lista,radios,transportista):
        radioElegido.grid()
        botonCambiar.grid()
        botonGuardar.destroy()
        dato = str(lista.get())
        transportista[2] = radios[lista.current()][0]
        transportista[3] = radios[lista.current()][1]
        lista.destroy()
        textoVariable.set(dato)

    def nuevoFarmaboxChico(self,nroFB,cantidad):
        cantidadModificada = cantidad -1
        tanda = (cantidadModificada // (Recursos.FILAS_MAX * Recursos.COLUMNA_MAX))
        columna = ((cantidadModificada % (Recursos.FILAS_MAX * Recursos.COLUMNA_MAX )) // Recursos.FILAS_MAX)*2
        fila = (cantidadModificada % Recursos.FILAS_MAX) + tanda * Recursos.FILAS_MAX
        Label(self.frameScrollChicos,text=str(cantidad),font="Verdana 10 bold",bg=Recursos.COLOR_NARANJA_MUY_SUAVE).grid(row=fila,column=columna,sticky=W,padx=(10,3))
        Label(self.frameScrollChicos, text=str(nroFB),font=(Recursos.FUENTE_PRINCIPAL, 10),bg=Recursos.COLOR_NARANJA_MUY_SUAVE).grid(row=fila,column=columna+1,sticky=W,padx=(2,10))
        self.marcadorCH.set(str(cantidad))

    def nuevoFarmaboxGrande(self,nroFB,cantidad):
        cantidadModificada = cantidad -1
        tanda = (cantidadModificada // (Recursos.FILAS_MAX * Recursos.COLUMNA_MAX))
        columna = ((cantidadModificada % (Recursos.FILAS_MAX * Recursos.COLUMNA_MAX )) // Recursos.FILAS_MAX)*2
        fila = (cantidadModificada % Recursos.FILAS_MAX) + tanda * Recursos.FILAS_MAX
        Label(self.frameScrollGrandes,text=str(cantidad),font="Verdana 10 bold",bg=Recursos.COLOR_MORADO_MUY_SUAVE).grid(row=fila,column=columna,sticky=W,padx=(10,3))
        Label(self.frameScrollGrandes, text=str(nroFB),font=(Recursos.FUENTE_PRINCIPAL, 10),bg=Recursos.COLOR_MORADO_MUY_SUAVE).grid(row=fila,column=columna+1,sticky=W,padx=(2,10))
        self.marcadorGR.set(str(cantidad))

    def nuevoRechazado(self):
        self.marcadorRechazados.set(str(self.recepcion.rechazados))

    def enterPricipal(self,event,entradaQR):
        self.validarTransportista(entradaQR)
    
    def recibirDatos(self,dato1,dato2):
        if self.pantalla == 1:
            self.validarTransportista(dato1)
        elif self.pantalla == 2:
            self.recepcion.agregarFarmabox(self,dato1,dato2)

    def lanzarVentanaTapas(self):
        ancho = 460
        alto = 170
        VentanaTapas(self,ancho,alto,"Ingreso Tapas")

    def lanzarVentanaFarmabox(self):
        ancho = 460
        alto = 300
        VentanaFarmabox(self,ancho,alto,"Carga Manul de Farmabox")

    def lanzarVentanaCancelaRecepcion(self):
        ancho = 445
        alto = 180
        VentanaCancelaRecepcion(self,ancho,alto,"Confirmar Cancelación de Recepción")

    def lanzarVentanaFinalizarCarga(self):
        ancho = 460
        alto = 245
        VentanaFinalizarRecepcion(self,ancho,alto,"Finalizar Carga")

    def reiniciar(self):
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

class VentanaTapas(Recursos.VentanaHija):
    def __init__(self,ventanaMadre,ancho,alto,titulo):
        Recursos.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)

        #Texto
        Label(self.contenedor, text = "Cantidad de tapas:",font=(Recursos.FUENTE_PRINCIPAL, 15),bg='white').grid(row=1,column=0,pady=37,padx=10,sticky=E)

        #Entrada de Texto
        self.entradaTapas = Entry(self.contenedor, font=(Recursos.FUENTE_PRINCIPAL,15), width=15,highlightthickness=2)
        self.entradaTapas.focus_set()
        self.entradaTapas.grid(row=1,column=1,sticky=W)
        
        #Botones
        botonCancelar = Recursos.botonSecundario(self.contenedor,'Cancelar',self.ventana.destroy)
        botonCancelar.grid(row=2,column=0,sticky=EW,padx=5)
        botonFinalizar =  Recursos.botonPrincipal(self.contenedor,'Cargar Tapas',lambda: self.cargarTapas(self))
        botonFinalizar.grid(row=2,column=1,sticky=EW,padx=5)
        
        self.ventana.bind('<Return>', lambda event: self.cargarTapas(self))

    def cargarTapas(self,event):
        self.ventanaMadre.recepcion.agregarTapas(self.entradaTapas.get())
        self.ventanaMadre.marcadorTapas.set(self.ventanaMadre.recepcion.tapas)
        self.ventana.destroy()

class VentanaFarmabox(Recursos.VentanaHija):
    def __init__(self,ventanaMadre,ancho,alto,titulo):
        Recursos.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)
        
        self.listaFarmabox = []

        #Creo Frames
        altoFrameSuperior = alto - ventanaMadre.altoFrameInferior - self.altoLinea
        frameSuperior = Frame(self.contenedor ,height=altoFrameSuperior,width=ancho, background=Recursos.COLOR_FONDO)
        frameSuperior.pack(fill=BOTH, expand=True)
        self.frameInferior = Frame(self.contenedor ,height=ventanaMadre.altoFrameInferior,width=ancho,background=Recursos.COLOR_FONDO)
        self.frameInferior.pack(fill=BOTH)

        #---Frame Superior---
        # Creo Canvas dentro de Frame
        canvas = Canvas(frameSuperior, bg=Recursos.COLOR_FONDO,borderwidth=0,highlightthickness=0,width=ancho-50,height=altoFrameSuperior)
        canvas.pack(side=LEFT,fill=Y,expand=TRUE)

        #Creo Frame dentro de Canvas
        self.frameScroll = Frame(canvas,background=Recursos.COLOR_FONDO)

        #Armo Scroll y Linkeo
        scroll = Scrollbar(frameSuperior,orient=VERTICAL, command=canvas.yview)
        scroll.pack(side=RIGHT,fill=Y)
        canvas.configure(yscrollcommand=scroll.set)
        canvas.create_window((1,1), window=self.frameScroll, anchor=NW, tags="self.frameScroll")

        #Refresh en cada agregado de celda
        self.frameScroll.bind("<Configure>", lambda event: canvas.config(scrollregion=canvas.bbox("all")))
        self.fila = 0

        Recursos.igualarColumnas(self.frameScroll,3)
        self.agregarLineaCargaManualFB()
               
        #---Frame Inferior---
        Recursos.igualarColumnas(self.frameInferior,2)

        #Botones
        botonCancelar = Recursos.botonSecundario(self.frameInferior,'Cancelar',lambda: self.ventana.destroy())
        botonCancelar.grid(row=0,column=0,sticky='sew',padx=5,pady=10)
        botonFinalizar =  Recursos.botonPrincipal(self.frameInferior,'Agregar Farmabox', lambda: self.finalizarCarga())
        botonFinalizar.grid(row=0,column=1,sticky='sew',padx=5,pady=10)

    def agregarLineaCargaManualFB(self):
        
        entradaFB = Entry(self.frameScroll, font=(Recursos.FUENTE_PRINCIPAL,12), width=11,highlightthickness=2)
        entradaFB.focus_set()
        entradaFB.grid(row=self.fila,column=0,sticky=W,padx=10,pady=5)

        entradaFBControl = Entry(self.frameScroll, font=(Recursos.FUENTE_PRINCIPAL,12), width=11,highlightthickness=2)
        entradaFBControl.grid(row=self.fila,column=1,sticky=W,padx=10,pady=5)

        boton = Recursos.botonMicro(self.frameScroll,"Validar",lambda: self.compararFarmaboxManual(self,entradaFB, entradaFBControl,boton))
        boton.grid(row=self.fila,column=2,sticky=E,padx=10,pady=5)

        #Activo el enter
        self.ventana.bind('<Return>', lambda event : self.compararFarmaboxManual(self,entradaFB, entradaFBControl,boton))

    def compararFarmaboxManual(self,event,entrada1,entrada2,boton):
        dato1 = entrada1.get()
        dato2 = entrada2.get()

        if(dato1==dato2):
            self.listaFarmabox.append(dato1)
            entrada1.destroy()
            entrada2.destroy()
            boton.destroy()
            Label(self.frameScroll, text=str(self.fila + 1)+". "+str(dato1),font=(Recursos.FUENTE_PRINCIPAL, 12),bg=Recursos.COLOR_FONDO).grid(row=self.fila,column=0,sticky=W,padx=15)
            self.fila += 1
            self.agregarLineaCargaManualFB()


    def finalizarCarga(self):
        for cubeta in self.listaFarmabox:
            self.ventanaMadre.recepcion.agregarFarmabox(self.ventanaMadre,cubeta,cubeta)
        self.ventana.destroy()

class VentanaCancelaRecepcion(Recursos.VentanaHija):
    def __init__(self,ventanaMadre,ancho,alto,titulo):
        Recursos.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)
        
        #Texto
        Label(self.contenedor, text='¿ Está seguro que quiere cancelar esta recepción ?',font=(Recursos.FUENTE_PRINCIPAL, 12),bg=Recursos.COLOR_FONDO,anchor=CENTER).grid(row=0,column=0,columnspan=2,pady=40,padx=10,sticky=EW)
        #Botones
        botonVolver = Recursos.botonSecundario(self.contenedor,'Seguir Recepcionando',self.ventana.destroy)
        botonVolver.grid(row=1,column=0,sticky='sew',padx=(10,5),pady=10)
        botonCancelar =  Recursos.botonPrincipal(self.contenedor,'Cancelar Recepción',self.cancelar)
        botonCancelar.grid(row=1,column=1,sticky='sew',padx=(5,10),pady=10)

    def cancelar(self):
        self.ventanaMadre.pantallaInicial()
        self.ventana.destroy()

class VentanaFinalizarRecepcion(Recursos.VentanaHija):
    def __init__(self,ventanaMadre,ancho,alto,titulo):
        Recursos.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)

        Recursos.igualarColumnas(self.contenedor,2)


        #Texto Fijo
        Label(self.contenedor, text = "Está por generar la siguiente Recepción:",font=('Helvetica 15 underline'),bg='white').grid(row=1,column=0,columnspan=2,sticky=EW,pady=(10,20))
        Label(self.contenedor, text = "Transportista: ",font=(Recursos.FUENTE_PRINCIPAL, 12),bg='white').grid(row=2,column=0,sticky=E)
        Label(self.contenedor, text = "Farmabox Chicos: ",font=(Recursos.FUENTE_PRINCIPAL, 12),bg='white').grid(row=3,column=0,sticky=E)
        Label(self.contenedor, text = "Farmabox Grandes: ",font=(Recursos.FUENTE_PRINCIPAL, 12),bg='white').grid(row=4,column=0,sticky=E)
        Label(self.contenedor, text = "Tapas: ",font=(Recursos.FUENTE_PRINCIPAL, 12),bg='white').grid(row=5,column=0,sticky=E)

        #Texto Dinámico
        Label(self.contenedor, text=self.ventanaMadre.recepcion.transportista[1],font=(Recursos.FUENTE_PRINCIPAL, 12),background='white').grid(row=2,column=1,sticky=W,padx=10)
        Label(self.contenedor, text=self.ventanaMadre.recepcion.cantidadChicos(),font=(Recursos.FUENTE_PRINCIPAL, 12),bg='white').grid(row=3,column=1,sticky=W,padx=10)
        Label(self.contenedor, text=self.ventanaMadre.recepcion.cantidadGrandes(),font=(Recursos.FUENTE_PRINCIPAL, 12),bg='white').grid(row=4,column=1,sticky=W,padx=10)
        Label(self.contenedor, text=self.ventanaMadre.recepcion.tapas,font=(Recursos.FUENTE_PRINCIPAL, 12),bg='white').grid(row=5,column=1,sticky=W,padx=10)

        #Botones
        botonCancelar = Recursos.botonSecundario(self.contenedor,'Seguir Recepcionando',self.ventana.destroy)
        botonCancelar.grid(row=6,column=0,sticky=EW,pady=(25,0),padx=5)
        botonFinalizar = Recursos.botonPrincipal(self.contenedor,'Generar Recepción',self.finalizarCargaRecepcion)
        botonFinalizar.grid(row=6,column=1,sticky=EW,pady=(25,0),padx=5)
        
    def finalizarCargaRecepcion(self):
        BaseDatos.generarRecepcion(self.ventanaMadre.recepcion)
        Recursos.imprimirTicket(self.ventanaMadre.recepcion)
        self.ventanaMadre.pantallaInicial()
        self.ventana.destroy()

class PantallaRecepciones():
    def __init__(self,ventana):
        ventana.pantalla = 3

        #Limpio pantalla de widgets anteriores
        ventana.limpiarFrame()
        
        #-------------FRAME SUPERIOR------------
        #Titulo
        ventana.encabezado.set("Buscar Recepciones")


        #-------------FRAME INFERIORR------------
        #Boton Finalizar
        botonFinalizar = Recursos.botonPrincipal(ventana.frameInferior,'Finalizar',ventana.pantallaInicial)         
        botonFinalizar.pack(anchor=SE)
    