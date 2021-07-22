import serial
from threading import Thread
from threading import Semaphore
from time import sleep

import Recursos

class ManagerScanner():
    def __init__(self,ventana):
        self.ventana = ventana
        self.semaforo = Semaphore()
        self.lectura = False
        self.dato = 0
        self.lector1 = LectorPuerto(Recursos.puertoScanner1,Recursos.baudScanner1,self)
        self.lector2 = LectorPuerto(Recursos.puertoScanner2,Recursos.baudScanner2,self)

        if self.lector1 != None :
            self.lector1.iniciar()

        if self.lector2 != None :
            self.lector2.iniciar()      
    
    def recibirDato(self,dato):
        sleep(Recursos.delayScanner)
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