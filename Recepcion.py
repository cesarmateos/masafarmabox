from winsound import Beep
from threading import Thread

import Recursos
import BaseDatos

#Motivos Rechazo
FB_DATO_NULO = 1
FB_NO_COINCIDEN = 2
FB_NO_EXISTE = 3
FB_REPETIDO = 4

   
class Transportista:
    def __init__(self,tuplaTransportistaQuery) -> None:
        self.numero = tuplaTransportistaQuery[0]
        self.nombre = tuplaTransportistaQuery[1]
        self.radio = Radio(tuplaTransportistaQuery[2],tuplaTransportistaQuery[3])
        self.empresa = tuplaTransportistaQuery[4]
        self.estado = tuplaTransportistaQuery[5]
    
    @classmethod
    def desdeKey(cls,nroTransportista: int):
        resultadoQuery = BaseDatos.encontrarTransportista(nroTransportista)
        return cls(resultadoQuery)
    
class Radio:
    def __init__(self,codigo,descripcion):
        self.codigo = codigo
        self.descripcion = descripcion

    @classmethod
    def desdeKey(cls,codigo):
        resultadoQuery = BaseDatos.buscarRadio(codigo)
        codigo = resultadoQuery[0][0]
        descpricion = resultadoQuery[0][1] 
        return cls(codigo,descpricion)
    @classmethod
    def desdeResultadoQuery(cls,resultadoQuery):
        codigo = resultadoQuery[0][0]
        descpricion = resultadoQuery[0][1] 
        return cls(codigo,descpricion)

class Recepcion:
    def __init__(self,transportista: Transportista) -> None:
        self.transportista = transportista
        self.listaFarmaboxChico = []
        self.listaFarmaboxGrande = []
        self.listaRechazados = []
        self.tapas = 0
        self.rechazados = 0
        self.nroRecepcion = None
        self.radio =  transportista.radio
        self.fecha = None

    @classmethod
    def desdeKey(cls,nroRecepcion: int):
        #OJO - NO TIENE EN CUENTA QUE PASA SI LA QUERY ESTA VACIA

        #Obtengo los datos de la recepcion de la base de datos
        recepcionQuery = BaseDatos.buscarRecepcionParaArmadoDeClase(nroRecepcion)

        #Extraigo el nro Transportista
        nroTransportista = recepcionQuery[0][3]

        #Instancio el objeto Transportista
        transportista = Transportista.desdeKey(nroTransportista)

        #Instancio Objeto Recepcion
        recepcion = cls(transportista)
    
        #Lleno los atributos de la Recepción
        recepcion.nroRecepcion = recepcionQuery[0][0]   
        recepcion.setFecha(recepcionQuery[0][1])
        recepcion.radio = Radio.desdeKey(recepcionQuery[0][2])
        recepcion.tapas = recepcionQuery[0][5]
        
        for fila in recepcionQuery:
            nroFarmabox = fila[4]
            if Recursos.esCubetaChica(nroFarmabox):
                recepcion.listaFarmaboxChico.append(nroFarmabox)
            else:
                recepcion.listaFarmaboxGrande.append(nroFarmabox)

        return recepcion
    
    @classmethod
    def desdeResultadoQuery(cls,recepcionQuery):
        #OJO - NO TIENE EN CUENTA QUE PASA SI LA QUERY ESTA VACIA

        #Extraigo el nro Transportista
        nroTransportista = recepcionQuery[0][3]

        #Instancio el objeto Transportista
        transportista = Transportista.desdeKey(nroTransportista)

        #Instancio Objeto Recepcion
        recepcion = cls(transportista)
    
        #Lleno los atributos de la Recepción
        recepcion.nroRecepcion = recepcionQuery[0][0]   
        recepcion.fecha = recepcionQuery[0][1]
        recepcion.radio = Radio.desdeKey(recepcionQuery[0][2])
        recepcion.tapas = recepcionQuery[0][5]
        
        for fila in recepcion:
            nroFarmabox = fila[4]
            if Recursos.esCubetaChica(nroFarmabox):
                recepcion.listaFarmaboxChico.append(nroFarmabox)
            else:
                recepcion.listaFarmaboxGrande.append(nroFarmabox)

        return recepcion
    
    def agregarFarmabox(self, pantallaRecepcion, dato1,dato2):
        
        fbox1 = int(dato1)
        fbox2 = int(dato2)

        if fbox1 == 0 or fbox2 == 0:
            self.farmaboxRechazado(pantallaRecepcion,fbox1,fbox2,FB_DATO_NULO)
        elif fbox1 != fbox2:
            self.farmaboxRechazado(pantallaRecepcion,fbox1,fbox2,FB_NO_COINCIDEN)
        elif self.existeFB(fbox1):
            if Recursos.esCubetaChica(fbox1):
                if fbox1 in self.listaFarmaboxChico:
                    self.farmaboxRechazado(pantallaRecepcion,fbox1,fbox2,FB_REPETIDO)
                else:
                    self.listaFarmaboxChico.append(fbox1)
                    pantallaRecepcion.nuevoFarmaboxChico(dato1,self.cantidadChicos())
            else:
                if fbox1 in self.listaFarmaboxGrande:
                    self.farmaboxRechazado(pantallaRecepcion,fbox1,fbox2,FB_REPETIDO)
                else:
                    self.listaFarmaboxGrande.append(fbox1)
                    pantallaRecepcion.nuevoFarmaboxGrande(dato1,self.cantidadGrandes())
        else:
            self.farmaboxRechazado(pantallaRecepcion,fbox1,fbox2,FB_NO_EXISTE)

    def agregarTapas(self,tapas):
        self.tapas = tapas

    def farmaboxRechazado(self,pantallaRecepcion,nroFBA, nroFBB, motivo: int):
        self.rechazados += 1
        pantallaRecepcion.nuevoRechazado()
        nuevoRegistroRechazo = []
        nuevoRegistroRechazo.append(nroFBA)
        nuevoRegistroRechazo.append(nroFBB)
        nuevoRegistroRechazo.append(motivo)
        nuevoRegistroRechazo.append(0)
        self.listaRechazados.append(nuevoRegistroRechazo)
        hilo = Thread(target=self.sonido)
        hilo.daemon = True
        hilo.start()

    def cantidadChicos(self):
        return len(self.listaFarmaboxChico)
    
    def cantidadGrandes(self):
        return len(self.listaFarmaboxGrande)
    
    def setNroRecepcion(self, nroRecepcion : int):
        self.nroRecepcion = nroRecepcion
    
    def setFecha(self,fecha):
        self.fecha = fecha

    def chicosOrdenados(self):
        self.listaFarmaboxChico.sort()
        return self.listaFarmaboxChico

    def grandesOrdenados(self):
        self.listaFarmaboxGrande.sort()
        return self.listaFarmaboxGrande

    def existeFB(self,nroFB):
        farmabox = BaseDatos.encontrarFarmabox(nroFB)
        if farmabox == None :
            return False
        return True

    def sonido(self):
        Beep(900,100)
        Beep(700,400)
