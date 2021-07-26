import os.path
import ctypes
import math
from configparser import ConfigParser


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
    backfeed = configParser.get('Impresora','backfeed')

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

    fechaImprimible = recepcion.fecha

    tsclibrary.setup("SIZE 100 mm, 63 mm")
    tsclibrary.sendcommandW("DIRECTION 1")
    tsclibrary.sendcommandW("GAP 0,0")
    tsclibrary.sendcommandW("CLS")
    tsclibrary.sendcommandW("BACKFEED "+backfeed)
    tsclibrary.windowsfontW("10","10","34","0", "0", "0", "Arial",recepcion.transportista[1]+ " - "+ recepcion.transportista[4])
    tsclibrary.windowsfontW("590","10","34","0", "0", "0", "Arial","Recep: "+str(recepcion.nroRecepcion).zfill(8))
    tsclibrary.windowsfontW("10","50","34","0", "0", "0", "Arial",recepcion.transportista[2])
    tsclibrary.windowsfontW("50","55","26","0", "0", "0", "Arial","("+ recepcion.transportista[3]+")")
    tsclibrary.windowsfontW("545","50","34","0", "0", "0", "Arial",fechaImprimible)
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