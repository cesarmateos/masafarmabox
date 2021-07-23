from winsound import Beep
from threading import Thread

import Recursos
import BaseDatos

#Motivos Rechazo
FB_DATO_NULO = 1
FB_NO_COINCIDEN = 2
FB_NO_EXISTE = 3
FB_REPETIDO = 4

class Recepcion:
    def __init__(self,transportista) -> None:
        self.transportista = transportista
        self.listaFarmaboxChico = []
        self.listaFarmaboxGrande = []
        self.listaRechazados = []
        self.tapas = 0
        self.rechazados = 0
    
    def agregarFarmabox(self, ventana, dato1,dato2):
        
        fbox1 = int(dato1)
        fbox2 = int(dato2)

        if fbox1 == 0 or fbox2 == 0:
            self.farmaboxRechazado(ventana,fbox1,fbox2,FB_DATO_NULO)
        elif fbox1 != fbox2:
            self.farmaboxRechazado(ventana,fbox1,fbox2,FB_NO_COINCIDEN)
        elif self.existeFB(fbox1):
            if Recursos.esCubetaChica(fbox1):
                if fbox1 in self.listaFarmaboxChico:
                    self.farmaboxRechazado(ventana,fbox1,fbox2,FB_REPETIDO)
                else:
                    self.listaFarmaboxChico.append(fbox1)
                    ventana.nuevoFarmaboxChico(dato1,self.cantidadChicos())
            else:
                if fbox1 in self.listaFarmaboxGrande:
                    self.farmaboxRechazado(ventana,fbox1,fbox2,FB_REPETIDO)
                else:
                    self.listaFarmaboxGrande.append(fbox1)
                    ventana.nuevoFarmaboxGrande(dato1,self.cantidadGrandes())
        else:
            self.farmaboxRechazado(ventana,fbox1,fbox2,FB_NO_EXISTE)

    def agregarTapas(self,tapas):
        self.tapas = tapas

    def farmaboxRechazado(self,ventana,nroFBA, nroFBB, motivo: int):
        self.rechazados += 1
        ventana.nuevoRechazado()
        self.listaRechazados.append((nroFBA,nroFBB,motivo))
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

   