import sqlite3 as sql
import csv

from datetime import datetime
import Recursos

def conectarBase():
    rutaBase = Recursos.rutaArchivo(Recursos.nombreBase)
    return sql.connect(rutaBase)

def encontrarTransportista(nroTransportista):
    
    conexion = conectarBase()
    cursor = conexion.cursor()

    querySQL = ('SELECT NroTransportista, NombreTransportista, CodRadioUsual, DescripcionRadio, NombreEmpresa '
        'FROM TRANSPORTISTA '
        'JOIN RADIO ON RADIO.CodRadio = TRANSPORTISTA.CodRadioUsual '
        'JOIN EMPRESA ON EMPRESA.CodEmpresa = TRANSPORTISTA.CodEmpresa '
        'WHERE TRANSPORTISTA.NroTransportista=?')
    

    filaTransportista = cursor.execute(querySQL,(nroTransportista,))
    transportista = filaTransportista.fetchone()

    if transportista is None:
        cursor.close
        return None

    cursor.close
    return transportista

def generarRecepcion(recepcion):
    try:
        #Conecto y armo cursor
        conexion = conectarBase()
        cursor = conexion.cursor()

        #Obtengo datos de la recepcion
        nroTransportista = recepcion.transportista[0]
        codRadio = recepcion.transportista[2]
        listaChicos = recepcion.listaFarmaboxChico
        listaGrandes = recepcion.listaFarmaboxGrande
        listaRechazados = recepcion.listaRechazados
        tapas = recepcion.tapas

        #Armo y ejecuto la Query
        fechaHora = datetime.now()
        querySQL = 'INSERT INTO RECEPCION (CodRadio, NroTransportista, FechaRecepcion, Tapas) VALUES (?,?,?,?)'
        cursor.execute(querySQL,(codRadio,nroTransportista,fechaHora,tapas))
        

        #Obtengo ID
        idGenerado = cursor.lastrowid

        #Obtengo toda la fila
        querySQL = 'SELECT * FROM RECEPCION WHERE NroRecepcion=?'
        resultadoQuery = cursor.execute(querySQL,(idGenerado,))
        ultimaFila = resultadoQuery.fetchone()

        #Copio los valores de la nueva recepción en la clase
        recepcion.setNroRecepcion(idGenerado)
        recepcion.setFecha(ultimaFila[4])
        recepcion.agregarTapas(ultimaFila[5])
                

        for cubeta in listaChicos:
            querySQL = 'INSERT INTO FB_X_RECEPCION (NroFarmabox, NroRecepcion) VALUES (?,?)'
            cursor.execute(querySQL,(cubeta,idGenerado))

        for cubeta in listaGrandes:
            querySQL = 'INSERT INTO FB_X_RECEPCION (NroFarmabox, NroRecepcion) VALUES (?,?)'
            cursor.execute(querySQL,(cubeta,idGenerado))

        for registro in listaRechazados:
            querySQL = 'INSERT INTO RECHAZOS_X_RECEPCION (NroRecepcion,Lectura1,Lectura2,CodMotivoRechazo) VALUES (?,?,?,?)'
            cursor.execute(querySQL,(idGenerado,registro[0],registro[1],registro[2]))

        conexion.commit()
        cursor.close()

        print("Se generó la recepción "+ str(idGenerado))

        return idGenerado

    except sql.Error as error:
            print("Fallo al insertar datos de la recepción :", error)
    finally:
        if conexion:
            conexion.close()
            print("The SQLite connection is closed")

def obtenerRadios():
    conexion = conectarBase()
    cursor = conexion.cursor()

    querySQL = ('SELECT * FROM RADIO')

    cursor.execute(querySQL)
    radios = list(cursor.fetchall())
    cursor.close
    return radios

def obtenerTransportistas():
    conexion = conectarBase()
    cursor = conexion.cursor()

    querySQL = ('SELECT * FROM TRANSPORTISTA')

    cursor.execute(querySQL)
    transportistas = list(cursor.fetchall())
    cursor.close
    return transportistas

def obtenerEmpresas():
    conexion = conectarBase()
    cursor = conexion.cursor()

    querySQL = ('SELECT * FROM EMPRESA')

    cursor.execute(querySQL)
    empresas = list(cursor.fetchall())
    cursor.close
    return empresas

def obtenerTiposModificacion():
    conexion = conectarBase()
    cursor = conexion.cursor()

    querySQL = ('SELECT * FROM TIPOS_MODIFICACION')

    cursor.execute(querySQL)
    tiposMod = list(cursor.fetchall())
    cursor.close
    return tiposMod

def obtenerMotivosRechazo():
    conexion = conectarBase()
    cursor = conexion.cursor()

    querySQL = ('SELECT * FROM MOTIVO_RECHAZO')

    cursor.execute(querySQL)
    rechazo = list(cursor.fetchall())
    cursor.close
    return rechazo

def encontrarFarmabox(NroFarmabox):
    conexion = conectarBase()
    cursor = conexion.cursor()

    querySQL = ('SELECT * FROM FARMABOX '
        'WHERE NroFarmabox=?')

    filaFB = cursor.execute(querySQL,(NroFarmabox,))
    farmabox = filaFB.fetchone()

    if farmabox is None:
        cursor.close
        return None

    cursor.close
    return farmabox

def buscarRecepciones(fechaDesde,fechaHasta,radio,transporte,empresa):
    conexion = conectarBase()
    cursor = conexion.cursor()
    argumentosLista = []
    primero = True

    
    parte1 = ('SELECT RECEPCION.NroRecepcion,FechaRecepcion,CodRadio,TRANSPORTISTA.NombreTransportista,EMPRESA.NombreEmpresa,COUNT(FB_X_RECEPCION.NroFarmabox) AS CantidadFarmabox,Tapas,Procesado '
        'FROM RECEPCION '
        'JOIN TRANSPORTISTA ON TRANSPORTISTA.NroTransportista = RECEPCION.NroTransportista '
        'JOIN EMPRESA ON EMPRESA.CodEmpresa = TRANSPORTISTA.CodEmpresa '
        'JOIN FB_X_RECEPCION ON FB_X_RECEPCION.NroRecepcion = RECEPCION.NroRecepcion ')

    parte2 = parte2 = parte3 = parte4 = parte5 = parte6 = parte7 = parte8 = ''
    parte9 = 'GROUP BY RECEPCION.NroRecepcion '
    
    if fechaDesde == '' and fechaHasta =='':
        pass
    else:
        primero = False
        parte2 = 'WHERE FechaRecepcion BETWEEN ? AND ? '
        fechaDesdeFormateada = None
        fechaHastaFormateada = None
        if fechaDesde != '' and fechaHasta !='':
            desde = fechaDesde + ' 00:00:00'
            fechaDesdeFormateada = datetime.strptime(desde, "%d/%m/%y %H:%M:%S")
            hasta = fechaHasta +' 23:59:59'
            fechaHastaFormateada = datetime.strptime(hasta, "%d/%m/%y %H:%M:%S")
        elif fechaDesde != '' and fechaHasta =='':
            desde = fechaDesde + ' 00:00:00'
            fechaDesdeFormateada = datetime.strptime(desde, "%d/%m/%y %H:%M:%S")
            fechaHastaFormateada = datetime.now()

        else:
            hasta = fechaHasta +' 23:59:59'
            fechaDesdeFormateada = datetime.strptime('2021/07/22 15:44:23', "%Y/%m/%d %H:%M:%S")
            fechaHastaFormateada = datetime.strptime(hasta, "%d/%m/%y %H:%M:%S")

        argumentosLista.append(fechaDesdeFormateada)
        argumentosLista.append(fechaHastaFormateada)   

    if radio == '00':
        pass
    else:
        if primero:
            parte3 ='WHERE '
            primero = False 
            
        else:
            parte3 ='AND '
        parte4 = 'CodRadio=? '
        argumentosLista.append(radio)

    if transporte == 0:
        pass
    else:
        if primero:
            parte5 ='WHERE '
            primero = False 
            
        else:
            parte5 ='AND '
        parte6 = 'RECEPCION.NroTransportista=? '
        argumentosLista.append(transporte)


    if empresa == 0:
        pass
    else:
        if primero:
            parte7 ='WHERE ' 
            
        else:
            parte7 ='AND '
        parte8 = 'EMPRESA.CodEmpresa=? '
        argumentosLista.append(empresa)

   
    querySQL =  parte1 + parte2 + parte3 + parte4 + parte5 + parte6 + parte7+ parte8 +parte9

    argumentos = tuple(argumentosLista)
    cursor.execute(querySQL,(argumentos))

    recepciones = list(cursor.fetchall())
    cursor.close
    
    return recepciones

def buscarRecepcion(nroRecepcion):
    conexion = conectarBase()
    cursor = conexion.cursor()

    if nroRecepcion != '':
        querySQL = ('SELECT '
            'RECEPCION.NroRecepcion,FechaRecepcion,CodRadio,TRANSPORTISTA.NombreTransportista,EMPRESA.NombreEmpresa, FB_X_RECEPCION.NroFarmabox,Tapas,Procesado '
            'FROM RECEPCION '
            'JOIN TRANSPORTISTA ON TRANSPORTISTA.NroTransportista = RECEPCION.NroTransportista '
            'JOIN EMPRESA ON EMPRESA.CodEmpresa = TRANSPORTISTA.CodEmpresa '
            'JOIN FB_X_RECEPCION ON FB_X_RECEPCION.NroRecepcion = RECEPCION.NroRecepcion '
            'WHERE FB_X_RECEPCION.NroRecepcion=?')

        cursor.execute(querySQL,(nroRecepcion,))
        recepcion = list(cursor.fetchall())
        cursor.close
        return recepcion
    return None

def cargarFarmaboxDesdeCSV(archivo,tipo:int):
    
    #Conecto y armo cursor
    conexion = conectarBase()
    cursor = conexion.cursor()

    #Armo y ejecuto la Query
    now = datetime.now()
    #fechaHora = now.strftime("%Y/%m/%d %H:%M:%S")
    querySQL = 'INSERT INTO MODIFICACION (CodTipoModificacion) VALUES (?)'
    cursor.execute(querySQL,(str(tipo)))

    #Obtengo ID
    idGenerado = cursor.lastrowid

    querySQL2 = 'INSERT INTO FB_X_MODIFICACION (NroFarmabox,NroModificacion) VALUES (?,?)'
    querySQL3 = 'INSERT OR REPLACE INTO FARMABOX (NroFarmabox,CodEstadoFarmabox) VALUES (?,?)'

    with open(archivo, newline='') as File:  
        reader = csv.DictReader(File)
        for row in reader:    
            cursor.execute(querySQL3,(row['NroFarmabox'],int(1)))
            cursor.execute(querySQL2,(row['NroFarmabox'],idGenerado))
            

    conexion.commit()
    cursor.close()
