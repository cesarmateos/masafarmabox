from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkinter.ttk import Treeview
from tkinter.ttk import Style
from tkcalendar import Calendar
import BaseDatos
import Recursos
import Recepcion
import Widgets
import os
import sys


class Ventana(Tk):

    def __init__(self, *args, **kwargs):

        Tk.__init__(self, *args, **kwargs)
        
        #Color del fondo
        self.fondo = Widget
        self.configure(bg=Widgets.COLOR_FONDO)

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
        self.title(Widgets.TITULO)
        rutaIcono = Recursos.rutaArchivo('Imagenes/Pantuflas.ico')
        self.iconbitmap(rutaIcono)

        altoVentana = self.altoFrameInferior + self.altoFrameMedio + self.altoFrameSuperior
        self.geometry(str(self.anchoVentana)+"x"+str(altoVentana)+"+"+margenPosicional+"+10")
        self.resizable(False, False)

        #---Frame Superior----
        self.frameSuperior = Frame(self,bg=Widgets.COLOR_FONDO,height=self.altoFrameInferior)
        self.frameSuperior.pack(side = TOP, fill = BOTH, expand = TRUE)
        self.frameSuperior.propagate(False)

        #Linea Superior
        Widgets.linea(self.frameSuperior,self.anchoVentana,0,2)
          
        #Encabezado Top Izquierdo
        self.encabezado = StringVar()   
        self.subtitulo = StringVar()   
        Label(self.frameSuperior, textvariable=self.encabezado,font=(Widgets.FUENTE_PRINCIPAL, 16),background=Widgets.COLOR_FONDO).grid(row=0,column=0,sticky=W,pady=(5,0),padx=Widgets.MARGEN_X)
        Label(self.frameSuperior, textvariable=self.subtitulo,font=(Widgets.FUENTE_PRINCIPAL, 9),background=Widgets.COLOR_FONDO).grid(row=1,column=0,sticky=W,padx=Widgets.MARGEN_X)

        #Logo
        imagenLogo = PhotoImage(file=Recursos.rutaArchivo('Imagenes/Logo.png'))
        logo = Label(self.frameSuperior, image=imagenLogo,bg=Widgets.COLOR_FONDO)
        logo.photo = imagenLogo
        logo.grid(row=0,column=1,rowspan=2,sticky=N+S+E,pady=10,padx=Widgets.MARGEN_X)


        #---Frame contenedor de Widgets---
        self.contenedor = Frame(self,bg=Widgets.COLOR_FONDO,height=self.altoFrameMedio) 
        self.contenedor.propagate(False)
        self.contenedor.pack(side = TOP, fill = X, expand = True)

        #---Frame inferior---
        self.frameInferior = Frame(self,bg=Widgets.COLOR_FONDO,height=self.altoFrameInferior) 
        self.frameInferior.pack(side = BOTTOM, fill = BOTH, expand = TRUE,padx=Widgets.MARGEN_X,pady=10)
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
        Label(self.contenedor, text="Escanear código QR o ingresar manualmente",font=(Widgets.FUENTE_PRINCIPAL, 15),bg=Widgets.COLOR_FONDO).place(x=210,y=200)
        
        #Entrada de QR
        entradaQR = Entry(self.contenedor, font=(Widgets.FUENTE_PRINCIPAL,20), width=20,highlightthickness=2)
        entradaQR.focus_set()
        entradaQR.place(x=235,y=250)  

        #Boton Lupa
        botonLupa = Widgets.Btn(self.contenedor, imagenNormal='Lupa.png', imagenHover='LupaHover.png', command=lambda: self.enterPricipal(self, entradaQR))
        botonLupa.place(x=600,y=245) 

        #Activo el enter
        self.bind('<Return>', lambda event : self.enterPricipal(self,entradaQR))


        #-------------FRAME INFERIOR------------
        #Boton Consultas         
        botonConsultas = Widgets.botonPrincipal(self.frameInferior,'Consultas',self.pantallaConsultas)
        #botonRecepciones = Recursos.botonPrincipal(self.frameInferior,'Recepciones',lambda : PantallaRecepciones(self))
        botonConsultas.pack(side=RIGHT, anchor=SE)

        #Boton Configuración       
        botonConfiguración = Widgets.botonPrincipal(self.frameInferior,'Configuración',self.pantallaConfiguracion)
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
        frameTitulos = Frame(contenedorGeneral,height=self.altoFrameTitulos,background=Widgets.COLOR_FONDO)
        frameTitulos.pack(side=TOP,padx=Widgets.MARGEN_X)
        altoFrameNroFarmabox = self.altoFrameMedio - (self.altoFrameTitulos*2)
        frameMedio = Frame(contenedorGeneral,height=altoFrameNroFarmabox,background=Widgets.COLOR_FONDO)
        frameMedio.pack(fill=BOTH,expand=True,padx=Widgets.MARGEN_X,side=TOP)
        frameTotales = Frame(contenedorGeneral,height=self.altoFrameTitulos,background=Widgets.COLOR_FONDO)
        frameTotales.pack(fill=Y,expand=False,padx=Widgets.MARGEN_X,side=BOTTOM)

        
        anchoLinea = self.anchoVentana-Widgets.MARGEN_X*2

        #-------------FRAME TITULOS------------ 
        #Linea1
        Widgets.linea(frameTitulos,anchoLinea,0,2) 
        
        #Títulos
        #Widgets.igualarColumnas(frameTitulos,2)
        Label(frameTitulos, text="Chicos",font=(Widgets.FUENTE_PRINCIPAL, 19),bg=Widgets.COLOR_NARANJA_SUAVE,fg=Widgets.COLOR_NARANJA,anchor=CENTER).grid(row=1,column=0,sticky=EW)
        Label(frameTitulos, text="Grandes",font=(Widgets.FUENTE_PRINCIPAL, 19),bg=Widgets.COLOR_MORADO_SUAVE,fg=Widgets.COLOR_MORADO,anchor=CENTER).grid(row=1,column=1,sticky=EW)

        #Linea2
        Widgets.linea(frameTitulos,anchoLinea,2,2) 
 

        #-------------FRAME MEDIO------------
        anchoFrameCubetas = (self.anchoVentana-Widgets.MARGEN_X*2)/2
        frameChicos = Frame(frameMedio,background=Widgets.COLOR_NARANJA_MUY_SUAVE,height=altoFrameNroFarmabox,width=anchoFrameCubetas)
        frameChicos.pack(fill='both',expand=True,side=LEFT)
        frameChicos.propagate(False)
        frameGrandes = Frame(frameMedio,background=Widgets.COLOR_MORADO_MUY_SUAVE,height=altoFrameNroFarmabox,width=anchoFrameCubetas)
        frameGrandes.propagate(False)
        frameGrandes.pack(fill='both',expand=True,side=RIGHT)
        
     
        # Creo Canvas dentro de Frame
        canvasChicos = Canvas(frameChicos, bg=Widgets.COLOR_NARANJA_MUY_SUAVE,borderwidth=0,highlightthickness=0,width=anchoFrameCubetas-45,height=altoFrameNroFarmabox)
        canvasGrandes = Canvas(frameGrandes, bg=Widgets.COLOR_MORADO_MUY_SUAVE,borderwidth=0,highlightthickness=0,width=anchoFrameCubetas-45,height=altoFrameNroFarmabox)
        canvasChicos.pack(side=LEFT,fill=BOTH,expand=TRUE)
        canvasGrandes.pack(side=LEFT,fill=BOTH,expand=TRUE)

        #Creo Frame dentro de Canvas
        self.frameScrollChicos = Frame(canvasChicos,background=Widgets.COLOR_NARANJA_MUY_SUAVE)
        self.frameScrollGrandes = Frame(canvasGrandes,background=Widgets.COLOR_MORADO_MUY_SUAVE)

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
        
        Widgets.igualarColumnas(self.frameScrollChicos,Widgets.COLUMNA_MAX)
        Widgets.igualarColumnas(self.frameScrollGrandes,Widgets.COLUMNA_MAX)


        #-------------FRAME TOTALES------------
        Widgets.igualarColumnas(frameTotales,8)

        #DeclaroVariables de los marcadores
        self.marcadorCH = StringVar()
        self.marcadorGR = StringVar()
        self.marcadorTapas = StringVar()
        self.marcadorRechazados = StringVar()

        #Linea3
        Widgets.linea(frameTotales,anchoLinea,0,8) 
        
        #Textos
        Label(frameTotales, text="Total Chicos: ",font=(Widgets.FUENTE_PRINCIPAL, 15),bg=Widgets.COLOR_FONDO,fg='#FF9933').grid(row=1,column=0,sticky=E,pady=5)
        Label(frameTotales, text="Total Grandes: ",font=(Widgets.FUENTE_PRINCIPAL, 15),bg=Widgets.COLOR_FONDO,fg='#FF9933').grid(row=1,column=4,sticky=E,pady=5)
        Label(frameTotales, text="Total Tapas: ",font=(Widgets.FUENTE_PRINCIPAL, 15),bg=Widgets.COLOR_FONDO,fg='#FF9933').grid(row=1,column=2,sticky=E,pady=5)
        Label(frameTotales, text="Rechazados: ",font=(Widgets.FUENTE_PRINCIPAL, 15),bg=Widgets.COLOR_FONDO,fg='#FF9933').grid(row=1,column=6,sticky=E,pady=5)

        #Marcadores Dinámicos
        Label(frameTotales, textvariable=self.marcadorCH,font=(Widgets.FUENTE_PRINCIPAL, 15),bg=Widgets.COLOR_FONDO).grid(row=1,column=1,sticky=W,padx=(15,0),pady=5)
        Label(frameTotales, textvariable=self.marcadorGR,font=(Widgets.FUENTE_PRINCIPAL, 15),bg=Widgets.COLOR_FONDO).grid(row=1,column=5,sticky=W,padx=(15,0),pady=5)
        Label(frameTotales, textvariable=self.marcadorTapas,font=(Widgets.FUENTE_PRINCIPAL, 15),bg=Widgets.COLOR_FONDO).grid(row=1,column=3,sticky=W,padx=(15,0),pady=5)
        Label(frameTotales, textvariable=self.marcadorRechazados,font=(Widgets.FUENTE_PRINCIPAL, 15),bg=Widgets.COLOR_FONDO,fg='red').grid(row=1,column=7,sticky=W,padx=(15,0),pady=5)

        #Linkeo Marcadores con Contador
        self.marcadorCH.set(str(self.recepcion.cantidadChicos()))
        self.marcadorGR.set(str(self.recepcion.cantidadGrandes()))
        self.marcadorTapas.set(str(self.recepcion.tapas))
        self.marcadorRechazados.set(str(self.recepcion.rechazados))

        #Linea4
        Widgets.linea(frameTotales,anchoLinea,2,8) 
        
        #-------------FRAME INFERIOR------------
        #Boton Cancelar
        botonCancelar = Widgets.botonSecundario(self.frameInferior,'Cancelar',self.lanzarVentanaCancelaRecepcion)
        botonCancelar.grid(row=3,column=0,columnspan=2,sticky=W)

        #Boton Tapas
        botonTapas = Widgets.botonPrincipal(self.frameInferior,'Ingresar Tapas',self.lanzarVentanaTapas)         
        botonTapas.grid(row=3,column=2,columnspan=2,sticky=EW,padx=13)

        #Boton Farmabox   
        botonFarmabox = Widgets.botonPrincipal(self.frameInferior,'Ingresar Farmabox',self.lanzarVentanaFarmabox)       
        botonFarmabox.grid(row=3,column=4,columnspan=2,sticky=EW,padx=(0,13))

        #Boton Finalizar
        botonFinalizar = Widgets.botonPrincipal(self.frameInferior,'Finalizar',self.lanzarVentanaFinalizarCarga)         
        botonFinalizar.grid(row=3,column=6,columnspan=2,sticky=E)
     
    def pantallaConsultas(self):
        self.pantalla = 3

        #Limpio pantalla de widgets anteriores
        self.limpiarFrame()
        
        #-------------FRAME SUPERIOR------------
        #Titulo
        self.encabezado.set("Consultas")

        #-------------FRAME MEDIO------------
        margenY = 2

        #Divido la pantalla en dos frames
        anchoFrame = (self.anchoVentana/2) - Widgets.MARGEN_X
        frameIzquierdo = Frame(self.contenedor,height=self.altoFrameMedio,width=anchoFrame,background=Widgets.COLOR_FONDO)
        frameIzquierdo.propagate(False)
        frameIzquierdo.pack(fill=BOTH,expand=True,padx=(Widgets.MARGEN_X,0),side=LEFT)
        frameDerecho = Frame(self.contenedor,height=self.altoFrameMedio,width=anchoFrame,background=Widgets.COLOR_FONDO)
        frameDerecho.propagate(False)
        frameDerecho.pack(fill=BOTH,expand=True,side=RIGHT,padx=(0,Widgets.MARGEN_X))
        

        #----Seccion Recepciones----
        seccionRecepciones = Widgets.Seccion(frameIzquierdo," Recepciones",width=anchoFrame,bg=Widgets.COLOR_FONDO)
        seccionRecepciones.grid(row=0,column=0)
        
        
        #Fecha Desde
        Label(seccionRecepciones.contenido, text="Fecha desde",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=0,column=0,sticky=E,pady=margenY,padx=(0,4))
        fechaDesdeRecep = Entry(seccionRecepciones.contenido, font=(Widgets.FUENTE_PRINCIPAL,9), width=10,highlightthickness=2)
        fechaDesdeRecep.grid(row=0,column=1,sticky=E,pady=margenY)
        botonPickFechaDesdeRecepcion = Widgets.botonMicro(seccionRecepciones.contenido,"Elegir",lambda: VentanaCalendario(self,fechaDesdeRecep))
        botonPickFechaDesdeRecepcion.grid(row=0,column=2,sticky=E,pady=margenY,padx=2)   

        #Fecha Hasta
        Label(seccionRecepciones.contenido, text="Fecha hasta",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=1,column=0,sticky=E,padx=(10,4),pady=margenY)
        fechaHastaRecep = Entry(seccionRecepciones.contenido, font=(Widgets.FUENTE_PRINCIPAL,9), width=10,highlightthickness=2)
        fechaHastaRecep.grid(row=1,column=1,sticky=E,pady=margenY)
        botonPickFechaHastaRecepcion = Widgets.botonMicro(seccionRecepciones.contenido,"Elegir",lambda: VentanaCalendario(self,fechaHastaRecep))
        botonPickFechaHastaRecepcion.grid(row=1,column=2,sticky=E,pady=margenY,padx=2)  
        
        #Radio
        Label(seccionRecepciones.contenido, text="Radio",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=2,column=0,sticky=E,pady=margenY,padx=(0,4))
        radios = BaseDatos.obtenerRadios()
        radios.append(("00","TODOS LOS RADIOS"))
        valoresRadio = [valores[0]+" - "+valores[1] for valores in radios]
        listaRadio = Combobox(seccionRecepciones.contenido,values=valoresRadio,state='readonly',width=40)
        listaRadio.current(len(valoresRadio)-1)
        listaRadio.grid(row=2,column=1,sticky=W,columnspan=3,pady=margenY)
        
        #Transportista
        Label(seccionRecepciones.contenido, text="Transportista",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=3,column=0,sticky=E,pady=margenY,padx=(0,4))
        transportistas = BaseDatos.obtenerTransportistas()
        transportistas.append((0,"TODOS LOS TRANSPORTISTAS"))
        valoresTransp = [str(valores[0])+" - "+valores[1] for valores in transportistas]
        listaTransp = Combobox(seccionRecepciones.contenido,values=valoresTransp,state='readonly',width=40)
        listaTransp.current(len(valoresTransp)-1)
        listaTransp.grid(row=3,column=1,sticky=W,columnspan=3,pady=margenY)

        
        #Empresa
        Label(seccionRecepciones.contenido, text="Empresa",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=4,column=0,sticky=E,pady=margenY,padx=(0,4))
        empresas = BaseDatos.obtenerEmpresas()
        empresas.append((0,"TODAS LAS EMPRESAS"))
        valoresEmpresa = [valores[1] for valores in empresas]  
        listaEmpresa = Combobox(seccionRecepciones.contenido,values=valoresEmpresa,state='readonly',width=40)
        listaEmpresa.current(len(valoresEmpresa)-1)
        listaEmpresa.grid(row=4,column=1,sticky=W,columnspan=3,pady=margenY)

        
        #Buscar
        botonBuscarRecepcionA = Widgets.botonMicro(seccionRecepciones.contenido,"Buscar",lambda: VentanaRecepciones(self,self.anchoVentana,600,"Consulta Recepciones",fechaDesdeRecep.get(),fechaHastaRecep.get(),(listaRadio.current(),radios),(listaTransp.current(),transportistas),(listaEmpresa.current(),empresas)))
        botonBuscarRecepcionA.grid(row=5,column=2,sticky=E,pady=(margenY,0))   

        
        #Detalle Recepción
        Label(seccionRecepciones.contenido, text="Recepción Nro",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=6,column=0,sticky=E,pady=(20,margenY),padx=(0,4))
        detalleRecepcion = Entry(seccionRecepciones.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=18,highlightthickness=2)
        detalleRecepcion.grid(row=6,column=1,sticky=W,pady=(20,margenY))
        botonBuscarRecepcionB = Widgets.botonMicro(seccionRecepciones.contenido,"Buscar",lambda: VentanaDetalleRecepcion(self,self.anchoVentana,600,"Detalle de Recepción",detalleRecepcion.get()))
        botonBuscarRecepcionB.grid(row=6,column=2,sticky=E,pady=(20,margenY))   
        

        
        #----Seccion Farmabox----
        seccionFarmabox = Widgets.Seccion(frameIzquierdo," Farmabox (Kardex)",width=anchoFrame,bg=Widgets.COLOR_FONDO)
        seccionFarmabox.grid(row=1,column=0)
        
        #Fecha Desde
        Label(seccionFarmabox.contenido, text="Fecha desde",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=0,column=0,sticky=E,pady=margenY,padx=(0,4))
        fechaDesdeFarma = Entry(seccionFarmabox.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=10,highlightthickness=2)
        fechaDesdeFarma.grid(row=0,column=1,sticky=E,pady=margenY)
        botonPickFechaDesdeFarma = Widgets.botonMicro(seccionFarmabox.contenido,"Elegir",lambda: VentanaCalendario(self,fechaDesdeFarma))
        botonPickFechaDesdeFarma.grid(row=0,column=2,sticky=E,pady=margenY,padx=(4,0)) 

        #Fecha Hasta
        Label(seccionFarmabox.contenido, text="Fecha hasta",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=1,column=0,sticky=E,padx=(10,4),pady=margenY)
        fechaHastaFarma = Entry(seccionFarmabox.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=10,highlightthickness=2)
        fechaHastaFarma.grid(row=1,column=1,sticky=E,pady=margenY)
        botonPickFechaHastaFarma = Widgets.botonMicro(seccionFarmabox.contenido,"Elegir",lambda: VentanaCalendario(self,fechaHastaFarma))
        botonPickFechaHastaFarma.grid(row=1,column=2,sticky=E,pady=margenY,padx=(4,0)) 

        #Número Farmabox
        Label(seccionFarmabox.contenido, text="Nro Farmabox",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=2,column=0,sticky=E,pady=margenY,padx=(20,4))
        nroFarmabox = Entry(seccionFarmabox.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=10,highlightthickness=2)
        nroFarmabox.grid(row=2,column=1,sticky=E,pady=margenY)

        #Buscar Farmabox
        botonBuscarFarmabox = Widgets.botonMicro(seccionFarmabox.contenido,"Buscar",lambda: self.BaseDatos.buscarRecepciones())
        botonBuscarFarmabox.grid(row=3,column=3,sticky=E,pady=(margenY,0),padx=0)  


        
        #--Seccion Rechazados--
        seccionRechazados = Widgets.Seccion(frameDerecho," Rechazados",width=anchoFrame,bg=Widgets.COLOR_FONDO)
        seccionRechazados.grid(row=0,column=0)
        
        #Fecha Desde
        Label(seccionRechazados.contenido, text="Fecha desde",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=0,column=0,sticky=E,pady=margenY,padx=(0,4))
        fechaRechazDesde = Entry(seccionRechazados.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=10,highlightthickness=2)
        fechaRechazDesde.grid(row=0,column=1,sticky=E,pady=margenY)
        botonPickFechaDesdeRechaz = Widgets.botonMicro(seccionRechazados.contenido,"Elegir",lambda: VentanaCalendario(self,fechaRechazDesde))
        botonPickFechaDesdeRechaz.grid(row=0,column=2,sticky=E,pady=margenY,padx=(10,0))


        #Fecha Hasta
        Label(seccionRechazados.contenido, text="Fecha hasta",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=1,column=0,sticky=E,padx=(10,4),pady=margenY)
        fechaRechazHasta = Entry(seccionRechazados.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=10,highlightthickness=2)
        fechaRechazHasta.grid(row=1,column=1,sticky=E,pady=margenY)
        botonPickFechaHastaRechaz = Widgets.botonMicro(seccionRechazados.contenido,"Elegir",lambda: VentanaCalendario(self,fechaRechazHasta))
        botonPickFechaHastaRechaz.grid(row=1,column=2,sticky=E,pady=margenY,padx=(10,0))
        
        #Motivo
        Label(seccionRechazados.contenido, text="Motivo",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=2,column=0,sticky=E,pady=margenY,padx=(5,4))
        motivosRechazo = BaseDatos.obtenerMotivosRechazo()
        valoresMotivoRechazo = [valores[1] for valores in motivosRechazo]
        valoresMotivoRechazo.append("TODOS")
        lista = Combobox(seccionRechazados.contenido,values=valoresMotivoRechazo,state='readonly',width=40)
        lista.current(len(valoresMotivoRechazo)-1)
        lista.grid(row=2,column=1,columnspan=3,sticky=W,pady=margenY)

        #Buscar
        botonBuscarRechazo = Widgets.botonMicro(seccionRechazados.contenido,"Buscar",lambda: self.BaseDatos.buscarRecepciones())
        botonBuscarRechazo.grid(row=3,column=3,columnspan=3,sticky=E,pady=(margenY,0))  

        
        #--Seccion Movimientos--
        seccionMovimientos = Widgets.Seccion(frameDerecho," Modificaciones Farmabox",width=anchoFrame,bg=Widgets.COLOR_FONDO)
        seccionMovimientos.grid(row=3,column=0)
        
        #Fecha Desde
        Label(seccionMovimientos.contenido, text="Fecha desde",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=0,column=0,sticky=E,pady=margenY,padx=(0,4))
        fechaModDesde = Entry(seccionMovimientos.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=10,highlightthickness=2)
        fechaModDesde.grid(row=0,column=1,sticky=E,pady=margenY)
        botonPickFechaDesdeMod = Widgets.botonMicro(seccionMovimientos.contenido,"Elegir",lambda: VentanaCalendario(self,fechaModDesde))
        botonPickFechaDesdeMod.grid(row=0,column=2,sticky=E,pady=margenY,padx=(10,0))


        #Fecha Hasta
        Label(seccionMovimientos.contenido, text="Fecha hasta",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=1,column=0,sticky=E,padx=(10,4),pady=margenY)
        fechaModHasta = Entry(seccionMovimientos.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=10,highlightthickness=2)
        fechaModHasta.grid(row=1,column=1,sticky=E,pady=margenY)
        botonPickFechaHastaMod = Widgets.botonMicro(seccionMovimientos.contenido,"Elegir",lambda: VentanaCalendario(self,fechaModHasta))
        botonPickFechaHastaMod.grid(row=1,column=2,sticky=E,pady=margenY,padx=(10,0))
        
        Label(seccionMovimientos.contenido, text="Modificación",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=2,column=0,sticky=E,pady=margenY,padx=(0,4))
        tiposModificacion = BaseDatos.obtenerTiposModificacion()
        valoresTipoMod = [valores[1] for valores in tiposModificacion]
        valoresTipoMod.append("TODOS")
        lista = Combobox(seccionMovimientos.contenido,values=valoresTipoMod,state='readonly',width=40)
        lista.current(len(valoresTipoMod)-1)
        lista.grid(row=2,column=1,sticky=W,columnspan=3,pady=margenY)

        botonBuscarMovA = Widgets.botonMicro(seccionMovimientos.contenido,"Buscar",lambda: self.BaseDatos.buscarRecepciones())
        botonBuscarMovA.grid(row=3,column=3,sticky=E,pady=(margenY,0))   

        
        Label(seccionMovimientos.contenido, text="Modificación Nro",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=4,column=0,sticky=E,pady=(20,0),padx=(0,4))
        detalleMovimiento = Entry(seccionMovimientos.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=18,highlightthickness=2)
        detalleMovimiento.grid(row=4,column=1,columnspan=3,sticky=W,pady=(20,0))
        botonBuscarMovB = Widgets.botonMicro(seccionMovimientos.contenido,"Buscar",lambda: self.BaseDatos.buscarRecepciones())
        botonBuscarMovB.grid(row=4,column=3,sticky=E,pady=(20,0)) 
        


        #-------------FRAME INFERIORR------------
        #Boton Finalizar
        botonFinalizar = Widgets.botonPrincipal(self.frameInferior,'Volver',self.pantallaInicial)         
        botonFinalizar.pack(anchor=SE)

    def pantallaConfiguracion(self):
        self.pantalla = 4

        #Limpio pantalla de widgets anteriores
        self.limpiarFrame()

        

        #-------------FRAME SUPERIOR------------
        #Titulo
        self.encabezado.set("Configuración")
        self.subtitulo.set("Reiniciar luego de efectuar los cambios")



        #-------------FRAME MEDIO------------
    
        #Armo un Frame con márgenes
        anchoFrame = self.anchoVentana-Widgets.MARGEN_X*2 
        frameMedio = Frame(self.contenedor,height=self.altoFrameMedio,width=anchoFrame,background=Widgets.COLOR_FONDO)
        frameMedio.pack(fill=BOTH,expand=True,padx=Widgets.MARGEN_X,side=TOP)


        #Valores Puertos COM
        valoresCOM = []
        for i in range (1,21):
            valoresCOM.append("COM"+str(i))

        #Valores Puertos Baud Rates
        valoresBaudios = [1200,1800,2400,4800,7200,9600,14400,19200,38400,57600,115200,128000]


        #--Seccion Scanner 1--
        seccionScannner1 = Widgets.Seccion(frameMedio," Scanner 1",width=self.anchoVentana,bg=Widgets.COLOR_FONDO)
        seccionScannner1.grid(row=0,column=0)

        #Puerto Scanner 1
        Label(seccionScannner1.contenido, text="Puerto :",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=0,column=0,sticky=E)
        textoPuertoScanner1Variable = StringVar()
        textoPuertoScanner1Variable.set(Recursos.puertoScanner1)
        puertoScanner1 = Label(seccionScannner1.contenido, textvariable=textoPuertoScanner1Variable,font=(Widgets.FUENTE_PRINCIPAL, 10),bg=Widgets.COLOR_FONDO,anchor=W)
        puertoScanner1.grid(row=0,column=1,sticky=W,padx=(5,47))
        botonCambiarSerial1 = Widgets.botonMicro(seccionScannner1.contenido,"Cambiar",lambda: self.cambiarValorConfiguracion(seccionScannner1.contenido,textoPuertoScanner1Variable,botonCambiarSerial1,0,1,valoresCOM,'Scanner1', 'PUERTO'))
        botonCambiarSerial1.grid(row=0,column=2,sticky=W)

        #Baudrate Scanner 1
        Label(seccionScannner1.contenido, text="Baud Rate (bits por seg):",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=(30,0),row=0,column=3,sticky=E)
        textoBaud1 = StringVar()
        textoBaud1.set(Recursos.baudScanner2)
        baudScanner1 = Label(seccionScannner1.contenido, textvariable=textoBaud1,font=(Widgets.FUENTE_PRINCIPAL, 10),bg=Widgets.COLOR_FONDO,anchor=W)
        baudScanner1.grid(row=0,column=4,sticky=W,padx=(5,47))
        botonCambiarBaud1 = Widgets.botonMicro(seccionScannner1.contenido,"Cambiar",lambda: self.cambiarValorConfiguracion(seccionScannner1.contenido,textoBaud1,botonCambiarBaud1,0,4,valoresBaudios,'Scanner1', 'BAUD'))
        botonCambiarBaud1.grid(row=0,column=5,sticky=W)

        #--Seccion Scanner 2--
        seccionScannner2 = Widgets.Seccion(frameMedio," Scanner 2",width=self.anchoVentana,bg=Widgets.COLOR_FONDO)
        seccionScannner2.grid(row=1,column=0)

        #Puerto Scanner 2
        Label(seccionScannner2.contenido, text="Puerto :",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=0,column=0,sticky=E)
        textoPuertoScanner2Variable = StringVar()
        textoPuertoScanner2Variable.set(Recursos.puertoScanner2)
        puertoScanner2 = Label(seccionScannner2.contenido, textvariable=textoPuertoScanner2Variable,font=(Widgets.FUENTE_PRINCIPAL, 10),bg=Widgets.COLOR_FONDO,anchor=W)
        puertoScanner2.grid(row=0,column=1,sticky=W,padx=(5,47))
        botonCambiarSerial2 = Widgets.botonMicro(seccionScannner2.contenido,"Cambiar",lambda: self.cambiarValorConfiguracion(seccionScannner2.contenido,textoPuertoScanner2Variable,botonCambiarSerial2,0,1,valoresCOM,'Scanner2', 'PUERTO'))
        botonCambiarSerial2.grid(row=0,column=2,sticky=W)

        #Baudrate Scanner 2
        Label(seccionScannner2.contenido, text="Baud Rate (bits por seg):",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=(30,0),row=0,column=3,sticky=E)
        textoBaud2 = StringVar()
        textoBaud2.set(Recursos.baudScanner2)
        baudScanner2 = Label(seccionScannner2.contenido, textvariable=textoBaud2,font=(Widgets.FUENTE_PRINCIPAL, 10),bg=Widgets.COLOR_FONDO,anchor=W)
        baudScanner2.grid(row=0,column=4,sticky=W,padx=(5,47))
        botonCambiarBaud2 = Widgets.botonMicro(seccionScannner2.contenido,"Cambiar",lambda: self.cambiarValorConfiguracion(seccionScannner2.contenido,textoBaud2,botonCambiarBaud2,0,4,valoresBaudios,'Scanner2', 'BAUD'))
        botonCambiarBaud2.grid(row=0,column=5,sticky=W)

        #--Seccion Sincronizacion--
        seccionSincro = Widgets.Seccion(frameMedio," Sincronización de Scanners",width=self.anchoVentana,bg=Widgets.COLOR_FONDO)
        seccionSincro.grid(row=2,column=0)

        #Tolerancia
        valoresTolerancia = []
        for i in range (1,11):
            valoresTolerancia.append(str(round(i*0.05,2)))

        Label(seccionSincro.contenido, text="Tolerancia (segundos): ",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=(5,0),row=0,column=0,sticky=W)
        textoTolereancia = StringVar()
        textoTolereancia.set(Recursos.delayScanner)
        tolerancia = Label(seccionSincro.contenido, textvariable=textoTolereancia,font=(Widgets.FUENTE_PRINCIPAL, 10),bg=Widgets.COLOR_FONDO,anchor=W)
        tolerancia.grid(row=0,column=1,sticky=W,padx=(5,55))
        botonCambiarTolerancia = Widgets.botonMicro(seccionSincro.contenido,"Cambiar",lambda: self.cambiarValorConfiguracion(seccionSincro.contenido,textoTolereancia,botonCambiarTolerancia,0,1,valoresTolerancia,'Sincronizacion', 'tolerancia'))
        botonCambiarTolerancia.grid(row=0,column=2,sticky=W)


        #--Seccion Base--
        seccionBase = Widgets.Seccion(frameMedio," Base",width=self.anchoVentana,bg=Widgets.COLOR_FONDO)
        seccionBase.grid(row=3,column=0)


        #--Seccion Impresora--
        seccionImpresora = Widgets.Seccion(frameMedio," Impresora",width=self.anchoVentana,bg=Widgets.COLOR_FONDO)
        seccionImpresora.grid(row=4,column=0)

        #Backfeed
        valoresFeed = []
        for i in range (1,50):
            valoresFeed.append(str(i*10))

        Label(seccionImpresora.contenido, text="Retroseso Etiqueta Previo: ",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=(5,0),row=0,column=0,sticky=W)
        textoBackFeed = StringVar()
        textoBackFeed.set(Recursos.backfeed)
        backFeed = Label(seccionImpresora.contenido, textvariable=textoBackFeed,font=(Widgets.FUENTE_PRINCIPAL, 10),bg=Widgets.COLOR_FONDO,anchor=W)
        backFeed.grid(row=0,column=1,sticky=W,padx=(5,52))
        botonCambiarBackFeed = Widgets.botonMicro(seccionImpresora.contenido,"Cambiar",lambda: self.cambiarValorConfiguracion(seccionImpresora.contenido,textoBackFeed,botonCambiarBackFeed,0,1,valoresFeed,'Impresora', 'backfeed'))
        botonCambiarBackFeed.grid(row=0,column=2,sticky=W)
        
        Label(seccionImpresora.contenido, text="Alimento Etiqueta Posterior: ",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=(30,0),row=0,column=3,sticky=W)
        textoFeed = StringVar()
        textoFeed.set(Recursos.feed)
        feed = Label(seccionImpresora.contenido, textvariable=textoFeed,font=(Widgets.FUENTE_PRINCIPAL, 10),bg=Widgets.COLOR_FONDO,anchor=W)
        feed.grid(row=0,column=4,sticky=W,padx=(5,52))
        botonCambiarFeed = Widgets.botonMicro(seccionImpresora.contenido,"Cambiar",lambda: self.cambiarValorConfiguracion(seccionImpresora.contenido,textoFeed,botonCambiarFeed,0,4,valoresFeed,'Impresora', 'feed'))
        botonCambiarFeed.grid(row=0,column=5,sticky=W)



        #-------------FRAME INFERIOR------------
        #Boton Recepciones            
        botonGuardar = Widgets.botonPrincipal(self.frameInferior,'Reiniciar',self.reiniciar)
        botonGuardar.pack(side=LEFT, anchor=SW)

        #Boton Configuración       
        botonFinalizar = Widgets.botonPrincipal(self.frameInferior,'Volver',self.pantallaInicial)
        botonFinalizar.pack(side=RIGHT, anchor=SE)

    def cambiarValorConfiguracion(self,contenedor, textoVariable,botonCambiar,fila,columna,valores,grupo,item):
        lista = Combobox(contenedor,values=valores,state='readonly',width=10)
        lista.current(0)
        lista.grid(row=fila,column=columna,sticky=W)
        botonCambiar.grid_remove()
        botonGuardar = Widgets.botonMicro(contenedor,"Guardar",lambda: self.guardarCambios(botonGuardar,botonCambiar,textoVariable,lista,grupo,item))
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

    def validarTransportista(self,nroTransportista):
        tuplaResultadoQuery = BaseDatos.encontrarTransportista(nroTransportista)
        
        if (tuplaResultadoQuery == None):
            messagebox.showinfo(message="El transportista "+str(nroTransportista)+" no existe", title="Transportista no encontrado")
        else:
            transportista = list(tuplaResultadoQuery)
            self.limpiarFrame()

            #--Frame Inferior--
            botonVolver = Widgets.botonSecundario(self.frameInferior,'Cancelar',lambda: self.pantallaInicial())        
            botonVolver.pack(side=LEFT, anchor=SW)
            botonFinalizar = Widgets.botonPrincipal(self.frameInferior,'Iniciar Recepción',lambda: self.pantallaCargaRecepcion(Recepcion.Recepcion(transportista)))        
            botonFinalizar.pack(side=RIGHT, anchor=SE)

            #--Frame Medio--
            Label(self.contenedor, text=transportista[1]+" - "+transportista[4],font=(Widgets.FUENTE_PRINCIPAL, 20),bg=Widgets.COLOR_FONDO).pack(anchor=CENTER,side=TOP,pady=(180,20))
            frameRadio = Frame(self.contenedor,background=Widgets.COLOR_FONDO)
            frameRadio.pack(anchor=CENTER,side=TOP)
            Label(frameRadio, text="Radio",font=(Widgets.FUENTE_PRINCIPAL, 13),bg=Widgets.COLOR_FONDO).grid(column=0,row=0,padx=3)
            textoCodRadio = StringVar()
            textoCodRadio.set(transportista[2]+": "+transportista[3])
            radioElegido = Label(frameRadio, textvariable=textoCodRadio,font=(Widgets.FUENTE_PRINCIPAL, 13),bg=Widgets.COLOR_FONDO)
            radioElegido.grid(column=1,row=0)
            botonCambiar = Widgets.botonMicro(frameRadio,"Cambiar",lambda: self.cambiarValorRadio(frameRadio,radioElegido,textoCodRadio,botonCambiar,transportista))
            botonCambiar.grid(row=0,column=2,sticky=W,padx=10)

    def cambiarValorRadio(self,contenedor, radioElegido,textoVariable,botonCambiar,transportista):
        radios = BaseDatos.obtenerRadios()
        valores = [valores[0]+" - "+valores[1] for valores in radios]
        radioElegido.grid_remove()
        lista = Combobox(contenedor,values=valores,state='readonly',width=40)
        lista.current(0)
        lista.grid(row=0,column=1,sticky=W)
        botonCambiar.grid_remove()
        botonGuardar = Widgets.botonMicro(contenedor,"Guardar",lambda: self.guardarCambiosRadio(botonGuardar,botonCambiar,radioElegido,textoVariable,lista,radios,transportista))
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
        tanda = (cantidadModificada // (Widgets.FILAS_MAX * Widgets.COLUMNA_MAX))
        columna = ((cantidadModificada % (Widgets.FILAS_MAX * Widgets.COLUMNA_MAX )) // Widgets.FILAS_MAX)*2
        fila = (cantidadModificada % Widgets.FILAS_MAX) + tanda * Widgets.FILAS_MAX
        Label(self.frameScrollChicos,text=str(cantidad),font="Verdana 10 bold",bg=Widgets.COLOR_NARANJA_MUY_SUAVE).grid(row=fila,column=columna,sticky=W,padx=(10,3))
        Label(self.frameScrollChicos, text=str(nroFB),font=(Widgets.FUENTE_PRINCIPAL, 10),bg=Widgets.COLOR_NARANJA_MUY_SUAVE).grid(row=fila,column=columna+1,sticky=W,padx=(2,10))
        self.marcadorCH.set(str(cantidad))

    def nuevoFarmaboxGrande(self,nroFB,cantidad):
        cantidadModificada = cantidad -1
        tanda = (cantidadModificada // (Widgets.FILAS_MAX * Widgets.COLUMNA_MAX))
        columna = ((cantidadModificada % (Widgets.FILAS_MAX * Widgets.COLUMNA_MAX )) // Widgets.FILAS_MAX)*2
        fila = (cantidadModificada % Widgets.FILAS_MAX) + tanda * Widgets.FILAS_MAX
        Label(self.frameScrollGrandes,text=str(cantidad),font="Verdana 10 bold",bg=Widgets.COLOR_MORADO_MUY_SUAVE).grid(row=fila,column=columna,sticky=W,padx=(10,3))
        Label(self.frameScrollGrandes, text=str(nroFB),font=(Widgets.FUENTE_PRINCIPAL, 10),bg=Widgets.COLOR_MORADO_MUY_SUAVE).grid(row=fila,column=columna+1,sticky=W,padx=(2,10))
        self.marcadorGR.set(str(cantidad))

    def nuevoRechazado(self):
        self.marcadorRechazados.set(str(self.recepcion.rechazados))

    def enterPricipal(self,event,entradaQR):
        nroTransportista = entradaQR.get()
        entradaQR.delete(0, 'end')
        self.validarTransportista(nroTransportista)
    
    def recibirDatos(self,dato1,dato2):
        if self.pantalla == 1:
            self.validarTransportista(dato1)
        elif self.pantalla == 2:
            self.recepcion.agregarFarmabox(self,dato1,dato2)

    def lanzarVentanaTapas(self):
        ancho = 450
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
        ancho = 450
        alto = 245
        VentanaFinalizarRecepcion(self,ancho,alto,"Finalizar Carga")

    def reiniciar(self):
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

    def buscarRecepciones(self):
        pass

class VentanaTapas(Widgets.VentanaHija):
    def __init__(self,ventanaMadre,ancho,alto,titulo):
        Widgets.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)

        #Texto
        Label(self.contenedor, text = "Cantidad de tapas:",font=(Widgets.FUENTE_PRINCIPAL, 15),bg='white').grid(row=1,column=0,pady=28,padx=15,sticky=E)

        #Entrada de Texto
        self.entradaTapas = Entry(self.contenedor, font=(Widgets.FUENTE_PRINCIPAL,15), width=15,highlightthickness=2)
        self.entradaTapas.focus_set()
        self.entradaTapas.grid(row=1,column=1,sticky=W)
        
        #Botones
        botonCancelar = Widgets.botonSecundario(self.frameInferior,'Cancelar',self.ventana.destroy)
        botonCancelar.pack(side=LEFT, anchor=SW,pady=10,padx=(10,0))
        botonFinalizar =  Widgets.botonPrincipal(self.frameInferior,'Cargar Tapas',lambda: self.cargarTapas(self))
        botonFinalizar.pack(side=RIGHT, anchor=SE,pady=10,padx=(0,10))
        
        self.ventana.bind('<Return>', lambda event: self.cargarTapas(self))

    def cargarTapas(self,event):
        self.ventanaMadre.recepcion.agregarTapas(self.entradaTapas.get())
        self.ventanaMadre.marcadorTapas.set(self.ventanaMadre.recepcion.tapas)
        self.ventana.destroy()

class VentanaFarmabox(Widgets.VentanaHija):
    def __init__(self,ventanaMadre,ancho,alto,titulo):
        Widgets.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)
        
        self.listaFarmabox = []

        #Creo Frames
        altoFrameSuperior = alto - ventanaMadre.altoFrameInferior - self.altoLinea
        frameSuperior = Frame(self.contenedor ,height=altoFrameSuperior,width=ancho, background=Widgets.COLOR_FONDO)
        frameSuperior.pack(fill=BOTH, expand=True)

        #---Frame Superior---
        # Creo Canvas dentro de Frame
        canvas = Canvas(frameSuperior, bg=Widgets.COLOR_FONDO,borderwidth=0,highlightthickness=0,width=ancho-50,height=altoFrameSuperior)
        canvas.pack(side=LEFT,fill=Y,expand=TRUE)

        #Creo Frame dentro de Canvas
        self.frameScroll = Frame(canvas,background=Widgets.COLOR_FONDO)

        #Armo Scroll y Linkeo
        scroll = Scrollbar(frameSuperior,orient=VERTICAL, command=canvas.yview)
        scroll.pack(side=RIGHT,fill=Y)
        canvas.configure(yscrollcommand=scroll.set)
        canvas.create_window((1,1), window=self.frameScroll, anchor=NW, tags="self.frameScroll")

        #Refresh en cada agregado de celda
        self.frameScroll.bind("<Configure>", lambda event: canvas.config(scrollregion=canvas.bbox("all")))
        self.fila = 0

        Widgets.igualarColumnas(self.frameScroll,3)
        self.agregarLineaCargaManualFB()
               
        #---Frame Inferior---
        Widgets.igualarColumnas(self.frameInferior,2)

        #Botones
        botonCancelar = Widgets.botonSecundario(self.frameInferior,'Cancelar',lambda: self.ventana.destroy())
        botonCancelar.pack(side=LEFT, anchor=SW,pady=10,padx=(10,0))
        botonFinalizar =  Widgets.botonPrincipal(self.frameInferior,'Agregar Farmabox', lambda: self.finalizarCarga())
        botonFinalizar.pack(side=RIGHT, anchor=SE,pady=10,padx=(0,10))

    def agregarLineaCargaManualFB(self):
        
        entradaFB = Entry(self.frameScroll, font=(Widgets.FUENTE_PRINCIPAL,12), width=11,highlightthickness=2)
        entradaFB.focus_set()
        entradaFB.grid(row=self.fila,column=0,sticky=W,padx=10,pady=5)

        entradaFBControl = Entry(self.frameScroll, font=(Widgets.FUENTE_PRINCIPAL,12), width=11,highlightthickness=2)
        entradaFBControl.grid(row=self.fila,column=1,sticky=W,padx=10,pady=5)

        boton = Widgets.botonMicro(self.frameScroll,"Validar",lambda: self.compararFarmaboxManual(self,entradaFB, entradaFBControl,boton))
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
            Label(self.frameScroll, text=str(self.fila + 1)+". "+str(dato1),font=(Widgets.FUENTE_PRINCIPAL, 12),bg=Widgets.COLOR_FONDO).grid(row=self.fila,column=0,sticky=W,padx=15)
            self.fila += 1
            self.agregarLineaCargaManualFB()


    def finalizarCarga(self):
        for cubeta in self.listaFarmabox:
            self.ventanaMadre.recepcion.agregarFarmabox(self.ventanaMadre,cubeta,cubeta)
        self.ventana.destroy()

class VentanaCancelaRecepcion(Widgets.VentanaHija):
    def __init__(self,ventanaMadre,ancho,alto,titulo):
        Widgets.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)
        
        #Texto
        Label(self.contenedor, text='¿ Está seguro que quiere cancelar esta recepción ?',font=(Widgets.FUENTE_PRINCIPAL, 12),bg=Widgets.COLOR_FONDO,anchor=CENTER).grid(row=0,column=0,columnspan=2,pady=40,padx=10,sticky=EW)
        
        #Botones
        botonVolver = Widgets.botonSecundario(self.frameInferior,'Seguir Recepcionando',self.ventana.destroy)
        botonVolver.pack(side=LEFT, anchor=SW,pady=10,padx=(10,0))
        botonCancelar =  Widgets.botonPrincipal(self.frameInferior,'Cancelar Recepción',self.cancelar)
        botonCancelar.pack(side=RIGHT, anchor=SE,pady=10,padx=(0,10))

    def cancelar(self):
        self.ventanaMadre.pantallaInicial()
        self.ventana.destroy()

class VentanaFinalizarRecepcion(Widgets.VentanaHija):
    def __init__(self,ventanaMadre,ancho,alto,titulo):
        Widgets.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)

        Widgets.igualarColumnas(self.contenedor,2)


        #Texto Fijo
        Label(self.contenedor, text = "Está por generar la siguiente Recepción:",font=('Helvetica 15 underline'),bg='white').grid(row=1,column=0,columnspan=2,sticky=EW,pady=(10,20))
        Label(self.contenedor, text = "Transportista: ",font=(Widgets.FUENTE_PRINCIPAL, 12),bg='white').grid(row=2,column=0,sticky=E)
        Label(self.contenedor, text = "Farmabox Chicos: ",font=(Widgets.FUENTE_PRINCIPAL, 12),bg='white').grid(row=3,column=0,sticky=E)
        Label(self.contenedor, text = "Farmabox Grandes: ",font=(Widgets.FUENTE_PRINCIPAL, 12),bg='white').grid(row=4,column=0,sticky=E)
        Label(self.contenedor, text = "Tapas: ",font=(Widgets.FUENTE_PRINCIPAL, 12),bg='white').grid(row=5,column=0,sticky=E)

        #Texto Dinámico
        Label(self.contenedor, text=self.ventanaMadre.recepcion.transportista[1],font=(Widgets.FUENTE_PRINCIPAL, 12),background='white').grid(row=2,column=1,sticky=W,padx=10)
        Label(self.contenedor, text=self.ventanaMadre.recepcion.cantidadChicos(),font=(Widgets.FUENTE_PRINCIPAL, 12),bg='white').grid(row=3,column=1,sticky=W,padx=10)
        Label(self.contenedor, text=self.ventanaMadre.recepcion.cantidadGrandes(),font=(Widgets.FUENTE_PRINCIPAL, 12),bg='white').grid(row=4,column=1,sticky=W,padx=10)
        Label(self.contenedor, text=self.ventanaMadre.recepcion.tapas,font=(Widgets.FUENTE_PRINCIPAL, 12),bg='white').grid(row=5,column=1,sticky=W,padx=10)

        #Botones
        botonCancelar = Widgets.botonSecundario(self.frameInferior,'Seguir Recepcionando',self.ventana.destroy)
        botonCancelar.pack(side=LEFT, anchor=SW,pady=10,padx=(10,0))
        botonFinalizar = Widgets.botonPrincipal(self.frameInferior,'Generar Recepción',self.finalizarCargaRecepcion)
        botonFinalizar.pack(side=RIGHT, anchor=SE,pady=10,padx=(0,10))
        
    def finalizarCargaRecepcion(self):
        BaseDatos.generarRecepcion(self.ventanaMadre.recepcion)
        Recursos.imprimirTicket(self.ventanaMadre.recepcion)
        self.ventanaMadre.pantallaInicial()
        self.ventana.destroy()

class VentanaRecepciones(Widgets.VentanaHija):
    def __init__(self,ventanaMadre,ancho,alto,titulo,fechaD,fechaH,radio,transp,empresa):

        Widgets.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)
        
        codRadio = radio[1][radio[0]][0]
        radioImprimible = "TODOS LOS RADIOS"
        if codRadio != '00':
            radioImprimible = codRadio

        transporteObjetivo = transp[1][transp[0]]
        nroTransp = transporteObjetivo[0]
        nomTransp = transporteObjetivo[1]
        nroTranspImrimible = ''
        if nroTransp != 0:
            nroTranspImrimible = " ("+str(nroTransp)+")"

        empresaObjetivo = empresa[1][empresa[0]]
        nroEmpresa = empresaObjetivo[0]
        nomEmpresa = empresaObjetivo[1]
        nroEmpresaImrimible = ''
        if nroEmpresa != 0:
            nroEmpresaImrimible = " ("+str(nroEmpresa)+")"

        
        recepciones = BaseDatos.buscarRecepciones(fechaD,fechaH,codRadio,nroTransp,nroEmpresa)

        #---Frame TOP---
        altoTop = 64
        frameTop = Frame(self.contenedor,bg=Widgets.COLOR_FONDO,height=altoTop) 
        frameTop.pack(side = TOP, fill = X, expand = TRUE, padx=Widgets.MARGEN_X)
        frameTop.propagate(False)
        frameTopDerecho = Frame(frameTop,bg=Widgets.COLOR_FONDO,height=altoTop,width=(ancho/2)-Widgets.MARGEN_X)
        frameTopDerecho.pack(side = LEFT, fill = BOTH, expand = TRUE)
        frameTopIzquierdo = Frame(frameTop,bg=Widgets.COLOR_FONDO,height=altoTop,width=(ancho/2)-Widgets.MARGEN_X)
        frameTopIzquierdo.pack(side = RIGHT, fill = BOTH, expand = TRUE)

        Label(frameTopDerecho, text="Radio : "+radioImprimible,font=(Widgets.FUENTE_PRINCIPAL, 9),background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)
        Label(frameTopDerecho, text="Transportista : "+nomTransp+nroTranspImrimible,font=(Widgets.FUENTE_PRINCIPAL, 9),background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)
        Label(frameTopDerecho, text="Empresa : "+nomEmpresa+nroEmpresaImrimible,font=(Widgets.FUENTE_PRINCIPAL, 9),background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)

        Label(frameTopIzquierdo, text="Fecha Desde :  "+str(fechaD),background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)
        Label(frameTopIzquierdo, text="Fecha Hasta :  "+str(fechaH),background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)


        #---Frame Tabla---
        frameTabla = Frame(self.contenedor,bg=Widgets.COLOR_FONDO,height=self.altoContenedor-altoTop) 
        frameTabla.pack(side = BOTTOM, fill = BOTH, expand = TRUE, padx=Widgets.MARGEN_X)
        frameTabla.propagate(False)

        estilo = Style()
        estilo.theme_use('clam')
        estilo.configure('Treeview.Heading', background=Widgets.COLOR_NARANJA_SUAVE,relief="groove",justify=CENTER)

        tabla = Treeview(frameTabla, column=("#1", "#2", "#3","#4","#5","#6","#7","#8"), show='headings',height=23,selectmode=BROWSE)
        tabla.pack(side=LEFT)

        tabla.column("#1", anchor=CENTER, width=78)
        tabla.heading("#1", text="Recepción")
        tabla.column("#2", anchor=CENTER, width=140)
        tabla.heading("#2", text="Fecha")
        tabla.column("#3", anchor=CENTER, width=70)
        tabla.heading("#3", text="Radio")
        tabla.column("#4", anchor=CENTER, width=185)
        tabla.heading("#4", text="Transportista")
        tabla.column("#5", anchor=CENTER, width=185)
        tabla.heading("#5", text="Empresa")
        tabla.column("#6", anchor=CENTER, width=60)
        tabla.heading("#6", text="Fbox")
        tabla.column("#7", anchor=CENTER, width=60)
        tabla.heading("#7", text="Tapas")
        tabla.column("#8", anchor=CENTER, width=60)
        tabla.heading("#8", text="Proces.")

        scrollbar = Scrollbar(frameTabla, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        tabla.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=tabla.yview)

        for row in recepciones:
            tabla.insert("", END, values=row)     

        #Botones
        botonCSV = Widgets.botonPrincipal(self.frameInferior,'Generar CSV',self.ventana.destroy)
        botonCSV.pack(side=LEFT, anchor=SW,pady=10,padx=(10,0))
        botonExcel = Widgets.botonPrincipal(self.frameInferior,'Generar Excel',self.ventana.destroy)
        botonExcel.pack(side=LEFT, anchor=CENTER,pady=10,padx=5)
        botonFinalizar = Widgets.botonPrincipal(self.frameInferior,'Cerrar',self.ventana.destroy)
        botonFinalizar.pack(side=RIGHT, anchor=SE,pady=10,padx=(0,10))

class VentanaDetalleRecepcion(Widgets.VentanaHija):
    def __init__(self,ventanaMadre,ancho,alto,titulo,nroRecepcion):

        Widgets.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)
        
        recepciones = BaseDatos.buscarRecepcion(nroRecepcion)

        if recepciones is None:
            codRadio = ''
            nomTransportista = ''
            nomEmpresa = ''
            fecha = ''
            procesado = ''
            textoProcesado = ''

        else:
            codRadio = recepciones[0][2]
            nomTransportista = recepciones[0][3]
            nomEmpresa = recepciones[0][4]
            fecha = recepciones[0][1]
            procesado = recepciones[0][8]
            textoProcesado = "No"

            if procesado==0:
                textoProcesado = "Si"


        altoTop = 64
        altoTotales = 30

        #---Frame TOP---
        frameTop = Frame(self.contenedor,bg=Widgets.COLOR_FONDO,height=altoTop) 
        frameTop.pack(side = TOP, fill = X, expand = TRUE, padx=Widgets.MARGEN_X)
        frameTop.propagate(False)
        frameTopDerecho = Frame(frameTop,bg=Widgets.COLOR_FONDO,height=altoTop,width=(ancho/2)-Widgets.MARGEN_X)
        frameTopDerecho.pack(side = LEFT, fill = BOTH, expand = TRUE)
        frameTopIzquierdo = Frame(frameTop,bg=Widgets.COLOR_FONDO,height=altoTop,width=(ancho/2)-Widgets.MARGEN_X)
        frameTopIzquierdo.pack(side = RIGHT, fill = BOTH, expand = TRUE)

        Label(frameTopDerecho, text="Racepción : "+str(nroRecepcion),font=(Widgets.FUENTE_PRINCIPAL, 9),background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)
        Label(frameTopDerecho, text="Radio : "+codRadio,font=(Widgets.FUENTE_PRINCIPAL, 9),background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)
        Label(frameTopDerecho, text="Transportista : "+nomTransportista+" - "+nomEmpresa,font=(Widgets.FUENTE_PRINCIPAL, 9),background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)

        Label(frameTopIzquierdo, text="Fecha :  "+str(fecha),background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)
        Label(frameTopIzquierdo, text="Fecha Hasta :  "+textoProcesado,background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)


        #---Frame Tabla---
        frameTabla = Frame(self.contenedor,bg=Widgets.COLOR_FONDO,height=self.altoContenedor-altoTop-altoTotales) 
        frameTabla.pack(side = TOP, fill = BOTH, expand = TRUE, padx=Widgets.MARGEN_X)
        frameTabla.propagate(False)

        estilo = Style()
        estilo.theme_use('clam')
        estilo.configure('Treeview.Heading', background=Widgets.COLOR_NARANJA_SUAVE,relief="groove",justify=CENTER)

        tabla = Treeview(frameTabla, column=("#1"), show='headings',height=20,selectmode=BROWSE)
        tabla.pack(side=LEFT)

        tabla.column("#1", anchor=CENTER, width=200)
        tabla.heading("#1", text="Número de Farmabox")

        scrollbar = Scrollbar(frameTabla, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        tabla.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=tabla.yview)

        if recepciones is not None:
            for row in recepciones:
                tabla.insert("", END, values=row[7])     

        #---Frame Totales---
        frameTotales = Frame(self.contenedor,bg=Widgets.COLOR_FONDO,height=altoTotales) 
        frameTotales.pack(side = BOTTOM, fill = BOTH, expand = TRUE, padx=Widgets.MARGEN_X)
        frameTotales.propagate(False)

        #Textos
        Label(frameTotales, text="Total Chicos: ",font=(Widgets.FUENTE_PRINCIPAL, 12),bg=Widgets.COLOR_FONDO).grid(row=0,column=0,sticky=E,pady=5)
        Label(frameTotales, text="Total Grandes: ",font=(Widgets.FUENTE_PRINCIPAL, 12),bg=Widgets.COLOR_FONDO).grid(row=0,column=2,sticky=E,pady=5)
        Label(frameTotales, text="Tapas: ",font=(Widgets.FUENTE_PRINCIPAL, 12),bg=Widgets.COLOR_FONDO).grid(row=0,column=3,sticky=E,pady=5)

        #Botones
        botonCSV = Widgets.botonPrincipal(self.frameInferior,'Generar CSV',self.ventana.destroy)
        botonCSV.pack(side=LEFT, anchor=SW,pady=10,padx=(10,0))
        botonExcel = Widgets.botonPrincipal(self.frameInferior,'Generar Excel',self.ventana.destroy)
        botonExcel.pack(side=LEFT, anchor=CENTER,pady=10,padx=5)
        botonFinalizar = Widgets.botonPrincipal(self.frameInferior,'Cerrar',self.ventana.destroy)
        botonFinalizar.pack(side=RIGHT, anchor=SE,pady=10,padx=(0,10))

class VentanaCalendario(Widgets.VentanaHija):
    def __init__(self,ventanaMadre,fechaEntry):
        
        self.fechaEntry = fechaEntry

        self.ventana = Toplevel(ventanaMadre)
        rutaIcono = Recursos.rutaArchivo('Imagenes/Pantuflas.ico')
        self.ventana.iconbitmap(rutaIcono)

        ancho = 255
        alto = 212

        self.ventana.title("Elija una Fecha")
        self.ventana.geometry(str(ancho)+"x"+str(alto))

        # Add Calendar
        self.calendario = Calendar(self.ventana, selectmode = 'day',date_pattern='dd/mm/yy')
        self.calendario.pack(pady = 0)
    
        # Add Button and Label
        Button(self.ventana, text = "Seleccionar Fecha",
            command = lambda: self.guardar(event=None)).pack(pady = 0,expand=True,fill=BOTH)

        self.ventana.bind('<Double-Button-1>', self.guardar)

    def guardar(self,event):
            fecha = self.calendario.get_date()
            self.fechaEntry.delete(0,END)
            self.fechaEntry.insert(0,fecha)
            self.ventana.destroy()
    