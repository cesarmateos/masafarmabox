from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
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
import csv


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
        TITULO = 'MASAfarmabox ' + Recursos.version
        self.title(TITULO)
        rutaIcono = Recursos.rutaArchivo('Recursos/Imagenes/Pantuflas.ico')
        if os.path.exists(rutaIcono):
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
        rutaLogo = Recursos.rutaArchivo('Recursos/Imagenes/Logo.png')
        logo = Label(self.frameSuperior,bg=Widgets.COLOR_FONDO)

        if os.path.exists(rutaLogo):
            imagenLogo = PhotoImage(file=rutaLogo)       
            logo.configure(image=imagenLogo)
            logo.photo = imagenLogo
        else :
            logo.configure(text="MASA")
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
        self.cargarEstilo()
        self.pantallaAciva  = PantallaInicial(self)

        #Declaro la variable en la que se guarda el dato del segundo escaner
        self.dato2 = 0

    def recibirDatos(self,dato1,dato2):
        if self.pantalla == 1:
            self.validarTransportista(dato1)
        elif self.pantalla == 2:
            self.recepcion.agregarFarmabox(self,dato1,dato2)

    def cargarEstilo(self):
        estilo = Style()
        estilo.theme_use('clam')
        estilo.configure('Treeview.Heading', background=Widgets.COLOR_NARANJA_SUAVE,relief="groove",justify=CENTER)
        estilo.configure("TCombobox",background =Widgets.COLOR_FONDO)
        estilo.map('TCombobox', fieldbackground=[('readonly','white')])
        estilo.map('TCombobox', selectbackground=[('readonly', 'white')])
        estilo.map('TCombobox', selectforeground=[('readonly', 'black')])  


#Semi-Abstracta Pantalla
class Pantalla():

    def __init__(self,ventanaMadre:Ventana):
        ventanaMadre.pantallaActiva = self
        self.ventana = ventanaMadre
        self.limpiarFrame()
    
    def limpiarFrame(self):
        for widgets in self.ventana.contenedor.winfo_children():
            widgets.destroy()
        for widgets in self.ventana.frameInferior.winfo_children():
            widgets.destroy()

    def recibirDatos(self,dato1,dato2):
        pass


#Pantallas
class PantallaInicial(Pantalla):

    def __init__(self,ventana:Ventana):
        
        ventana.encabezado.set("")
        ventana.subtitulo.set("")

        super().__init__(ventana)


        #-------------FRAME CONTENEDOR PRINCIPAL------------
        #Texto
        Label(ventana.contenedor, text="Escanear código QR o ingresar manualmente",font=(Widgets.FUENTE_PRINCIPAL, 15),bg=Widgets.COLOR_FONDO).place(x=210,y=200)
        
        #Entrada de QR
        entradaQR = Entry(ventana.contenedor, font=(Widgets.FUENTE_PRINCIPAL,20), width=20,highlightthickness=2)
        entradaQR.focus_set()
        entradaQR.place(x=235,y=250)
        entradaQR.bind('<Return>',lambda event: self.recibirTransportistaTexto(entradaQR))

        
        #Boton Lupa
        botonLupa = Widgets.Btn(ventana.contenedor, imagenNormal='Lupa.png', imagenHover='LupaHover.png', command=lambda: self.recibirTransportistaTexto(entradaQR))
        botonLupa.place(x=600,y=245) 


        #-------------FRAME INFERIOR------------
        #Boton Consultas         
        botonConsultas = Widgets.botonPrincipal(ventana.frameInferior,'Consultas',lambda: PantallaConsultas(ventana))
        botonConsultas.pack(side=RIGHT, anchor=SE)

        #Boton Configuración       
        botonConfiguración = Widgets.botonPrincipal(ventana.frameInferior,'Configuración',lambda: PantallaConfiguracion(ventana))
        botonConfiguración.pack(side=LEFT, anchor=SW)
        
        #Boton Administración         
        botonAdministracion = Widgets.botonPrincipal(ventana.frameInferior,'Administración',lambda: VentanaPassword(ventana,440,170,"Acceso Administración"))
        botonAdministracion.pack(side=LEFT, anchor=SW,padx=10)

    def recibirDatos(self,dato1,dato2):
        self.validarTransportista(dato1)

    def recibirTransportistaTexto(self,entradaQR):
        nroTransportista = entradaQR.get()
        entradaQR.delete(0, 'end')
        self.validarTransportista(nroTransportista)

    def validarTransportista(self,nroTransportista):
        try:
            tuplaResultadoQuery = BaseDatos.encontrarTransportista(nroTransportista)
        except:
            messagebox.showinfo(message="Error al conectarse a la base datos")
        else:
            if (tuplaResultadoQuery == None):
                messagebox.showinfo(message="El transportista "+str(nroTransportista)+" no existe", title="Transportista no encontrado")
            else:
                #transportista = list(tuplaResultadoQuery)
                transportista = Recepcion.Transportista(tuplaResultadoQuery)
                recepcion = Recepcion.Recepcion(transportista)
                self.limpiarFrame()

                #--Frame Medio--
                Label(self.ventana.contenedor, text=transportista.nombre+" - "+transportista.empresa,font=(Widgets.FUENTE_PRINCIPAL, 20),bg=Widgets.COLOR_FONDO).pack(anchor=CENTER,side=TOP,pady=(180,20))
                frameRadio = Frame(self.ventana.contenedor,background=Widgets.COLOR_FONDO)
                frameRadio.pack(anchor=CENTER,side=TOP)
                Label(frameRadio, text="Radio",font=(Widgets.FUENTE_PRINCIPAL, 13),bg=Widgets.COLOR_FONDO).grid(column=0,row=0,padx=3)
                textoCodRadio = StringVar()
                textoCodRadio.set(transportista.radio.codigo+": "+transportista.radio.descripcion)
                radioElegido = Label(frameRadio, textvariable=textoCodRadio,font=(Widgets.FUENTE_PRINCIPAL, 13),bg=Widgets.COLOR_FONDO)
                radioElegido.grid(column=1,row=0)
                botonCambiar = Widgets.botonMicroNaranja(frameRadio,"Cambiar",lambda: self.cambiarValorRadio(frameRadio,radioElegido,textoCodRadio,botonCambiar,recepcion))
                botonCambiar.grid(row=0,column=2,sticky=W,padx=10)

                #--Frame Inferior--
                botonVolver = Widgets.botonSecundario(self.ventana.frameInferior,'Cancelar',lambda: PantallaInicial(self.ventana))        
                botonVolver.pack(side=LEFT, anchor=SW)
                botonFinalizar = Widgets.botonPrincipal(self.ventana.frameInferior,'Iniciar Recepción',lambda: PantallaRecepcion(self.ventana,recepcion))        
                botonFinalizar.pack(side=RIGHT, anchor=SE)

    def cambiarValorRadio(self,contenedor, radioElegido,textoVariable,botonCambiar,recepcion : Recepcion.Recepcion):
        radios = BaseDatos.obtenerRadios()
        valores = [valores[0]+" - "+valores[1] for valores in radios]
        radioElegido.grid_remove()
        lista = Combobox(contenedor,values=valores,state='readonly',width=40)
        lista.current(0)
        lista.grid(row=0,column=1,sticky=W)
        botonCambiar.grid_remove()
        botonGuardar = Widgets.botonMicroMorado(contenedor,"Guardar",lambda: self.guardarCambiosRadio(botonGuardar,botonCambiar,radioElegido,textoVariable,lista,radios,recepcion))
        botonGuardar.grid(row=0,column=2,sticky=W,padx=10)    
        
    def guardarCambiosRadio(self,
                    botonGuardar,
                    botonCambiar,
                    radioElegido,
                    textoVariable,
                    lista,
                    radios,
                    recepcion : Recepcion.Recepcion):
        radioElegido.grid()
        botonCambiar.grid()
        botonGuardar.destroy()
        dato = str(lista.get())
        recepcion.radio = Recepcion.Radio(radios[lista.current()][0],radios[lista.current()][1])
        lista.destroy()
        textoVariable.set(dato)

class PantallaRecepcion(Pantalla):

    def __init__(self,ventana:Ventana,recepcion : Recepcion.Recepcion):

        super().__init__(ventana)


        #Variable al pedo
        contenedorGeneral = ventana.contenedor

        #Variable de la recepción    
        self.recepcion = recepcion

        #Genero Encabezado
        ventana.encabezado.set(recepcion.transportista.nombre+ " - "+ recepcion.transportista.empresa)
        ventana.subtitulo.set("Radio : " +recepcion.radio.codigo+"  ("+recepcion.radio.descripcion+")")

        #Creo los 3 frames
        frameTitulos = Frame(contenedorGeneral,height=ventana.altoFrameTitulos,background=Widgets.COLOR_FONDO)
        frameTitulos.pack(side=TOP,padx=Widgets.MARGEN_X)
        altoFrameNroFarmabox = ventana.altoFrameMedio - (ventana.altoFrameTitulos*2)
        frameMedio = Frame(contenedorGeneral,height=altoFrameNroFarmabox,background=Widgets.COLOR_FONDO)
        frameMedio.pack(fill=BOTH,expand=True,padx=Widgets.MARGEN_X,side=TOP)
        frameTotales = Frame(contenedorGeneral,height=ventana.altoFrameTitulos,background=Widgets.COLOR_FONDO)
        frameTotales.pack(fill=Y,expand=False,padx=Widgets.MARGEN_X,side=BOTTOM)

        
        anchoLinea = ventana.anchoVentana-Widgets.MARGEN_X*2

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
        anchoFrameCubetas = (ventana.anchoVentana-Widgets.MARGEN_X*2)/2
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
        canvasChicos.create_window((1,1), window=self.frameScrollChicos, anchor=NW, tags="frameChicos")

        scrollGrandes = Scrollbar(frameGrandes,orient=VERTICAL, command=canvasGrandes.yview)
        scrollGrandes.pack(side=RIGHT,fill=Y)
        canvasGrandes.configure(yscrollcommand=scrollGrandes.set)
        canvasGrandes.create_window((1,1), window=self.frameScrollGrandes, anchor=NW, tags="frameGrandes")

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
        margenX = 13
        anchoPopUp = 440
        #Boton Cancelar
        botonCancelar = Widgets.botonSecundario(ventana.frameInferior,'Cancelar',lambda:  VentanaCancelaRecepcion(ventana,anchoPopUp,180,"Confirmar Cancelación de Recepción"))
        botonCancelar.grid(row=3,column=0,sticky=EW,padx=(0,margenX))

        #Boton Tapas
        botonTapas = Widgets.botonPrincipal(ventana.frameInferior,'Ingresar Tapas',lambda: VentanaTapas(ventana,self,anchoPopUp,170,"Ingreso Tapas"))         
        botonTapas.grid(row=3,column=1,sticky=EW,padx=margenX)

        #Boton Farmabox   
        botonFarmabox = Widgets.botonPrincipal(ventana.frameInferior,'Ingresar Farmabox',lambda: VentanaFarmabox(ventana,self,anchoPopUp,300,"Carga Manual de Farmabox"))
        botonFarmabox.grid(row=3,column=2,sticky=EW,padx=margenX)

        #Boton Ver Rechazados
        botonRechazados = Widgets.botonPrincipal(ventana.frameInferior,'Ver Rechazados',lambda : VentanCargaRechazados(ventana,self,anchoPopUp,300,"Rechazados"))       
        botonRechazados.grid(row=3,column=3,sticky=EW,padx=margenX)

        #Boton Finalizar
        botonFinalizar = Widgets.botonPrincipal(ventana.frameInferior,'Finalizar',lambda: VentanaFinalizarRecepcion(ventana,recepcion,anchoPopUp,245,"Finalizar Carga"))
        botonFinalizar.grid(row=3,column=4,sticky=EW,padx=(margenX,0))

    def recibirDatos(self,dato1,dato2):
        self.recepcion.agregarFarmabox(self,dato1,dato2)
          
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
    
class PantallaConsultas(Pantalla):

    def __init__(self,ventana:Ventana):

        super().__init__(ventana)
        
        #-------------FRAME SUPERIOR------------
        #Titulo
        ventana.encabezado.set("Consultas")

        #-------------FRAME MEDIO------------
        margenY = 2

        #Divido la pantalla en dos frames
        anchoFrame = (ventana.anchoVentana/2) - Widgets.MARGEN_X
        frameIzquierdo = Frame(ventana.contenedor,height=ventana.altoFrameMedio,width=anchoFrame,background=Widgets.COLOR_FONDO)
        frameIzquierdo.propagate(False)
        frameIzquierdo.pack(fill=BOTH,expand=True,padx=(Widgets.MARGEN_X,0),side=LEFT)
        frameDerecho = Frame(ventana.contenedor,height=ventana.altoFrameMedio,width=anchoFrame,background=Widgets.COLOR_FONDO)
        frameDerecho.propagate(False)
        frameDerecho.pack(fill=BOTH,expand=True,side=RIGHT,padx=(0,Widgets.MARGEN_X))
        

        #----Seccion Recepciones----
        seccionRecepciones = Widgets.Seccion(frameIzquierdo," Recepciones",width=anchoFrame,bg=Widgets.COLOR_FONDO)
        seccionRecepciones.grid(row=0,column=0)
        
        
        #Fecha Desde
        Label(seccionRecepciones.contenido, text="Fecha desde",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=0,column=0,sticky=E,pady=margenY,padx=(0,4))
        fechaDesdeRecep = Entry(seccionRecepciones.contenido, font=(Widgets.FUENTE_PRINCIPAL,9), width=10,highlightthickness=2)
        fechaDesdeRecep.grid(row=0,column=1,sticky=E,pady=margenY)
        botonPickFechaDesdeRecepcion = Widgets.botonMicroNaranja(seccionRecepciones.contenido,"Elegir",lambda: VentanaCalendario(ventana,fechaDesdeRecep))
        botonPickFechaDesdeRecepcion.grid(row=0,column=2,sticky=E,pady=margenY,padx=2)   

        #Fecha Hasta
        Label(seccionRecepciones.contenido, text="Fecha hasta",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=1,column=0,sticky=E,padx=(10,4),pady=margenY)
        fechaHastaRecep = Entry(seccionRecepciones.contenido, font=(Widgets.FUENTE_PRINCIPAL,9), width=10,highlightthickness=2)
        fechaHastaRecep.grid(row=1,column=1,sticky=E,pady=margenY)
        botonPickFechaHastaRecepcion = Widgets.botonMicroNaranja(seccionRecepciones.contenido,"Elegir",lambda: VentanaCalendario(ventana,fechaHastaRecep))
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
        transportistas = BaseDatos.obtenerTransportistasActivos()
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

        #Estado
        Label(seccionRecepciones.contenido, text="Estado",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=5,column=0,sticky=E,pady=margenY,padx=(0,4))
        estados = [(0,"Procesados"),(1,"Sin Procesar"),(2,"TODOS")]
        valoresEstados = [valores[1] for valores in estados]  
        listaEstado = Combobox(seccionRecepciones.contenido,values=valoresEstados,state='readonly',width=40)
        listaEstado.current(len(valoresEstados)-1)
        listaEstado.grid(row=5,column=1,sticky=W,columnspan=3,pady=margenY)

        
        #Buscar
        botonBuscarRecepcionA = Widgets.botonMicroNaranja(seccionRecepciones.contenido,"Buscar",lambda: VentanaRecepciones(ventana,ventana.anchoVentana,600,"Consulta Recepciones",fechaDesdeRecep.get(),fechaHastaRecep.get(),(listaRadio.current(),radios),(listaTransp.current(),transportistas),(listaEmpresa.current(),empresas),(listaEstado.current(),estados)))
        botonBuscarRecepcionA.grid(row=6,column=2,sticky=E,pady=(margenY,0))   

        
        #Detalle Recepción
        Label(seccionRecepciones.contenido, text="Recepción Nro",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=7,column=0,sticky=E,pady=(20,margenY),padx=(0,4))
        detalleRecepcion = Entry(seccionRecepciones.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=18,highlightthickness=2)
        detalleRecepcion.grid(row=7,column=1,sticky=W,pady=(20,margenY))
        detalleRecepcion.bind('<Return>', lambda event: self.buscarRecepcion(detalleRecepcion.get()))
        botonBuscarRecepcionB = Widgets.botonMicroNaranja(seccionRecepciones.contenido,"Buscar",lambda: self.buscarRecepcion(detalleRecepcion.get()))
        botonBuscarRecepcionB.grid(row=7,column=2,sticky=E,pady=(20,margenY))   
        

        
        #----Seccion Farmabox----
        seccionFarmabox = Widgets.Seccion(frameIzquierdo," Farmabox (Kardex)",width=anchoFrame,bg=Widgets.COLOR_FONDO)
        seccionFarmabox.grid(row=1,column=0)
        
        #Fecha Desde
        Label(seccionFarmabox.contenido, text="Fecha desde",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=0,column=0,sticky=E,pady=margenY,padx=(0,4))
        fechaDesdeFarma = Entry(seccionFarmabox.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=10,highlightthickness=2)
        fechaDesdeFarma.grid(row=0,column=1,sticky=E,pady=margenY)
        botonPickFechaDesdeFarma = Widgets.botonMicroNaranja(seccionFarmabox.contenido,"Elegir",lambda: VentanaCalendario(ventana,fechaDesdeFarma))
        botonPickFechaDesdeFarma.grid(row=0,column=2,sticky=E,pady=margenY,padx=(4,0)) 

        #Fecha Hasta
        Label(seccionFarmabox.contenido, text="Fecha hasta",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=1,column=0,sticky=E,padx=(10,4),pady=margenY)
        fechaHastaFarma = Entry(seccionFarmabox.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=10,highlightthickness=2)
        fechaHastaFarma.grid(row=1,column=1,sticky=E,pady=margenY)
        botonPickFechaHastaFarma = Widgets.botonMicroNaranja(seccionFarmabox.contenido,"Elegir",lambda: VentanaCalendario(self,fechaHastaFarma))
        botonPickFechaHastaFarma.grid(row=1,column=2,sticky=E,pady=margenY,padx=(4,0)) 

        #Número Farmabox
        Label(seccionFarmabox.contenido, text="Nro Farmabox",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=2,column=0,sticky=E,pady=margenY,padx=(20,4))
        nroFarmabox = Entry(seccionFarmabox.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=23,highlightthickness=2)
        nroFarmabox.grid(row=2,column=1,columnspan=2,sticky=E,pady=margenY)

        #Buscar Farmabox
        nroFarmabox.bind('<Return>',lambda event: self.buscarFarmabox(nroFarmabox.get(),fechaDesdeFarma.get(),fechaHastaFarma.get()))
        botonBuscarFarmabox = Widgets.botonMicroNaranja(seccionFarmabox.contenido,"Buscar",lambda: self.buscarFarmabox(nroFarmabox.get(),fechaDesdeFarma.get(),fechaHastaFarma.get() ))
        botonBuscarFarmabox.grid(row=3,column=2,columnspan=3,sticky=E,pady=(margenY,0),padx=0)



        
        #--Seccion Rechazados--
        seccionRechazados = Widgets.Seccion(frameDerecho," Rechazados",width=anchoFrame,bg=Widgets.COLOR_FONDO)
        seccionRechazados.grid(row=0,column=0)
        
        #Fecha Desde
        Label(seccionRechazados.contenido, text="Fecha desde",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=0,column=0,sticky=E,pady=margenY,padx=(0,4))
        fechaRechazDesde = Entry(seccionRechazados.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=10,highlightthickness=2)
        fechaRechazDesde.grid(row=0,column=1,sticky=E,pady=margenY)
        botonPickFechaDesdeRechaz = Widgets.botonMicroNaranja(seccionRechazados.contenido,"Elegir",lambda: VentanaCalendario(ventana,fechaRechazDesde))
        botonPickFechaDesdeRechaz.grid(row=0,column=2,sticky=E,pady=margenY,padx=(10,0))


        #Fecha Hasta
        Label(seccionRechazados.contenido, text="Fecha hasta",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=1,column=0,sticky=E,padx=(10,4),pady=margenY)
        fechaRechazHasta = Entry(seccionRechazados.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=10,highlightthickness=2)
        fechaRechazHasta.grid(row=1,column=1,sticky=E,pady=margenY)
        botonPickFechaHastaRechaz = Widgets.botonMicroNaranja(seccionRechazados.contenido,"Elegir",lambda: VentanaCalendario(ventana,fechaRechazHasta))
        botonPickFechaHastaRechaz.grid(row=1,column=2,sticky=E,pady=margenY,padx=(10,0))
        
        #Motivo
        Label(seccionRechazados.contenido, text="Motivo",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=2,column=0,sticky=E,pady=margenY,padx=(5,4))
        motivosRechazo = BaseDatos.obtenerMotivosRechazo()
        motivosRechazo.append((0,"TODOS LOS MOTIVOS"))
        valoresMotivoRechazo = [valores[1] for valores in motivosRechazo]
        listaRechazados = Combobox(seccionRechazados.contenido,values=valoresMotivoRechazo,state='readonly',width=40)
        listaRechazados.current(len(valoresMotivoRechazo)-1)
        listaRechazados.grid(row=2,column=1,columnspan=3,sticky=W,pady=margenY)

        Label(seccionRechazados.contenido, text="Recepción Nro",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=3,column=0,sticky=E,pady=margenY,padx=(5,4))
        nroRecepcionRechazados = Entry(seccionRechazados.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=18,highlightthickness=2)
        nroRecepcionRechazados.grid(row=3,column=1,columnspan=3,sticky=W,pady=margenY)
        nroRecepcionRechazados.bind('<Return>',lambda event: VentanRechazados(ventana,780,600,"Consulta Rechazos",fechaRechazDesde.get(),fechaRechazHasta.get(),(listaRechazados.current(),motivosRechazo),nroRecepcionRechazados.get()))
        
        #Buscar
        botonBuscarRechazo = Widgets.botonMicroNaranja(seccionRechazados.contenido,"Buscar",lambda: VentanRechazados(ventana,760,600,"Consulta Rechazos",fechaRechazDesde.get(),fechaRechazHasta.get(),(listaRechazados.current(),motivosRechazo),nroRecepcionRechazados.get()))
        botonBuscarRechazo.grid(row=4,column=3,columnspan=3,sticky=E,pady=(margenY,0))  

        
        #--Seccion Movimientos--
        seccionMovimientos = Widgets.Seccion(frameDerecho," Modificaciones Farmabox",width=anchoFrame,bg=Widgets.COLOR_FONDO)
        seccionMovimientos.grid(row=3,column=0)
        
        #Fecha Desde
        Label(seccionMovimientos.contenido, text="Fecha desde",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=0,column=0,sticky=E,pady=margenY,padx=(0,4))
        fechaModDesde = Entry(seccionMovimientos.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=10,highlightthickness=2)
        fechaModDesde.grid(row=0,column=1,sticky=E,pady=margenY)
        botonPickFechaDesdeMod = Widgets.botonMicroNaranja(seccionMovimientos.contenido,"Elegir",lambda: VentanaCalendario(ventana,fechaModDesde))
        botonPickFechaDesdeMod.grid(row=0,column=2,sticky=E,pady=margenY,padx=(10,0))


        #Fecha Hasta
        Label(seccionMovimientos.contenido, text="Fecha hasta",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=1,column=0,sticky=E,padx=(10,4),pady=margenY)
        fechaModHasta = Entry(seccionMovimientos.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=10,highlightthickness=2)
        fechaModHasta.grid(row=1,column=1,sticky=E,pady=margenY)
        botonPickFechaHastaMod = Widgets.botonMicroNaranja(seccionMovimientos.contenido,"Elegir",lambda: VentanaCalendario(ventana,fechaModHasta))
        botonPickFechaHastaMod.grid(row=1,column=2,sticky=E,pady=margenY,padx=(10,0))
        
        Label(seccionMovimientos.contenido, text="Tipo Modif.",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=2,column=0,sticky=E,pady=margenY,padx=(0,4))
        tiposModificacion = BaseDatos.obtenerTiposModificacion()
        tiposModificacion.append((0,"TODOS LOS MOTIVOS"))
        valoresTipoMod = [valores[1] for valores in tiposModificacion]
        listaMod = Combobox(seccionMovimientos.contenido,values=valoresTipoMod,state='readonly',width=40)
        listaMod.current(len(valoresTipoMod)-1)
        listaMod.grid(row=2,column=1,sticky=W,columnspan=3,pady=margenY)

        botonBuscarMovA = Widgets.botonMicroNaranja(seccionMovimientos.contenido,"Buscar",lambda: VentanaModificaciones(ventana,ventana.anchoVentana,500,"Consulta Modificaciones",fechaModDesde.get(),fechaModHasta.get(),(listaMod.current(),tiposModificacion)))
        botonBuscarMovA.grid(row=3,column=2,columnspan=2,sticky=E,pady=(margenY,0))   

        
        Label(seccionMovimientos.contenido, text="Modificación Nro",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=4,column=0,sticky=E,pady=(20,0),padx=(20,4))
        detalleModificacion = Entry(seccionMovimientos.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=18,highlightthickness=2)
        detalleModificacion.grid(row=4,column=1,columnspan=3,sticky=W,pady=(20,0))
        detalleModificacion.bind('<Return>',lambda event: self.buscarModificacion(detalleModificacion.get()))
        botonBuscarMovB = Widgets.botonMicroNaranja(seccionMovimientos.contenido,"Buscar",lambda: self.buscarModificacion(detalleModificacion.get()))
        botonBuscarMovB.grid(row=4,column=2,columnspan=2,sticky=E,pady=(20,0),padx=(10,0) )
        


        #-------------FRAME INFERIORR------------
        #Boton Finalizar
        botonFinalizar = Widgets.botonPrincipal(ventana.frameInferior,'Volver',lambda: PantallaInicial(ventana))         
        botonFinalizar.pack(anchor=SE)


    def buscarRecepcion(self,nroRecepcion):
        if nroRecepcion == '':
            messagebox.showinfo(message="Debe completar el campo \" Recepción Nro \"", title="Campo Nulo")
        else:
            recepcion = BaseDatos.buscarRecepcion(nroRecepcion)
            if recepcion == []:
                messagebox.showinfo(message="Recepción "+nroRecepcion+" no encontrada.", title="Recepción inexistente")
            else:
                VentanaDetalleRecepcion(self.ventana,650,600,"Detalle de Recepción",recepcion)

    def buscarFarmabox(self,nroFarmabox,fechaD,fechaH):
        if nroFarmabox == '':
            messagebox.showinfo(message="Debe completar el campo \" Nro. Farmabox \"", title="Campo Nulo")
        else:
            recepcion = BaseDatos.buscarKardexFarmabox(nroFarmabox,fechaD,fechaH)
            if recepcion[0] == []:
                messagebox.showinfo(message="Farmabox "+nroFarmabox+" no encontrado.", title="Farmabox inexistente")
            else:
                VentanaKardexFarmabox(self.ventana,700,600,"Kardex Farmabox",recepcion)

    def buscarModificacion(self,nroModificacion):
        if nroModificacion == '':
            messagebox.showinfo(message="Debe completar el campo \" Modificación Nro \"", title="Campo Nulo")
        else:
            modificacion = BaseDatos.buscarModificacion(nroModificacion)
            if modificacion == []:
                messagebox.showinfo(message="Recepción "+nroModificacion+" no encontrada.", title="Recepción inexistente")
            else:
                VentanaDetallesModificacion(self.ventana,650,600,"Detalle de Modificación de Farmabox",modificacion)

class PantallaConfiguracion(Pantalla):

    def __init__(self,ventana:Ventana):

        super().__init__(ventana)
        
        #-------------FRAME SUPERIOR------------
        #Titulo
        ventana.encabezado.set("Configuración")
        ventana.subtitulo.set("Reiniciar luego de efectuar los cambios")


        #-------------FRAME MEDIO------------
        #Armo un Frame con márgenes
        anchoFrame = ventana.anchoVentana-Widgets.MARGEN_X*2 
        frameMedio = Frame(ventana.contenedor,height=ventana.altoFrameMedio,width=anchoFrame,background=Widgets.COLOR_FONDO)
        frameMedio.pack(fill=BOTH,expand=True,padx=Widgets.MARGEN_X,side=TOP)

        #Valores Puertos COM
        valoresCOM = []
        for i in range (1,21):
            valoresCOM.append("COM"+str(i))

        #Valores Puertos Baud Rates
        valoresBaudios = [1200,1800,2400,4800,7200,9600,14400,19200,38400,57600,115200,128000]


        #--Seccion Scanner 1--
        seccionScannner1 = Widgets.Seccion(frameMedio,"Scanner 1",width=ventana.anchoVentana,bg=Widgets.COLOR_FONDO)
        seccionScannner1.grid(row=0,column=0)

        #Puerto Scanner 1
        Label(seccionScannner1.contenido, text="Puerto :",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=0,column=0,sticky=E)
        textoPuertoScanner1Variable = StringVar()
        textoPuertoScanner1Variable.set(Recursos.puertoScanner1)
        puertoScanner1 = Label(seccionScannner1.contenido, textvariable=textoPuertoScanner1Variable,font=(Widgets.FUENTE_PRINCIPAL, 10),bg=Widgets.COLOR_FONDO,anchor=W)
        puertoScanner1.grid(row=0,column=1,sticky=W,padx=(5,47))
        botonCambiarSerial1 = Widgets.botonMicroNaranja(seccionScannner1.contenido,"Cambiar",lambda: self.cambiarValorConfiguracion(seccionScannner1.contenido,textoPuertoScanner1Variable,botonCambiarSerial1,0,1,valoresCOM,'Scanner1', 'PUERTO'))
        botonCambiarSerial1.grid(row=0,column=2,sticky=W)

        #Baudrate Scanner 1
        Label(seccionScannner1.contenido, text="Baud Rate (bits por seg):",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=(30,0),row=0,column=3,sticky=E)
        textoBaud1 = StringVar()
        textoBaud1.set(Recursos.baudScanner2)
        baudScanner1 = Label(seccionScannner1.contenido, textvariable=textoBaud1,font=(Widgets.FUENTE_PRINCIPAL, 10),bg=Widgets.COLOR_FONDO,anchor=W)
        baudScanner1.grid(row=0,column=4,sticky=W,padx=(5,47))
        botonCambiarBaud1 = Widgets.botonMicroNaranja(seccionScannner1.contenido,"Cambiar",lambda: self.cambiarValorConfiguracion(seccionScannner1.contenido,textoBaud1,botonCambiarBaud1,0,4,valoresBaudios,'Scanner1', 'BAUD'))
        botonCambiarBaud1.grid(row=0,column=5,sticky=W)

        #--Seccion Scanner 2--
        seccionScannner2 = Widgets.Seccion(frameMedio,"Scanner 2",width=ventana.anchoVentana,bg=Widgets.COLOR_FONDO)
        seccionScannner2.grid(row=1,column=0)

        #Puerto Scanner 2
        Label(seccionScannner2.contenido, text="Puerto :",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(row=0,column=0,sticky=E)
        textoPuertoScanner2Variable = StringVar()
        textoPuertoScanner2Variable.set(Recursos.puertoScanner2)
        puertoScanner2 = Label(seccionScannner2.contenido, textvariable=textoPuertoScanner2Variable,font=(Widgets.FUENTE_PRINCIPAL, 10),bg=Widgets.COLOR_FONDO,anchor=W)
        puertoScanner2.grid(row=0,column=1,sticky=W,padx=(5,47))
        botonCambiarSerial2 = Widgets.botonMicroNaranja(seccionScannner2.contenido,"Cambiar",lambda: self.cambiarValorConfiguracion(seccionScannner2.contenido,textoPuertoScanner2Variable,botonCambiarSerial2,0,1,valoresCOM,'Scanner2', 'PUERTO'))
        botonCambiarSerial2.grid(row=0,column=2,sticky=W)

        #Baudrate Scanner 2
        Label(seccionScannner2.contenido, text="Baud Rate (bits por seg):",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=(30,0),row=0,column=3,sticky=E)
        textoBaud2 = StringVar()
        textoBaud2.set(Recursos.baudScanner2)
        baudScanner2 = Label(seccionScannner2.contenido, textvariable=textoBaud2,font=(Widgets.FUENTE_PRINCIPAL, 10),bg=Widgets.COLOR_FONDO,anchor=W)
        baudScanner2.grid(row=0,column=4,sticky=W,padx=(5,47))
        botonCambiarBaud2 = Widgets.botonMicroNaranja(seccionScannner2.contenido,"Cambiar",lambda: self.cambiarValorConfiguracion(seccionScannner2.contenido,textoBaud2,botonCambiarBaud2,0,4,valoresBaudios,'Scanner2', 'BAUD'))
        botonCambiarBaud2.grid(row=0,column=5,sticky=W)

        #--Seccion Sincronizacion--
        seccionSincro = Widgets.Seccion(frameMedio,"Sincronización de Scanners",width=ventana.anchoVentana,bg=Widgets.COLOR_FONDO)
        seccionSincro.grid(row=2,column=0)

        #Tolerancia
        valoresTolerancia = []
        for i in range (1,21):
            valoresTolerancia.append(str(round(i*0.05,2)))

        Label(seccionSincro.contenido, text="Tolerancia (segundos): ",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=(5,0),row=0,column=0,sticky=W)
        textoTolereancia = StringVar()
        textoTolereancia.set(Recursos.delayScanner)
        tolerancia = Label(seccionSincro.contenido, textvariable=textoTolereancia,font=(Widgets.FUENTE_PRINCIPAL, 10),bg=Widgets.COLOR_FONDO,anchor=W)
        tolerancia.grid(row=0,column=1,sticky=W,padx=(5,55))
        botonCambiarTolerancia = Widgets.botonMicroNaranja(seccionSincro.contenido,"Cambiar",lambda: self.cambiarValorConfiguracion(seccionSincro.contenido,textoTolereancia,botonCambiarTolerancia,0,1,valoresTolerancia,'Sincronizacion', 'tolerancia'))
        botonCambiarTolerancia.grid(row=0,column=2,sticky=W)


        #--Seccion Impresora--
        seccionImpresora = Widgets.Seccion(frameMedio,"Impresora",width=ventana.anchoVentana,bg=Widgets.COLOR_FONDO)
        seccionImpresora.grid(row=3,column=0)

        #Backfeed
        valoresFeed = []
        for i in range (1,81):
            valoresFeed.append(str(i*10))

        Label(seccionImpresora.contenido, text="Retroseso Etiqueta Previo: ",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=(5,0),row=0,column=0,sticky=W)
        textoBackFeed = StringVar()
        textoBackFeed.set(Recursos.backfeed)
        backFeed = Label(seccionImpresora.contenido, textvariable=textoBackFeed,font=(Widgets.FUENTE_PRINCIPAL, 10),bg=Widgets.COLOR_FONDO,anchor=W)
        backFeed.grid(row=0,column=1,sticky=W,padx=(5,52))
        botonCambiarBackFeed = Widgets.botonMicroNaranja(seccionImpresora.contenido,"Cambiar",lambda: self.cambiarValorConfiguracion(seccionImpresora.contenido,textoBackFeed,botonCambiarBackFeed,0,1,valoresFeed,'Impresora', 'backfeed'))
        botonCambiarBackFeed.grid(row=0,column=2,sticky=W)
        
        Label(seccionImpresora.contenido, text="Alimento Etiqueta Posterior: ",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=(30,0),row=0,column=3,sticky=W)
        textoFeed = StringVar()
        textoFeed.set(Recursos.feed)
        feed = Label(seccionImpresora.contenido, textvariable=textoFeed,font=(Widgets.FUENTE_PRINCIPAL, 10),bg=Widgets.COLOR_FONDO,anchor=W)
        feed.grid(row=0,column=4,sticky=W,padx=(5,52))
        botonCambiarFeed = Widgets.botonMicroNaranja(seccionImpresora.contenido,"Cambiar",lambda: self.cambiarValorConfiguracion(seccionImpresora.contenido,textoFeed,botonCambiarFeed,0,4,valoresFeed,'Impresora', 'feed'))
        botonCambiarFeed.grid(row=0,column=5,sticky=W)



        #-------------FRAME INFERIOR------------
        #Boton Reiniciar            
        botonGuardar = Widgets.botonPrincipal(ventana.frameInferior,'Reiniciar',self.reiniciar)
        botonGuardar.pack(side=LEFT, anchor=SW)

        #Boton Volver       
        botonFinalizar = Widgets.botonPrincipal(ventana.frameInferior,'Volver',lambda: PantallaInicial(ventana))
        botonFinalizar.pack(side=RIGHT, anchor=SE)

    def cambiarValorConfiguracion(self,contenedor, textoVariable,botonCambiar,fila,columna,valores,grupo,item):
        lista = Combobox(contenedor,values=valores,state='readonly',width=10)
        lista.current(0)
        lista.grid(row=fila,column=columna,sticky=W)
        botonCambiar.grid_remove()
        botonGuardar = Widgets.botonMicroMorado(contenedor,"Guardar",lambda: self.guardarCambios(botonGuardar,botonCambiar,textoVariable,lista,grupo,item))
        botonGuardar.grid(row=fila,column=columna+1,sticky=W)

    def guardarCambios(self,botonGuardar,botonCambiar,textoVariable,lista,grupo,item):
        botonCambiar.grid()
        botonGuardar.destroy()
        dato = str(lista.get())
        lista.destroy()
        textoVariable.set(dato)
        Recursos.modificarConfig(grupo,item,dato)
   
    def reiniciar(self):
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

class PantallaAdministracion(Pantalla):

    def __init__(self,ventana:Ventana):

        super().__init__(ventana)

        #-------------FRAME SUPERIOR------------
        #Titulo
        ventana.encabezado.set("Administración")
        ventana.subtitulo.set("")

        #-------------FRAME MEDIO------------
        #Armo un Frame con márgenes
        anchoFrame = ventana.anchoVentana-Widgets.MARGEN_X*2 
        frameMedioGeneral = Frame(ventana.contenedor,height=ventana.altoFrameMedio,width=anchoFrame,background=Widgets.COLOR_FONDO)
        frameMedioGeneral.pack(fill=BOTH,expand=True,padx=(Widgets.MARGEN_X,0),side=TOP)

        # Creo Canvas y Scroll dentro de Frame
        canvasScrollAdmin = Canvas(frameMedioGeneral, bg=Widgets.COLOR_FONDO,borderwidth=0,highlightthickness=0,width=anchoFrame-(Widgets.MARGEN_X*2),height=ventana.altoFrameMedio)
        canvasScrollAdmin.pack(side=LEFT,fill=BOTH,expand=TRUE)
        scrollAdmin = Scrollbar(frameMedioGeneral,orient=VERTICAL, command=canvasScrollAdmin.yview)
        scrollAdmin.pack(side=RIGHT,fill=Y,pady=(10,0))

        #Creo Frame Scrolleable dentro del canvas y linkeo con Scroll
        frameMedio = Frame(canvasScrollAdmin,background=Widgets.COLOR_FONDO)
        canvasScrollAdmin.configure(yscrollcommand=scrollAdmin.set)
        canvasScrollAdmin.create_window((1,1), window=frameMedio, anchor=NW, tags="frameMedio")


        #--Seccion Agregar--
        seccionAgregar = Widgets.Seccion(frameMedio,"Agregar Registro",width=ventana.anchoVentana,bg=Widgets.COLOR_FONDO)
        seccionAgregar.grid(row=0,column=0)
        
        Label(seccionAgregar.contenido, text="Nueva Empresa",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,fg=Widgets.COLOR_NARANJA,anchor=W).grid(padx=0,row=0,column=0,columnspan=3,sticky=W)
        Widgets.linea(seccionAgregar.contenido,anchoFrame,1,7,fill=Widgets.COLOR_NARANJA)
        Label(seccionAgregar.contenido, text="Nombre: ",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=(5,0),pady=(2,0),row=2,column=0,sticky=W)
        nombreEmpresa = Entry(seccionAgregar.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=23,highlightthickness=2)
        nombreEmpresa.grid(padx=5,pady=(2,0),row=2,column=1,columnspan=2,sticky=W)
        nombreEmpresa.bind('<Return>', lambda event: self.agregarEmpresa(nombreEmpresa.get()))
        botonGuardarEmpresa = Widgets.botonMicroNaranja(seccionAgregar.contenido,"Agregar", lambda: self.agregarEmpresa(nombreEmpresa.get()))
        botonGuardarEmpresa.grid(row=2,column=3,pady=(2,0),sticky=W)

        Label(seccionAgregar.contenido, text="Nuevo Radio",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,fg=Widgets.COLOR_NARANJA,anchor=W).grid(padx=0,pady=(5,0),row=3,column=0,columnspan=3,sticky=W)
        Widgets.linea(seccionAgregar.contenido,anchoFrame,4,7,fill=Widgets.COLOR_NARANJA)
        Label(seccionAgregar.contenido, text="Código : ",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=(5,0),pady=(2,0),row=5,column=0,sticky=W)
        nuevoCodRadio = Entry(seccionAgregar.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=10,highlightthickness=2)
        nuevoCodRadio.grid(padx=5,row=5,column=1,sticky=W)
        Label(seccionAgregar.contenido, text="Descripción: ",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=(5,0),pady=(2,0),row=5,column=2,sticky=W)
        nuevaDescRadio = Entry(seccionAgregar.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=25,highlightthickness=2)
        nuevaDescRadio.grid(padx=5,pady=(2,0),row=5,column=3,columnspan=2,sticky=W)
        botonGardarCodRadio = Widgets.botonMicroNaranja(seccionAgregar.contenido,"Agregar", lambda : self.agregarRadio(nuevoCodRadio.get(),nuevaDescRadio.get()))
        botonGardarCodRadio.grid(row=5,column=5,pady=(2,0),columnspan=2,sticky=W)

        Label(seccionAgregar.contenido, text="Nuevo Transportista",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,fg=Widgets.COLOR_NARANJA,anchor=W).grid(padx=0,pady=(5,0),row=7,column=0,columnspan=3,sticky=W)
        Widgets.linea(seccionAgregar.contenido,anchoFrame,8,7,fill=Widgets.COLOR_NARANJA)
        Label(seccionAgregar.contenido, text="Código: ",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=(5,0),pady=(2,0),row=9,column=0,sticky=W)
        nuevoCodTransportista= Entry(seccionAgregar.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=10,highlightthickness=2)
        nuevoCodTransportista.grid(padx=5,pady=(2,0),row=9,column=1,sticky=W)
        Label(seccionAgregar.contenido, text="Nombre: ",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=(5,0),pady=(2,0),row=9,column=2,sticky=W)
        nuevoNomTransportista= Entry(seccionAgregar.contenido, font=(Widgets.FUENTE_PRINCIPAL,10), width=25,highlightthickness=2)
        nuevoNomTransportista.grid(padx=5,pady=(2,0),row=9,column=3,columnspan=2,sticky=W)

        Label(seccionAgregar.contenido, text="Radio: ",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=(5,0),pady=(2,0),row=9,column=5,sticky=W)
        radios = BaseDatos.obtenerRadios()
        valores = [valores[0]+" - "+valores[1] for valores in radios]
        listaRadios = Combobox(seccionAgregar.contenido,values=valores,state='readonly',width=40)
        listaRadios.current(0)
        listaRadios.grid(row=9,column=6,pady=(2,0),sticky=W)
        Label(seccionAgregar.contenido, text="Empresa: ",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=(5,0),row=10,column=0,sticky=W)
        empresas = BaseDatos.obtenerEmpresas()
        valoresEmp = [valoresEmp[1] for valoresEmp in empresas]
        listaEmpresas = Combobox(seccionAgregar.contenido,values=valoresEmp,state='readonly',width=28)
        listaEmpresas.current(0)
        listaEmpresas.grid(row=10,column=1,padx=5,pady=(2,0),columnspan=2,sticky=W)
        botonGuardarTransportista = Widgets.botonMicroNaranja(seccionAgregar.contenido,"Agregar", lambda : self.agregarTransportista(nuevoCodTransportista.get(),nuevoNomTransportista.get(),(listaRadios.current(),radios),(listaEmpresas.current(),empresas)))
        botonGuardarTransportista.grid(row=10,column=3,pady=(2,0),sticky=W)

        #--Seccion Modificar--
        seccionModificar = Widgets.Seccion(frameMedio,"Modificar Registro",width=ventana.anchoVentana,bg=Widgets.COLOR_FONDO)
        seccionModificar.grid(row=1,column=0,columnspan=7)

        cantidadColumnasSeccionModificar = 3
        seccionModificar.contenido.columnconfigure(2,weight=1)

        Label(seccionModificar.contenido, text="Modificar Transportista",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,fg=Widgets.COLOR_NARANJA,anchor=W).grid(pady=(5,0),row=0,column=0,columnspan=cantidadColumnasSeccionModificar,sticky=W)
        Widgets.linea(seccionModificar.contenido,anchoFrame,1,cantidadColumnasSeccionModificar,fill=Widgets.COLOR_NARANJA)
        
        #Transportista
        Label(seccionModificar.contenido, text="Transportista",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=5,pady=(2,0),row=2,column=0,sticky=W)
        transportistas = BaseDatos.obtenerTransportistas()
        listaTransp = Combobox(seccionModificar.contenido,state='readonly',width=30,postcommand=lambda: self.updateListaTransportistas(listaTransp,transportistas))
        listaTransp.grid(row=2,column=1,sticky=W,pady=(2,0))
         
        codigo = StringVar()
        nombre = StringVar()
        empresa = StringVar()
        radio = StringVar()
        estado = StringVar()

        Label(seccionModificar.contenido, text="Número :",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=5,pady=(2,0),row=3,column=0,sticky=W)
        Label(seccionModificar.contenido, textvariable=codigo,font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=5,pady=(2,0),row=3,column=1,sticky=W)
 
        Label(seccionModificar.contenido, text="Nombre :",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=5,pady=0,row=4,column=0,sticky=W)
        Label(seccionModificar.contenido, textvariable=nombre,font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=5,pady=0,row=4,column=1,sticky=W)

        Label(seccionModificar.contenido, text="Empresa :",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=5,pady=0,row=5,column=0,sticky=W)
        Label(seccionModificar.contenido, textvariable=empresa,font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=5,pady=0,row=5,column=1,sticky=W)
                
        Label(seccionModificar.contenido, text="Radio :",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=5,pady=0,row=6,column=0,sticky=W)
        Label(seccionModificar.contenido, textvariable=radio,font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=5,pady=0,row=6,column=1,sticky=W)
        
        Label(seccionModificar.contenido, text="Estado :",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=5,pady=0,row=7,column=0,sticky=W)
        Label(seccionModificar.contenido, textvariable=estado,font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=5,pady=0,row=7,column=1,sticky=W)

        botonModificarTransportista = Widgets.botonMicroNaranja(seccionModificar.contenido,"Modificar", lambda : self.habilitarCambiosTransportista(seccionModificar.contenido,transportistas,listaTransp,botonModificarTransportista))
        botonModificarTransportista.grid(row=7,column=2,pady=0,sticky=W)
  
        #Conecto la selección del combobox con la función que cambia los datos en pantalla según la elección
        listaTransp.bind('<<ComboboxSelected>>', lambda event :self.cambiarValoresTransportista(codigo,nombre,empresa,radio,estado,transportistas,listaTransp.current()))
        

        #--Seccion Ticket--
        seccionTicket = Widgets.Seccion(frameMedio,"Ticket",width=ventana.anchoVentana,bg=Widgets.COLOR_FONDO)
        seccionTicket.grid(row=2,column=0)

        Label(seccionTicket.contenido, text="Imprimir Radios ",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=5,pady=(2,0),row=0,column=0,sticky=W)
        toggleRadio = Widgets.Toggle(seccionTicket.contenido,Recursos.imprimirRadio)
        toggleRadio.configure(command = lambda: toggleRadio.switch(Recursos.imprimirRadio,'radio'))
        toggleRadio.grid(row=0,column=1,pady=(2,0),sticky=W)
        Label(seccionTicket.contenido, text="Imprimir Detalle ",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=5,pady=(2,0),row=1,column=0,sticky=W)
        toggleDetalle = Widgets.Toggle(seccionTicket.contenido,Recursos.imprimirDetalle)
        toggleDetalle.configure(command = lambda: toggleDetalle.switch(Recursos.imprimirDetalle,'detalle'))
        toggleDetalle.grid(row=1,column=1,pady=(2,0),sticky=W)

        #--Seccion Procesar Datos--
        seccionProcesar = Widgets.Seccion(frameMedio,"Procesar Datos",width=ventana.anchoVentana,bg=Widgets.COLOR_FONDO)
        seccionProcesar.grid(row=3,column=0)

        Label(seccionProcesar.contenido, text="Procesar Recepciones ",font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W).grid(padx=5,pady=(2,0),row=0,column=0,sticky=W)
        botonProcesarRecepciones = Widgets.botonMicroNaranja(seccionProcesar.contenido,"CSV", self.procesarRecepciones)
        botonProcesarRecepciones.grid(row=0,column=1,pady=(2,0),sticky=W)



        #Refresh en cada agregado de celda
        frameMedio.bind("<Configure>", lambda event: canvasScrollAdmin.config(scrollregion=canvasScrollAdmin.bbox("all")))


        #-------------FRAME INFERIOR------------
        #Boton Volver       
        botonFinalizar = Widgets.botonPrincipal(ventana.frameInferior,'Volver',lambda: PantallaInicial(ventana))
        botonFinalizar.pack(side=RIGHT, anchor=SE)

    def agregarEmpresa(self,nombreEmpresa):
        texto = []
        texto.append("Nombre Empresa : "+ nombreEmpresa)
        VentanaAdvierteGuardado(self.ventana,800,250,"Guardando Nueva Empresa",texto,BaseDatos.agregarEmpresa(nombreEmpresa))

    def agregarRadio(self,codigo,descipcion):
        texto = []
        texto.append("Código Radio: "+ codigo)
        texto.append("Descipción: "+ descipcion)
        VentanaAdvierteGuardado(self.ventana,800,250,"Guardando Nuevo Radio",texto,BaseDatos.agregarRadio(codigo,descipcion))

    def agregarTransportista(self,codigo,nombre,tuplaRadios,tuplaEmpresas):
        radio = tuplaRadios[1][tuplaRadios[0]]
        empresa = tuplaEmpresas[1][tuplaEmpresas[0]]
        texto = []
        texto.append("Número:"+ codigo)
        texto.append("Nombre: "+ nombre)
        texto.append("Radio Usual: "+ radio[0])
        texto.append("Empresa: "+ empresa[1])
        VentanaAdvierteGuardado(self.ventana,800,350,"Guardando Nuevo Transportista",texto,BaseDatos.agregarTransportista(codigo,nombre,radio[0],empresa[0]))
    
    def updateListaTransportistas(self, lista,transportistas):
        transportistas = BaseDatos.obtenerTransportistas()
        valoresTransp = [str(valores[0])+" - "+valores[1] for valores in transportistas]
        lista['values'] = valoresTransp

    def habilitarCambiosTransportista(self,
                    contenedor:Frame,
                    transportistas : list,
                    listaTransp : Combobox,
                    boton:Widgets.botonMicroNaranja):
        transportista = Recepcion.Transportista.desdeKey(transportistas[listaTransp.current()][0])
        boton.grid_remove()
        listaTransp.grid_remove()

        textoTransporte = Label(contenedor, text=transportista.nombre,font="Verdana 10 bold",bg=Widgets.COLOR_FONDO,anchor=W)
        textoTransporte.grid(row=2,column=1,sticky=W,pady=(2,0))

        radios = BaseDatos.obtenerRadios()
        valores = [valores[0]+" - "+valores[1] for valores in radios]
        listaRadios = Combobox(contenedor,values=valores,state='readonly',width=40)
        indexRadioActual = [radio[0] for radio in radios].index(transportista.radio.codigo)
        listaRadios.current(indexRadioActual)
        listaRadios.grid(padx=5,pady=0,row=6,column=1,sticky=W)

        listaEstado = Combobox(contenedor,values=("Inactivo","Activo"),state='readonly',width=40)
        listaEstado.current(transportista.estado)
        listaEstado.grid(padx=5,pady=0,row=7,column=1,sticky=W)

        botonGuardar = Widgets.botonMicroMorado(contenedor,"Guardar", lambda: self.cambiarTransportista(boton,botonGuardar,listaTransp,transportistas,transportista,textoTransporte,radios,listaRadios,listaEstado))
        botonGuardar.grid(row=7,column=2,pady=0,sticky=W)

    def cambiarTransportista(self,
                botonModificar:Widgets.botonMicroNaranja,
                botonGuardar:Widgets.botonMicroMorado,
                listaTransporte: Combobox,
                transportistas: list,
                transportista:Recepcion.Transportista,
                textoTransporte: Label,
                radios,
                listaRadios: Combobox,
                listaEstado: Combobox):


        #Instancio el Radio nuevo
        radioElegido = Recepcion.Radio(radios[listaRadios.current()][0],radios[listaRadios.current()][1])

        #Modifico los atributos del transportista con los nuevos
        transportista.estado = listaEstado.current()
        transportista.radio = radioElegido
        BaseDatos.modificarTransportista(transportista)

        #Quito del grid los widgets de Guardar
        botonGuardar.grid_remove()
        textoTransporte.grid_remove()
        listaEstado.grid_remove()
        listaRadios.grid_remove()

        #Quito de la lista de transportistas la tupla(por su inmutabilidad) y genero una nueva y la inserto en el lugar de la anterior
        indiceTransporteCombobox = listaTransporte.current()
        registroViejo = transportistas[indiceTransporteCombobox]
        registroNuevo = (registroViejo[0],registroViejo[1],radios[listaRadios.current()][0],registroViejo[3],listaEstado.current())
        transportistas.remove(registroViejo)
        transportistas.insert(indiceTransporteCombobox,registroNuevo)

        #Agrego al grid los Widgets de Modificar
        botonModificar.grid()
        listaTransporte.grid()

    def cambiarValoresTransportista(self,
                    textoCodigo :StringVar,
                    textoNombre: StringVar,
                    textoEmpresa:StringVar,
                    textoRadio:StringVar,
                    textoEstado:StringVar,
                    transportistas,
                    indice:int):
        textoCodigo.set(transportistas[indice][0])
        textoNombre.set(transportistas[indice][1])
        textoEmpresa.set(transportistas[indice][3])
        textoRadio.set(transportistas[indice][2])
        if(transportistas[indice][4]==1):
            textoEstado.set("Activo")
        else:
            textoEstado.set("Inactivo")

    def procesarRecepciones(self):
        farmaboxes = BaseDatos.procesarRecepciones()
        archivo = filedialog.asksaveasfile(mode ='w',title='Exportar a CSV',filetypes= [("Arhcivo CSV","*.csv")], defaultextension='.csv')
        titulos = ['Número Farmabox']
        with open(archivo.name, 'w+', newline ='',) as archivo:    
            escritor = csv.writer(archivo,delimiter = ";")
            escritor.writerow(titulos)
            escritor.writerows(farmaboxes)


#Ventanas Emergentes de Pantalla Recepción
class VentanaCancelaRecepcion(Widgets.VentanaHija):
    def __init__(self,ventanaMadre,ancho,alto,titulo):
        Widgets.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)
        
        #Texto
        Label(self.contenedor, text='¿Está seguro que quiere cancelar esta recepción?',font=(Widgets.FUENTE_PRINCIPAL, 12),bg=Widgets.COLOR_FONDO,anchor=CENTER).grid(row=0,column=0,columnspan=2,pady=40,padx=10,sticky=EW)
        
        #Botones
        botonVolver = Widgets.botonSecundario(self.frameInferior,'Seguir Recepcionando',self.ventana.destroy)
        botonVolver.pack(side=LEFT, anchor=SW,pady=10,padx=(10,0))
        botonCancelar =  Widgets.botonPrincipal(self.frameInferior,'Cancelar Recepción',self.cancelar)
        botonCancelar.pack(side=RIGHT, anchor=SE,pady=10,padx=(0,10))

    def cancelar(self):
        PantallaInicial(self.ventanaMadre)
        self.ventana.destroy()

class VentanaTapas(Widgets.VentanaHija):
    def __init__(self,ventanaMadre,pantallaRecepcion,ancho,alto,titulo):
        Widgets.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)

        self.pantallaRecepcion = pantallaRecepcion

        #Texto
        Label(self.contenedor, text = "Cantidad de tapas:",font=(Widgets.FUENTE_PRINCIPAL, 15),bg='white').grid(row=1,column=0,pady=28,padx=25,sticky=E)

        #Entrada de Texto
        self.entradaTapas = Entry(self.contenedor, font=(Widgets.FUENTE_PRINCIPAL,15), width=11,highlightthickness=2)
        self.entradaTapas.focus_set()
        self.entradaTapas.grid(row=1,column=1,sticky=W)
        
        #Botones
        botonCancelar = Widgets.botonSecundario(self.frameInferior,'Cancelar',self.ventana.destroy)
        botonCancelar.pack(side=LEFT, anchor=SW,pady=10,padx=(10,0))
        botonFinalizar =  Widgets.botonPrincipal(self.frameInferior,'Cargar Tapas',lambda: self.cargarTapas(self))
        botonFinalizar.pack(side=RIGHT, anchor=SE,pady=10,padx=(0,10))
        
        self.ventana.bind('<Return>', lambda event: self.cargarTapas(self))

    def cargarTapas(self,event):
        self.pantallaRecepcion.recepcion.agregarTapas(self.entradaTapas.get())
        self.pantallaRecepcion.marcadorTapas.set(self.pantallaRecepcion.recepcion.tapas)
        self.ventana.destroy()

class VentanaFarmabox(Widgets.VentanaHija):
    def __init__(self,ventanaMadre,pantallaRecepcion,ancho,alto,titulo):
        Widgets.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)
        
        self.listaFarmabox = []

         #---Frame Superior---
        # Creo Canvas dentro de Frame
        canvas = Canvas(self.contenedor, bg=Widgets.COLOR_FONDO,borderwidth=0,highlightthickness=0,width=ancho-50,height=self.altoContenedor)
        canvas.pack(side=LEFT,fill=Y,expand=TRUE)

        #Creo Frame dentro de Canvas
        self.frameScroll = Frame(canvas,background=Widgets.COLOR_FONDO)

        #Armo Scroll y Linkeo
        scroll = Scrollbar(self.contenedor,orient=VERTICAL, command=canvas.yview)
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
        botonFinalizar =  Widgets.botonPrincipal(self.frameInferior,'Agregar Farmabox', lambda: self.finalizarCarga(pantallaRecepcion))
        botonFinalizar.pack(side=RIGHT, anchor=SE,pady=10,padx=(0,10))

    def agregarLineaCargaManualFB(self):
        
        entradaFB = Entry(self.frameScroll, font=(Widgets.FUENTE_PRINCIPAL,12), width=11,highlightthickness=2)
        entradaFB.focus_set()
        entradaFB.grid(row=self.fila,column=0,sticky=W,padx=10,pady=5)

        entradaFBControl = Entry(self.frameScroll, font=(Widgets.FUENTE_PRINCIPAL,12), width=11,highlightthickness=2)
        entradaFBControl.grid(row=self.fila,column=1,sticky=W,padx=10,pady=5)

        boton = Widgets.botonMicroNaranja(self.frameScroll,"Validar",lambda: self.compararFarmaboxManual(self,entradaFB, entradaFBControl,boton))
        boton.grid(row=self.fila,column=2,sticky=E,padx=10,pady=5)

        #Activo el enter
        self.ventana.bind('<Return>', lambda event : self.compararFarmaboxManual(self,entradaFB, entradaFBControl,boton))

    def compararFarmaboxManual(self,event,entrada1,entrada2,boton):
        dato1 = entrada1.get()
        dato2 = entrada2.get()

        print(dato1)
        print(dato2)
        if(dato1==dato2 and dato1!='0' and dato1!=''):
            self.listaFarmabox.append(dato1)
            entrada1.destroy()
            entrada2.destroy()
            boton.destroy()
            Label(self.frameScroll, text=str(self.fila + 1)+". "+str(dato1),font=(Widgets.FUENTE_PRINCIPAL, 12),bg=Widgets.COLOR_FONDO).grid(row=self.fila,column=0,sticky=W,padx=15)
            self.fila += 1
            self.agregarLineaCargaManualFB()

    def finalizarCarga(self,pantallaRecepcion):
        for cubeta in self.listaFarmabox:
            pantallaRecepcion.recepcion.agregarFarmabox(pantallaRecepcion,cubeta,cubeta)
        self.ventana.destroy()

class VentanCargaRechazados(Widgets.VentanaHija):
    def __init__(self,ventanaMadre,pantallaRecepcion : PantallaRecepcion ,ancho,alto,titulo):

        Widgets.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)

        self.pantallaRecepcion = pantallaRecepcion
        self.listaRechazados = self.pantallaRecepcion.recepcion.listaRechazados

        self.tabla = Treeview(self.contenedor, column=("#1", "#2", "#3", "#4"), show='headings',height=21,selectmode=BROWSE)
        self.tabla.pack(side=LEFT)

        self.tabla.bind("<Double-1>", self.OnDoubleClick)

        self.tabla.column("#1", anchor=CENTER, width=80)
        self.tabla.heading("#1", text="Lectura 1")
        self.tabla.column("#2", anchor=CENTER, width=80)
        self.tabla.heading("#2", text="Lectura 2")
        self.tabla.column("#3", anchor=CENTER, width=120)
        self.tabla.heading("#3", text="Estado")
        self.tabla.column("#4", anchor=CENTER, width=140)
        self.tabla.heading("#4", text="Motivo Rechazo")

        scrollbar = Scrollbar(self.contenedor, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.tabla.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tabla.yview)

        for row in self.listaRechazados:
            estado = 'NO AGREGABLE'
            motivo = ''
            if row[2] == 1:
                motivo = 'Dato Nulo'            
                estado = 'AGREGAR'
                if(row[3]==1):
                    estado = 'AGREGADO'
            if row[2] == 2:
                motivo = 'No Coinciden'
            if row[2] == 3:
                motivo = 'No Existe'
            if row[2] == 4:
                motivo = 'Repetido'

            self.tabla.insert("", END, values=(row[0],row[1],estado,motivo)  )

        #Botones
        botonFinalizar = Widgets.botonPrincipal(self.frameInferior,'Cerrar',self.ventana.destroy)
        botonFinalizar.pack(side=RIGHT, anchor=SE,pady=10,padx=(0,10))

    def OnDoubleClick(self, event):
        lineaElegida = self.tabla.focus()
        datosLinea = self.tabla.item(lineaElegida,"values")
        estado = datosLinea[2]
        if estado == "AGREGAR":
            #Obtengo Nro Farmabox
            nroFB = datosLinea[0]
            #Obtengo Indice de línea seleccionada
            index = self.tabla.index(lineaElegida)
            #Agrego el farmabox a la Recepción
            self.pantallaRecepcion.recepcion.agregarFarmabox(self.pantallaRecepcion,nroFB,nroFB)
            #Cambio el estado en la lista de Rechazados a AGREGADO
            self.listaRechazados[index][3] = 1
            #Muestro en Pantalla que el farmabox fue agregado
            self.tabla.item(lineaElegida,values=(nroFB, datosLinea[1],'AGREGADO',datosLinea[3]))

class VentanaFinalizarRecepcion(Widgets.VentanaHija):
    def __init__(self,ventanaMadre,recepcion:Recepcion.Recepcion,ancho,alto,titulo):
        Widgets.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)

        Widgets.igualarColumnas(self.contenedor,2)
        self.recepcion = recepcion

        #Texto Fijo
        Label(self.contenedor, text = "Está por generar la siguiente Recepción:",font=('Helvetica 15 underline'),bg='white').grid(row=1,column=0,columnspan=2,sticky=EW,pady=(10,20))
        Label(self.contenedor, text = "Transportista: ",font=(Widgets.FUENTE_PRINCIPAL, 12),bg='white').grid(row=2,column=0,sticky=E)
        Label(self.contenedor, text = "Farmabox Chicos: ",font=(Widgets.FUENTE_PRINCIPAL, 12),bg='white').grid(row=3,column=0,sticky=E)
        Label(self.contenedor, text = "Farmabox Grandes: ",font=(Widgets.FUENTE_PRINCIPAL, 12),bg='white').grid(row=4,column=0,sticky=E)
        Label(self.contenedor, text = "Tapas: ",font=(Widgets.FUENTE_PRINCIPAL, 12),bg='white').grid(row=5,column=0,sticky=E)

        #Texto Dinámico
        Label(self.contenedor, text=recepcion.transportista.nombre,font=(Widgets.FUENTE_PRINCIPAL, 12),background='white').grid(row=2,column=1,sticky=W,padx=10)
        Label(self.contenedor, text=recepcion.cantidadChicos(),font=(Widgets.FUENTE_PRINCIPAL, 12),bg='white').grid(row=3,column=1,sticky=W,padx=10)
        Label(self.contenedor, text=recepcion.cantidadGrandes(),font=(Widgets.FUENTE_PRINCIPAL, 12),bg='white').grid(row=4,column=1,sticky=W,padx=10)
        Label(self.contenedor, text=recepcion.tapas,font=(Widgets.FUENTE_PRINCIPAL, 12),bg='white').grid(row=5,column=1,sticky=W,padx=10)

        #Botones
        botonCancelar = Widgets.botonSecundario(self.frameInferior,'Seguir Recepcionando',self.ventana.destroy)
        botonCancelar.pack(side=LEFT, anchor=SW,pady=10,padx=(10,0))
        botonFinalizar = Widgets.botonPrincipal(self.frameInferior,'Generar Recepción',self.finalizarCargaRecepcion)
        botonFinalizar.pack(side=RIGHT, anchor=SE,pady=10,padx=(0,10))
        
    def finalizarCargaRecepcion(self):
        try:
            idRecepcion = BaseDatos.generarRecepcion(self.recepcion)     
        except:
            messagebox.showinfo(message="Error al conectarse a la base datos")
        else:
            recepcionGenerada = Recepcion.Recepcion.desdeKey(idRecepcion)
            if not Recursos.imprimirTicket(recepcionGenerada):
                ancho = 600
                alto = 230
                VentanaErrorTicket(self.ventanaMadre,ancho,alto,"Error al imprimir el ticket",recepcionGenerada)
            PantallaInicial(self.ventanaMadre)

        self.ventana.destroy()              

class VentanaErrorTicket(Widgets.VentanaHija):
    def __init__(self,ventanaMadre,ancho,alto,titulo,recepcion:Recepcion.Recepcion):
        Widgets.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)

        Widgets.igualarColumnas(self.contenedor,2)

        self.ventana.attributes("-topmost",True)

        Label(self.contenedor, text = "Ocurrió un error al imprimir el ticket de la recepción "+str(recepcion.nroRecepcion),font=(Widgets.FUENTE_PRINCIPAL, 12),bg='white').grid(row=1,column=0,columnspan=2,sticky=EW,pady=(30,20))
        Label(self.contenedor, text = "¿Desea intentar imprimirlo nuevamente?",font=(Widgets.FUENTE_PRINCIPAL, 12),bg='white').grid(row=2,column=0,columnspan=2,sticky=EW,pady=(10,20))

        #Botones
        botonCancelar = Widgets.botonSecundario(self.frameInferior,'Seguir sin Ticket',self.sinTicket)
        botonCancelar.pack(side=LEFT, anchor=SW,pady=10,padx=(10,0))
        botonFinalizar = Widgets.botonPrincipal(self.frameInferior,'Reimprimir Ticket',lambda: self.reimprimirTicket(recepcion))
        botonFinalizar.pack(side=RIGHT, anchor=SE,pady=10,padx=(0,10))
    
    def reimprimirTicket(self,recepcion):
        if not Recursos.imprimirTicket(recepcion):
            ancho = 600
            alto = 230
            VentanaErrorTicket(self.ventanaMadre,ancho,alto,"Error al imprimir el ticket",recepcion)           
        self.ventana.destroy()  

    def sinTicket(self):
        self.ventana.destroy()


#Ventanas Emergentes Consultas
class VentanaRecepciones(Widgets.VentanaHija):
    def __init__(self,ventanaMadre,ancho,alto,titulo,fechaD,fechaH,radio,transp,empresa,estado):

        Widgets.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)
        
        self.pantallaConsulta = ventanaMadre.pantallaActiva

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

        estadoText = estado[1][estado[0]][1]

        recepciones = BaseDatos.buscarRecepciones(fechaD,fechaH,codRadio,nroTransp,nroEmpresa,estado[0])

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

        Label(frameTopIzquierdo, text="Fecha Desde :  "+str(fechaD)[0:19],background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)
        Label(frameTopIzquierdo, text="Fecha Hasta :  "+str(fechaH)[0:19],background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)
        Label(frameTopIzquierdo, text="Estado :  "+estadoText,background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)


        #---Frame Tabla---
        frameTabla = Frame(self.contenedor,bg=Widgets.COLOR_FONDO,height=self.altoContenedor-altoTop) 
        frameTabla.pack(side = BOTTOM, fill = BOTH, expand = TRUE, padx=Widgets.MARGEN_X)
        frameTabla.propagate(False)

        self.tabla = Treeview(frameTabla, column=("#1", "#2", "#3","#4","#5","#6","#7","#8"), show='headings',height=21,selectmode=BROWSE)
        self.tabla.pack(side=LEFT)

        #Bindeo doble click a función
        self.tabla.bind("<Double-1>", self.OnDoubleClick)

        self.tabla.column("#1", anchor=CENTER, width=78)
        self.tabla.heading("#1", text="Recepción")
        self.tabla.column("#2", anchor=CENTER, width=140)
        self.tabla.heading("#2", text="Fecha")
        self.tabla.column("#3", anchor=CENTER, width=70)
        self.tabla.heading("#3", text="Radio")
        self.tabla.column("#4", anchor=CENTER, width=185)
        self.tabla.heading("#4", text="Transportista")
        self.tabla.column("#5", anchor=CENTER, width=185)
        self.tabla.heading("#5", text="Empresa")
        self.tabla.column("#6", anchor=CENTER, width=60)
        self.tabla.heading("#6", text="Fbox")
        self.tabla.column("#7", anchor=CENTER, width=60)
        self.tabla.heading("#7", text="Tapas")
        self.tabla.column("#8", anchor=CENTER, width=60)
        self.tabla.heading("#8", text="Proces.")

        scrollbar = Scrollbar(frameTabla, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.tabla.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tabla.yview)

        for row in recepciones:
            self.tabla.insert("", END, values=(row[0],row[1][0:19],row[2],row[3],row[4],row[5],row[6],row[7])     )

        #Botones
        botonCSV = Widgets.botonPrincipal(self.frameInferior,'Generar CSV',lambda :self.guardarCSV(recepciones))
        botonCSV.pack(side=LEFT, anchor=SW,pady=10,padx=(10,0))
        botonRecepcionesConFarmabox = Widgets.botonPrincipal(self.frameInferior,'Generar CSV con Farmabox',lambda :self.generarCSVconFB(recepciones))
        botonRecepcionesConFarmabox.pack(side=LEFT, anchor=CENTER,pady=10,padx=5)
        botonFinalizar = Widgets.botonPrincipal(self.frameInferior,'Cerrar',self.ventana.destroy)
        botonFinalizar.pack(side=RIGHT, anchor=SE,pady=10,padx=(0,10))

    def guardarCSV(self,recepciones):
        archivo = filedialog.asksaveasfile(mode ='w',title='Exportar a CSV',filetypes= [("Arhcivo CSV","*.csv")], defaultextension='.csv')
        titulos = ['Número Recepción','Fecha','Radio','Transportista','Empresa','Cantidad Farmabox','Cantidad Tapas','Procesado']
        with open(archivo.name, 'w+', newline ='',) as archivo:    
            escritor = csv.writer(archivo,delimiter = ";")
            escritor.writerow(titulos)
            escritor.writerows(recepciones)

    def generarCSVconFB(self,recepciones):
        archivo = filedialog.asksaveasfile(mode ='w',title='Exportar a CSV',filetypes= [("Arhcivo CSV","*.csv")], defaultextension='.csv')
        titulos = ['Número Recepción','Fecha','Radio','Transportista','Empresa','Número Farmabox','Tapas']
        recepcionesConFB = BaseDatos.agregarFamaboxToRecepciones(recepciones)
        with open(archivo.name, 'w+', newline ='',) as archivo:    
            escritor = csv.writer(archivo,delimiter = ";")
            escritor.writerow(titulos)
            escritor.writerows(recepcionesConFB)
            
    def OnDoubleClick(self, event):
        item = self.tabla.selection()[0]
        nroRecepcion =  self.tabla.item(item,"values")[0]
        self.pantallaConsulta.buscarRecepcion(nroRecepcion)
         
class VentanaDetalleRecepcion(Widgets.VentanaHija):
    def __init__(self,ventanaMadre,ancho,alto,titulo,recepcion):

        Widgets.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)
         
        self.pantallaConsulta = ventanaMadre.pantallaActiva

        nroRecepcion = recepcion[0][0]
        codRadio = recepcion[0][2]
        nomTransportista = recepcion[0][3]
        nomEmpresa = recepcion[0][4]
        fecha = recepcion[0][1]
        tapas = recepcion[0][6]
        procesado = recepcion[0][7]
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

        Label(frameTopIzquierdo, text="Fecha :  "+str(fecha)[0:19],background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)
        Label(frameTopIzquierdo, text="Procesado :  "+textoProcesado,background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)


        #---Frame Tabla---
        frameTabla = Frame(self.contenedor,bg=Widgets.COLOR_FONDO,height=self.altoContenedor-altoTop-altoTotales) 
        frameTabla.pack(side = TOP, fill = BOTH, expand = TRUE, padx=Widgets.MARGEN_X)
        frameTabla.propagate(False)

        self.tabla = Treeview(frameTabla, column=("#1","#2"), show='headings',height=21,selectmode=BROWSE)
        self.tabla.pack(side=LEFT)

        self.tabla.bind("<Double-1>", self.OnDoubleClick)

        self.tabla.column("#1", anchor=CENTER, width=300)
        self.tabla.heading("#1", text="Número de Farmabox")
        self.tabla.column("#2", anchor=CENTER, width=290)
        self.tabla.heading("#2", text="Tamaño Farmabox")

        scrollbar = Scrollbar(frameTabla, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.tabla.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tabla.yview)
        cantidadCH = 0
        cantidadGR = 0

        recepcionConTamanio = []

        if recepcion is not None:
            for row in recepcion:
                nueva = list(row)
                if Recursos.esCubetaChica(row[5]):
                    nueva.append("Chico")
                    cantidadCH += 1
                else:
                    nueva.append("Grande")
                    cantidadGR +=1
                recepcionConTamanio.append(nueva)
                self.tabla.insert("",END, values=(nueva[5],nueva[8]) )  

        #---Frame Totales---
        frameTotales = Frame(self.contenedor,bg=Widgets.COLOR_FONDO,height=altoTotales) 
        frameTotales.pack(side = BOTTOM, fill = BOTH, expand = TRUE, padx=Widgets.MARGEN_X)
        frameTotales.propagate(False)

        #Textos
        Label(frameTotales, text="Total Chicos: "+str(cantidadCH),font=(Widgets.FUENTE_PRINCIPAL, 12),bg=Widgets.COLOR_FONDO).grid(row=0,column=0,sticky=EW,pady=5, padx=(0,30))
        Label(frameTotales, text="Total Grandes: "+str(cantidadGR),font=(Widgets.FUENTE_PRINCIPAL, 12),bg=Widgets.COLOR_FONDO).grid(row=0,column=1,sticky=EW,pady=5,padx=30)
        Label(frameTotales, text="Tapas: "+str(tapas),font=(Widgets.FUENTE_PRINCIPAL, 12),bg=Widgets.COLOR_FONDO).grid(row=0,column=2,sticky=EW,pady=5,padx=30)

        #Botones
        botonCSV = Widgets.botonPrincipal(self.frameInferior,'Generar CSV',lambda: self.guardarCSV(recepcionConTamanio))
        botonCSV.pack(side=LEFT, anchor=SW,pady=10,padx=(10,0))
        botonTicket = Widgets.botonPrincipal(self.frameInferior,'Imprimir Ticket',lambda: self.reimprimirTicket(recepcion))
        botonTicket.pack(side=LEFT, anchor=CENTER,pady=10,padx=5)
        botonFinalizar = Widgets.botonPrincipal(self.frameInferior,'Cerrar',self.ventana.destroy)
        botonFinalizar.pack(side=RIGHT, anchor=SE,pady=10,padx=(0,10))

    def guardarCSV(self,recepcion):
        archivo = filedialog.asksaveasfile(mode ='w',title='Exportar a CSV',filetypes= [("Arhcivo CSV","*.csv")], defaultextension='.csv')
        titulos = ['Número Recepción','Fecha','Radio','Transportista','Empresa','Número Farmabox','Cantidad Tapas','Procesado', 'Tamaño Farmabox']
        with open(archivo.name, 'w+', newline ='',) as archivo:    
            escritor = csv.writer(archivo,delimiter = ";")
            escritor.writerow(titulos)
            escritor.writerows(recepcion)

    def reimprimirTicket(self,recepcion):
        recepcionTicket = Recepcion.Recepcion.desdeKey(recepcion[0][0])
        if not Recursos.imprimirTicket(recepcionTicket):
            ancho = 600
            alto = 230
            VentanaErrorTicket(self.ventanaMadre,ancho,alto,"Error al imprimir el ticket",recepcionTicket)           
    
    def OnDoubleClick(self, event):
        item = self.tabla.selection()[0]
        nroFarmabox =  self.tabla.item(item,"values")[0]
        self.pantallaConsulta.buscarFarmabox(nroFarmabox,'','')

class VentanaCalendario():
    def __init__(self,ventanaMadre,fechaEntry):
        
        self.fechaEntry = fechaEntry
        self.ventana = Toplevel(ventanaMadre)

        rutaIcono = Recursos.rutaArchivo('Imagenes/Pantuflas.ico')

        if os.path.exists(rutaIcono):
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
    
class VentanaKardexFarmabox(Widgets.VentanaHija):
    def __init__(self,ventanaMadre,ancho,alto,titulo,tuplaBusquedaMovimientos):

        Widgets.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)

        self.pantallaConsulta = ventanaMadre.pantallaActiva

        movimientos = tuplaBusquedaMovimientos[0]
        fechaD = tuplaBusquedaMovimientos[1]
        fechaH = tuplaBusquedaMovimientos[2]
        nroFarmabox = movimientos[0][0]

        #---Frame TOP---
        altoTop = 50
        frameTop = Frame(self.contenedor,bg=Widgets.COLOR_FONDO,height=altoTop) 
        frameTop.pack(side = TOP, fill = X, expand = TRUE, padx=Widgets.MARGEN_X)
        frameTop.propagate(False)

        frameTopDerecho = Frame(frameTop,bg=Widgets.COLOR_FONDO,height=altoTop,width=(ancho/2)-Widgets.MARGEN_X)
        frameTopDerecho.pack(side = LEFT, fill = BOTH, expand = TRUE)
        frameTopIzquierdo = Frame(frameTop,bg=Widgets.COLOR_FONDO,height=altoTop,width=(ancho/2)-Widgets.MARGEN_X)
        frameTopIzquierdo.pack(side = RIGHT, fill = BOTH, expand = TRUE)

        Label(frameTopDerecho, text="Farmabox Número : "+str(nroFarmabox),font=(Widgets.FUENTE_PRINCIPAL, 15),background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)

        Label(frameTopIzquierdo, text="Fecha Desde :  "+str(fechaD)[0:19],background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)
        Label(frameTopIzquierdo, text="Fecha Hasta :  "+str(fechaH)[0:19],background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)


        #---Frame Tabla---
        frameTabla = Frame(self.contenedor,bg=Widgets.COLOR_FONDO,height=self.altoContenedor-altoTop) 
        frameTabla.pack(side = BOTTOM, fill = BOTH, expand = TRUE, padx=Widgets.MARGEN_X)
        frameTabla.propagate(False)

        self.tabla = Treeview(frameTabla, column=("#1", "#2", "#3","#4","#5"), show='headings',height=21,selectmode=BROWSE)
        self.tabla.pack(side=LEFT)

        self.tabla.bind("<Double-1>", self.OnDoubleClick)

        self.tabla.column("#1", anchor=CENTER, width=140)
        self.tabla.heading("#1", text="Fecha")
        self.tabla.column("#2", anchor=CENTER, width=140)
        self.tabla.heading("#2", text="Tipo Movimiento")
        self.tabla.column("#3", anchor=CENTER, width=140)
        self.tabla.heading("#3", text="Número Recepción")
        self.tabla.column("#4", anchor=CENTER, width=140)
        self.tabla.heading("#4", text="Número Modificación")
        self.tabla.column("#5", anchor=CENTER, width=80)
        self.tabla.heading("#5", text="Radio")

        scrollbar = Scrollbar(frameTabla, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.tabla.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tabla.yview)
    
        for row in movimientos:
            self.tabla.insert("", END, values=(row[1][0:19],row[2],row[3],row[4],row[5]) )

        #Botones
        botonCSV = Widgets.botonPrincipal(self.frameInferior,'Generar CSV',lambda: self.guardarCSV(movimientos))
        botonCSV.pack(side=LEFT, anchor=SW,pady=10,padx=(10,0))
        #botonExcel = Widgets.botonPrincipal(self.frameInferior,'Generar Excel',self.ventana.destroy)
        #botonExcel.pack(side=LEFT, anchor=CENTER,pady=10,padx=5)
        botonFinalizar = Widgets.botonPrincipal(self.frameInferior,'Cerrar',self.ventana.destroy)
        botonFinalizar.pack(side=RIGHT, anchor=SE,pady=10,padx=(0,10))
         
    def guardarCSV(self,movimientos):
        archivo = filedialog.asksaveasfile(mode ='w',title='Exportar a CSV',filetypes= [("Arhcivo CSV","*.csv")], defaultextension='.csv')
        titulos = ['Número Farmabox','Fecha','Tipo Movimiento','Número Recepción','Número Modificación','Radio']
        with open(archivo.name, 'w+', newline ='',) as archivo:    
            escritor = csv.writer(archivo,delimiter = ";")
            escritor.writerow(titulos)
            escritor.writerows(movimientos)

    def OnDoubleClick(self, event):
        item = self.tabla.selection()[0]
        tipoMovimiento = self.tabla.item(item,"values")[1]
        if tipoMovimiento == "RECEPCIÓN":
            self.pantallaConsulta.buscarRecepcion(self.tabla.item(item,"values")[2])
        else:
            self.pantallaConsulta.buscarModificacion(self.tabla.item(item,"values")[3])

class VentanaModificaciones(Widgets.VentanaHija):
    def __init__(self,ventanaMadre,ancho,alto,titulo,fechaD,fechaH,tuplaTipos):

        Widgets.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)

        lineaSeleccionada = tuplaTipos[1][tuplaTipos[0]]
        motivoCod = lineaSeleccionada[0]
        motivoTipo = lineaSeleccionada[1]
    
        modificaciones = BaseDatos.buscarModificaciones(fechaD,fechaH,motivoCod)


        #---Frame TOP---
        altoTop = 64
        frameTop = Frame(self.contenedor,bg=Widgets.COLOR_FONDO,height=altoTop) 
        frameTop.pack(side = TOP, fill = X, expand = TRUE, padx=Widgets.MARGEN_X)
        frameTop.propagate(False)
        frameTopDerecho = Frame(frameTop,bg=Widgets.COLOR_FONDO,height=altoTop,width=(ancho/2)-Widgets.MARGEN_X)
        frameTopDerecho.pack(side = LEFT, fill = BOTH, expand = TRUE)
        frameTopIzquierdo = Frame(frameTop,bg=Widgets.COLOR_FONDO,height=altoTop,width=(ancho/2)-Widgets.MARGEN_X)
        frameTopIzquierdo.pack(side = RIGHT, fill = BOTH, expand = TRUE)

        Label(frameTopDerecho, text="Motivo : "+motivoTipo,font=(Widgets.FUENTE_PRINCIPAL, 9),background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)

        Label(frameTopIzquierdo, text="Fecha Desde :  "+str(fechaD)[0:19],background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)
        Label(frameTopIzquierdo, text="Fecha Hasta :  "+str(fechaH)[0:19],background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)


        #---Frame Tabla---
        frameTabla = Frame(self.contenedor,bg=Widgets.COLOR_FONDO,height=self.altoContenedor-altoTop) 
        frameTabla.pack(side = BOTTOM, fill = BOTH, expand = TRUE, padx=Widgets.MARGEN_X)
        frameTabla.propagate(False)

        self.tabla = Treeview(frameTabla, column=("#1", "#2", "#3"), show='headings',height=21,selectmode=BROWSE)
        self.tabla.pack(side=LEFT)

        self.tabla.column("#1", anchor=CENTER, width=100)
        self.tabla.heading("#1", text="Número Modificación")
        self.tabla.column("#2", anchor=CENTER, width=140)
        self.tabla.heading("#2", text="Tipo Modificación")
        self.tabla.column("#3", anchor=CENTER, width=200)
        self.tabla.heading("#3", text="Fecha")

        scrollbar = Scrollbar(frameTabla, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.tabla.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tabla.yview)

        for row in modificaciones:
            self.tabla.insert("", END, values=(row[0],row[1],row[2][0:19])  )

        #Botones
        botonCSV = Widgets.botonPrincipal(self.frameInferior,'Generar CSV',lambda :self.guardarCSV(modificaciones))
        botonCSV.pack(side=LEFT, anchor=SW,pady=10,padx=(10,0))
        botonFinalizar = Widgets.botonPrincipal(self.frameInferior,'Cerrar',self.ventana.destroy)
        botonFinalizar.pack(side=RIGHT, anchor=SE,pady=10,padx=(0,10))

class VentanRechazados(Widgets.VentanaHija):
    def __init__(self,ventanaMadre,ancho,alto,titulo,fechaD,fechaH,tuplaMotivo,nroRecepcion):

        Widgets.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)

        lineaSeleccionada = tuplaMotivo[1][tuplaMotivo[0]]
        motivoCod = lineaSeleccionada[0]
        motivoTipo = lineaSeleccionada[1]


        rechazos = BaseDatos.buscarRechazos(fechaD,fechaH,motivoCod,nroRecepcion)

        #---Frame TOP---
        altoTop = 64
        frameTop = Frame(self.contenedor,bg=Widgets.COLOR_FONDO,height=altoTop) 
        frameTop.pack(side = TOP, fill = X, expand = TRUE, padx=Widgets.MARGEN_X)
        frameTop.propagate(False)
        frameTopDerecho = Frame(frameTop,bg=Widgets.COLOR_FONDO,height=altoTop,width=(ancho/2)-Widgets.MARGEN_X)
        frameTopDerecho.pack(side = LEFT, fill = BOTH, expand = TRUE)
        frameTopIzquierdo = Frame(frameTop,bg=Widgets.COLOR_FONDO,height=altoTop,width=(ancho/2)-Widgets.MARGEN_X)
        frameTopIzquierdo.pack(side = RIGHT, fill = BOTH, expand = TRUE)

        Label(frameTopDerecho, text="Motivo de Rechazo : "+motivoTipo,font=(Widgets.FUENTE_PRINCIPAL, 9),background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)
        Label(frameTopDerecho, text="Número de Recepción : "+str(nroRecepcion),font=(Widgets.FUENTE_PRINCIPAL, 9),background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)

        Label(frameTopIzquierdo, text="Fecha Desde :  "+str(fechaD)[0:19],background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)
        Label(frameTopIzquierdo, text="Fecha Hasta :  "+str(fechaH)[0:19],background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)



         #---Frame Tabla---
        frameTabla = Frame(self.contenedor,bg=Widgets.COLOR_FONDO,height=self.altoContenedor-altoTop) 
        frameTabla.pack(side = BOTTOM, fill = BOTH, expand = TRUE, padx=Widgets.MARGEN_X)
        frameTabla.propagate(False)

        self.tabla = Treeview(frameTabla, column=("#1", "#2", "#3","#4","#5"), show='headings',height=21,selectmode=BROWSE)
        self.tabla.pack(side=LEFT)

        self.tabla.column("#1", anchor=CENTER, width=150)
        self.tabla.heading("#1", text="Fecha Recepción")
        self.tabla.column("#2", anchor=CENTER, width=150)
        self.tabla.heading("#2", text="Número de Recepción")
        self.tabla.column("#3", anchor=CENTER, width=100)
        self.tabla.heading("#3", text="Lectura 1")
        self.tabla.column("#4", anchor=CENTER, width=100)
        self.tabla.heading("#4", text="Lectura 2")
        self.tabla.column("#5", anchor=CENTER, width=200)
        self.tabla.heading("#5", text="Motivo Rechazo")

        scrollbar = Scrollbar(frameTabla, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.tabla.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tabla.yview)

        for row in rechazos:
            self.tabla.insert("", END, values=(row[0][0:19],row[1],row[2],row[3],row[4])  )

        #Botones
        botonCSV = Widgets.botonPrincipal(self.frameInferior,'Generar CSV',lambda :self.guardarCSV(rechazos))
        botonCSV.pack(side=LEFT, anchor=SW,pady=10,padx=(10,0))
        botonFinalizar = Widgets.botonPrincipal(self.frameInferior,'Cerrar',self.ventana.destroy)
        botonFinalizar.pack(side=RIGHT, anchor=SE,pady=10,padx=(0,10))

    def guardarCSV(self,rechazos):
        archivo = filedialog.asksaveasfile(mode ='w',title='Exportar a CSV',filetypes= [("Arhcivo CSV","*.csv")], defaultextension='.csv')
        titulos = ['Fecha Recepción','Número de Recepción','Lectura 1','Lectura 2','Motivo Rechazo']
        with open(archivo.name, 'w+', newline ='',) as archivo:    
            escritor = csv.writer(archivo,delimiter = ";")
            escritor.writerow(titulos)
            escritor.writerows(rechazos)

class VentanaDetallesModificacion(Widgets.VentanaHija):
    def __init__(self,ventanaMadre,ancho,alto,titulo,modificacion):

        Widgets.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)

        self.pantallaConsulta = ventanaMadre.pantallaActiva

        nroModificacion = modificacion[0][0]
        fecha = modificacion[0][1]
        tipo = modificacion[0][2]
        altoTop = 64
   
        #---Frame TOP---
        frameTop = Frame(self.contenedor,bg=Widgets.COLOR_FONDO,height=altoTop) 
        frameTop.pack(side = TOP, fill = X, expand = TRUE, padx=Widgets.MARGEN_X)
        frameTop.propagate(False)
        frameTopDerecho = Frame(frameTop,bg=Widgets.COLOR_FONDO,height=altoTop,width=(ancho/2)-Widgets.MARGEN_X)
        frameTopDerecho.pack(side = LEFT, fill = BOTH, expand = TRUE)
        frameTopIzquierdo = Frame(frameTop,bg=Widgets.COLOR_FONDO,height=altoTop,width=(ancho/2)-Widgets.MARGEN_X)
        frameTopIzquierdo.pack(side = RIGHT, fill = BOTH, expand = TRUE)

        Label(frameTopDerecho, text="Modificacion : "+str(nroModificacion),font=(Widgets.FUENTE_PRINCIPAL, 9),background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)
        Label(frameTopDerecho, text="Tipo : "+tipo,font=(Widgets.FUENTE_PRINCIPAL, 9),background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)
        
        Label(frameTopIzquierdo, text="Fecha :  "+str(fecha)[0:19],background=Widgets.COLOR_FONDO).pack(side=TOP,anchor=NW)
       

        #---Frame Tabla---
        frameTabla = Frame(self.contenedor,bg=Widgets.COLOR_FONDO,height=self.altoContenedor-altoTop) 
        frameTabla.pack(side = TOP, fill = BOTH, expand = TRUE, padx=Widgets.MARGEN_X)
        frameTabla.propagate(False)


        self.tabla = Treeview(frameTabla, column=("#1","#2"), show='headings',height=21,selectmode=BROWSE)
        self.tabla.pack(side=LEFT)

        self.tabla.bind("<Double-1>", self.OnDoubleClick)

        self.tabla.column("#1", anchor=CENTER, width=300)
        self.tabla.heading("#1", text="Número de Farmabox")
        self.tabla.column("#2", anchor=CENTER, width=290)
        self.tabla.heading("#2", text="Tamaño Farmabox")

        scrollbar = Scrollbar(frameTabla, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.tabla.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tabla.yview)

        modificacionConTamanio = []

        if modificacion is not None:
            for row in modificacion:
                nueva = list(row)
                if Recursos.esCubetaChica(row[3]):
                    nueva.append("Chico")
                else:
                    nueva.append("Grande")
                modificacionConTamanio.append(nueva)
                self.tabla.insert("",END, values=(nueva[3],nueva[4]) )  

        #Botones
        botonCSV = Widgets.botonPrincipal(self.frameInferior,'Generar CSV',lambda: self.guardarCSV(modificacionConTamanio))
        botonCSV.pack(side=LEFT, anchor=SW,pady=10,padx=(10,0))
        #botonExcel = Widgets.botonPrincipal(self.frameInferior,'Generar Excel',self.ventana.destroy)
        #botonExcel.pack(side=LEFT, anchor=CENTER,pady=10,padx=5)
        botonFinalizar = Widgets.botonPrincipal(self.frameInferior,'Cerrar',self.ventana.destroy)
        botonFinalizar.pack(side=RIGHT, anchor=SE,pady=10,padx=(0,10))

    def guardarCSV(self,modificacion):
        archivo = filedialog.asksaveasfile(mode ='w',title='Exportar a CSV',filetypes= [("Arhcivo CSV","*.csv")], defaultextension='.csv')
        titulos = ['Número Modificación','Fecha','Tipo','Número Farmabox','Tamaño Farmabox']
        with open(archivo.name, 'w+', newline ='',) as archivo:    
            escritor = csv.writer(archivo,delimiter = ";")
            escritor.writerow(titulos)
            escritor.writerows(modificacion)
    
    def OnDoubleClick(self, event):
        item = self.tabla.selection()[0]
        nroFarmabox =  self.tabla.item(item,"values")[0]
        self.pantallaConsulta.buscarFarmabox(nroFarmabox,'','')


#Ventanas Emergentes Administración
class VentanaAdvierteGuardado(Widgets.VentanaHija):
    def __init__(self,ventanaMadre,ancho,alto, titulo, datosAGuardar,command):

        Widgets.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)


        #Texto
        Label(self.contenedor, text = "¿Está seguro que quiere agregar los siguientes elementos a la base?",font=(Widgets.FUENTE_PRINCIPAL, 14),bg='white').grid(row=0,column=0,pady=28,padx=15,sticky=EW)
        
        row = 1
        for dato in datosAGuardar:
            Label(self.contenedor, text = dato,font=(Widgets.FUENTE_PRINCIPAL, 12),bg='white').grid(row=row,column=0,pady=5,padx=15,sticky=W)
            row += 1

        #Botones
        botonCancelar = Widgets.botonSecundario(self.frameInferior,'Cancelar',self.ventana.destroy)
        botonCancelar.pack(side=LEFT, anchor=SW,pady=10,padx=(10,0))
        botonFinalizar =  Widgets.botonPrincipal(self.frameInferior,'Guardar',lambda: self.guardar(command))
        botonFinalizar.pack(side=RIGHT, anchor=SE,pady=10,padx=(0,10))

    def guardar(self, command):

        registro = command

        for widgets in self.contenedor.winfo_children():
            widgets.destroy()
        for widgets in self.frameInferior.winfo_children():
            widgets.destroy()

        if registro is None:
            Label(self.contenedor, text = "No se pudo guardar el registro",font=(Widgets.FUENTE_PRINCIPAL, 14),bg='white').grid(row=0,column=0,pady=28,padx=15,sticky=EW)
        else:
            Label(self.contenedor, text = "Se guardó el registro con el id "+str(registro),font=(Widgets.FUENTE_PRINCIPAL, 13),bg='white').grid(row=0,column=0,pady=28,padx=15,sticky=EW)

        botonFinalizar =  Widgets.botonPrincipal(self.frameInferior,'Cerrar',self.ventana.destroy)
        botonFinalizar.pack(side=RIGHT, anchor=SE,pady=10,padx=(0,10))

class VentanaPassword(Widgets.VentanaHija):
    def __init__(self,ventanaMadre,ancho,alto,titulo):
        Widgets.VentanaHija.__init__(self,ventanaMadre,ancho,alto,titulo)

        #Texto
        Label(self.contenedor, text = "Contraseña",font=(Widgets.FUENTE_PRINCIPAL, 15),bg='white').grid(row=1,column=0,pady=28,padx=15,sticky=E)

        #Entrada de Texto
        self.entradaPassword = Entry(self.contenedor, show="*",font=(Widgets.FUENTE_PRINCIPAL,15), width=18,highlightthickness=2)
        self.entradaPassword.focus_set()
        self.entradaPassword.grid(row=1,column=1,sticky=W)
        
        #Botones
        botonCancelar = Widgets.botonSecundario(self.frameInferior,'Cancelar',self.ventana.destroy)
        botonCancelar.pack(side=LEFT, anchor=SW,pady=10,padx=(10,0))
        botonFinalizar =  Widgets.botonPrincipal(self.frameInferior,'Ingresar',lambda: self.evaluarPass(self))
        botonFinalizar.pack(side=RIGHT, anchor=SE,pady=10,padx=(0,10))
        
        self.ventana.attributes("-topmost",True)
        self.ventana.bind('<Return>', lambda event: self.evaluarPass(self))

    def evaluarPass(self,event):
        if(self.entradaPassword.get()==Recursos.contrasena):
            PantallaAdministracion(self.ventanaMadre)
            self.ventana.destroy()
        else:
            messagebox.showinfo(message="Contraseña Incorrecta", title="Contraseña Incorrecta")
            self.entradaPassword.delete(0, 'end')
        
