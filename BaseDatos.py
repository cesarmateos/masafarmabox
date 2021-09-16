import sqlite3 as sql
import csv

from datetime import datetime
import Recursos

def conectarBase():
    rutaBase = Recursos.rutaArchivo(Recursos.nombreBase)
    try:
        return sql.connect(rutaBase)
    except sql.Error as error:
        print("Fallo al conectarse a la base datos:", error) 

def generarRecepcion(recepcion):
    try:
        #Conecto y armo cursor
        conexion = conectarBase()
        cursor = conexion.cursor()

        #Obtengo datos de la recepcion
        nroTransportista = recepcion.transportista.numero
        codRadio = recepcion.transportista.radio.codigo
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

        for cubeta in listaChicos:
            querySQL = 'INSERT INTO FB_X_RECEPCION (NroFarmabox, NroRecepcion) VALUES (?,?)'
            cursor.execute(querySQL,(cubeta,idGenerado))

        for cubeta in listaGrandes:
            querySQL = 'INSERT INTO FB_X_RECEPCION (NroFarmabox, NroRecepcion) VALUES (?,?)'
            cursor.execute(querySQL,(cubeta,idGenerado))

        for registro in listaRechazados:
            querySQL = 'INSERT INTO RECHAZOS_X_RECEPCION (NroRecepcion,Lectura1,Lectura2,CodMotivoRechazo, AgregadoDC) VALUES (?,?,?,?,?)'
            cursor.execute(querySQL,(idGenerado,registro[0],registro[1],registro[2],registro[3]))

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

def procesarRecepciones():
    try:
        conexion = conectarBase()
        cursor = conexion.cursor()

        querySQL = ('SELECT NroFarmabox FROM FB_X_RECEPCION '
            'JOIN RECEPCION ON RECEPCION.NroRecepcion = FB_X_RECEPCION.NroRecepcion '
            'WHERE RECEPCION.Procesado IS 1')

        cursor.execute(querySQL)
        noProcesados = list(cursor.fetchall())
        querySQL = 'UPDATE RECEPCION SET Procesado = 0 WHERE Procesado IS 1'
        cursor.execute(querySQL)  
        conexion.commit()

        cursor.close
        return noProcesados

    except sql.Error as error:
        print("Fallo al insertar datos de la recepción :", error)
        return None
    finally:
        if conexion:
            conexion.close()
    

#Listados Completos
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

    querySQL = ('SELECT NroTransportista, NombreTransportista, CodRadioUsual,NombreEmpresa,Estado '
        'FROM TRANSPORTISTA '
        'JOIN EMPRESA ON TRANSPORTISTA.CodEmpresa = EMPRESA.CodEmpresa')

    cursor.execute(querySQL)
    transportistas = list(cursor.fetchall())
    cursor.close
    return transportistas

def obtenerTransportistasActivos():
    conexion = conectarBase()
    cursor = conexion.cursor()

    querySQL = ('SELECT * FROM TRANSPORTISTA WHERE Estado=1')

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


#Multiples Condicionales
def buscarRecepciones(fechaDesde,fechaHasta,radio,transporte,empresa,estado):
    conexion = conectarBase()
    cursor = conexion.cursor()
    argumentosLista = []
    primero = True

    
    querySQL = ('SELECT RECEPCION.NroRecepcion,FechaRecepcion,CodRadio,TRANSPORTISTA.NombreTransportista,EMPRESA.NombreEmpresa,COUNT(FB_X_RECEPCION.NroFarmabox) AS CantidadFarmabox,Tapas,Procesado '
        'FROM RECEPCION '
        'JOIN TRANSPORTISTA ON TRANSPORTISTA.NroTransportista = RECEPCION.NroTransportista '
        'JOIN EMPRESA ON EMPRESA.CodEmpresa = TRANSPORTISTA.CodEmpresa '
        'JOIN FB_X_RECEPCION ON FB_X_RECEPCION.NroRecepcion = RECEPCION.NroRecepcion ')

    
    if fechaDesde == '' and fechaHasta =='':
        pass
    else:
        primero = False
        querySQL += 'WHERE FechaRecepcion BETWEEN ? AND ? '
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
            querySQL +='WHERE '
            primero = False 
            
        else:
            querySQL +='AND '
        querySQL += 'CodRadio=? '
        argumentosLista.append(radio)

    if transporte == 0:
        pass
    else:
        if primero:
            querySQL +='WHERE '
            primero = False 
            
        else:
            querySQL +='AND '
        querySQL += 'RECEPCION.NroTransportista=? '
        argumentosLista.append(transporte)


    if empresa == 0:
        pass
    else:
        if primero:
            querySQL +='WHERE ' 
            primero = False
            
        else:
            querySQL +='AND '
        querySQL += 'EMPRESA.CodEmpresa=? '
        argumentosLista.append(empresa)

    if estado == 2:
        pass
    else:
        if primero:
            querySQL +='WHERE ' 
            
        else:
            querySQL +='AND '
        querySQL += 'RECEPCION.Procesado=? '
        argumentosLista.append(estado)


    querySQL +=  'GROUP BY RECEPCION.NroRecepcion '

    argumentos = tuple(argumentosLista)
    cursor.execute(querySQL,(argumentos))

    recepciones = list(cursor.fetchall())
    cursor.close
    
    return recepciones

def agregarFamaboxToRecepciones(recepciones):
    conexion = conectarBase()
    cursor = conexion.cursor()

    argumentosLista = []
    querySQL = ''

    for indice, recepcion in enumerate(recepciones):
        if(indice!=0):
            querySQL += ' UNION '
        querySQL += ('SELECT RECEPCION.NroRecepcion,FechaRecepcion,CodRadio,TRANSPORTISTA.NombreTransportista,EMPRESA.NombreEmpresa, FB_X_RECEPCION.NroFarmabox,Tapas '
            'FROM RECEPCION '
            'JOIN TRANSPORTISTA ON TRANSPORTISTA.NroTransportista = RECEPCION.NroTransportista '
            'JOIN EMPRESA ON EMPRESA.CodEmpresa = TRANSPORTISTA.CodEmpresa '
            'JOIN FB_X_RECEPCION ON FB_X_RECEPCION.NroRecepcion = RECEPCION.NroRecepcion '
            'WHERE FB_X_RECEPCION.NroRecepcion=?')
        argumentosLista.append(recepcion[0])
    
    argumentos = tuple(argumentosLista)
    cursor.execute(querySQL,(argumentos))
    recepcion = list(cursor.fetchall())
    cursor.close

    return recepcion

def buscarRechazos(fechaDesde,fechaHasta,motivo,nroRecepcion):
    conexion = conectarBase()
    cursor = conexion.cursor()
    
    argumentosLista = []
    primero = True

    querySQL = ('SELECT RECEPCION.FechaRecepcion, RECEPCION.NroRecepcion, Lectura1, Lectura2, MotivoRechazo '
                'FROM RECHAZOS_X_RECEPCION '
                'JOIN RECEPCION ON RECEPCION.NroRecepcion = RECHAZOS_X_RECEPCION.NroRecepcion '
                'JOIN MOTIVO_RECHAZO ON MOTIVO_RECHAZO.CodRechazo = RECHAZOS_X_RECEPCION.CodMotivoRechazo ')

    
    if fechaDesde == '' and fechaHasta =='':
        pass
    else:
        primero = False
        querySQL += 'WHERE FechaRecepcion BETWEEN ? AND ? '
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


    if motivo == 0:
        pass
    else:
        if primero:
            querySQL +='WHERE '
            primero = False 
        else:
            querySQL +='AND '
        querySQL += 'MOTIVO_RECHAZO.CodRechazo=? '
        argumentosLista.append(motivo)

    if nroRecepcion == '':
        pass
    else:
        if primero:
            querySQL +='WHERE '
            primero = False 
        else:
            querySQL +='AND '
        querySQL += 'RECEPCION.NroRecepcion=? '
        argumentosLista.append(nroRecepcion)

    argumentos = tuple(argumentosLista)
    cursor.execute(querySQL,(argumentos))

    rechazos = list(cursor.fetchall())
    cursor.close
    
    return rechazos

def buscarModificaciones(fechaDesde,fechaHasta,tipo):
    conexion = conectarBase()
    cursor = conexion.cursor()
    argumentosLista = []
    primero = True

    
    querySQL = ('SELECT NroModificacion, TipoModificacion, FechaModificacion '
                'FROM MODIFICACION '
                'JOIN TIPOS_MODIFICACION ON TIPOS_MODIFICACION.CodTipoModificacion = MODIFICACION.CodTipoModificacion ')

    
    if fechaDesde == '' and fechaHasta =='':
        pass
    else:
        primero = False
        querySQL += 'WHERE FechaModificacion BETWEEN ? AND ? '
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


    if tipo == 0:
        pass
    else:
        if primero:
            querySQL +='WHERE '
            primero = False 
        else:
            querySQL +='AND '
        querySQL += 'TIPOS_MODIFICACION.CodTipoModificacion=? '
        argumentosLista.append(tipo)


    argumentos = tuple(argumentosLista)
    cursor.execute(querySQL,(argumentos))

    modificaciones = list(cursor.fetchall())
    cursor.close
    
    return modificaciones

def buscarKardexFarmabox(nroFarmabox,fechaDesde,fechaHasta):
    conexion = conectarBase()
    cursor = conexion.cursor()

    argumentosLista = [nroFarmabox]
    parte2 = parte4 =''

    
    parte1 = ('SELECT NroFarmabox, FechaModificacion AS Fecha, TIPOS_MODIFICACION.TipoModificacion AS TipoMovimiento, "-" AS Nro_Recepcion,MODIFICACION.NroModificacion, "-" AS CodRadio '
            'FROM MODIFICACION '
            'JOIN FB_X_MODIFICACION ON FB_X_MODIFICACION.NroModificacion = MODIFICACION.NroModificacion '
            'JOIN TIPOS_MODIFICACION ON TIPOS_MODIFICACION.CodTipoModificacion = MODIFICACION.CodTipoModificacion '
            'WHERE FB_X_MODIFICACION.NroFarmabox = ?')
    parte3 = ('UNION '
            'SELECT NroFarmabox, FechaRecepcion AS Fecha, "RECEPCIÓN" AS TipoMovimiento, RECEPCION.NroRecepcion, "-" AS NroModificacion, CodRadio '
            'FROM RECEPCION '
            'JOIN FB_X_RECEPCION ON FB_X_RECEPCION.NroRecepcion = RECEPCION.NroRecepcion '
            'WHERE FB_X_RECEPCION.NroFarmabox = ? ')
    parte5 ='ORDER BY 2'

    if fechaDesde == '' and fechaHasta =='':
        argumentosLista.append(nroFarmabox) 
    else:
        parte2 = 'AND FechaModificacion BETWEEN ? AND ? '
        parte4 = 'AND FechaRecepcion BETWEEN ? AND ? '
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
        argumentosLista.append(nroFarmabox) 
        argumentosLista.append(fechaDesdeFormateada)
        argumentosLista.append(fechaHastaFormateada)   

    querySQL = parte1+parte2+parte3+parte4+parte5

    argumentos = tuple(argumentosLista)
    cursor.execute(querySQL,(argumentos))

    kardex = list(cursor.fetchall())
    tuplaBusqueda = (kardex,fechaDesde,fechaHasta)
    cursor.close

    return tuplaBusqueda

#Registro Singular
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

def buscarRadio(corRadio):
    conexion = conectarBase()
    cursor = conexion.cursor()

    querySQL = ('SELECT CodRadio,DescripcionRadio '
        'FROM RADIO '
        'WHERE CodRadio=?')
    
    filaRadio = cursor.execute(querySQL,(corRadio,))
    radio = filaRadio.fetchone()

    cursor.close
    return radio

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

def buscarRecepcionParaArmadoDeClase(nroRecepcion):
    conexion = conectarBase()
    cursor = conexion.cursor()

    if nroRecepcion != '':
        querySQL = ('SELECT '
            'RECEPCION.NroRecepcion,FechaRecepcion,CodRadio,NroTransportista, FB_X_RECEPCION.NroFarmabox,Tapas '
            'FROM RECEPCION '
            'JOIN FB_X_RECEPCION ON FB_X_RECEPCION.NroRecepcion = RECEPCION.NroRecepcion '
            'WHERE FB_X_RECEPCION.NroRecepcion=?')

        cursor.execute(querySQL,(nroRecepcion,))
        recepcion = list(cursor.fetchall())
        cursor.close
        return recepcion
    return None

def buscarModificacion(nroModificacion):
    conexion = conectarBase()
    cursor = conexion.cursor()

    if nroModificacion != '':
        querySQL = ('SELECT MODIFICACION.NroModificacion, FechaModificacion,TipoModificacion,NroFarmabox '
                    'FROM MODIFICACION '
                    'JOIN TIPOS_MODIFICACION ON TIPOS_MODIFICACION.CodTipoModificacion = MODIFICACION.CodTipoModificacion '
                    'JOIN FB_X_MODIFICACION ON FB_X_MODIFICACION.NroModificacion = MODIFICACION.NroModificacion '
                    'WHERE MODIFICACION.NroModificacion=?')

        cursor.execute(querySQL,(nroModificacion,))
        modificacion = list(cursor.fetchall())
        cursor.close
        return modificacion
    return None

def encontrarTransportista(nroTransportista):
    conexion = conectarBase()
    cursor = conexion.cursor()

    querySQL = ('SELECT NroTransportista, NombreTransportista, CodRadioUsual, DescripcionRadio, NombreEmpresa, Estado '
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


#Agregar Registros
def agregarEmpresa(nombreEmpresa: str):
    try:
        conexion = conectarBase()
        cursor = conexion.cursor()
        querySQL = 'INSERT INTO EMPRESA (NombreEmpresa) VALUES (?)'
        cursor.execute(querySQL,(nombreEmpresa,))
        conexion.commit()

        #Obtengo ID
        idGenerado = cursor.lastrowid

        return idGenerado

    except sql.Error as error:
        return None
        
    finally:
        cursor.close()

def agregarRadio(codigo,descipcion):
    try:
        conexion = conectarBase()
        cursor = conexion.cursor()
        querySQL = 'INSERT INTO RADIO (CodRadio,DescripcionRadio) VALUES (?,?)'
        cursor.execute(querySQL,(codigo,descipcion,))
        conexion.commit()

        return codigo

    except sql.Error as error:
        print(error)
        return None
        
    finally:
        cursor.close()

def agregarTransportista(codigo,nombre,codRadio,nroEmpresa):
    try:
        conexion = conectarBase()
        cursor = conexion.cursor()
        querySQL = 'INSERT INTO TRANSPORTISTA (NroTransportista,NombreTransportista,CodRadioUsual,CodEmpresa,Estado) VALUES (?,?,?,?,?)'
        cursor.execute(querySQL,(codigo,nombre,codRadio,nroEmpresa,1,))
        conexion.commit()

        return codigo

    except sql.Error as error:
        return None
        
    finally:
        cursor.close()

#Modificar Registros
def modificarTransportista(transportista):
    conexion = conectarBase()
    cursor = conexion.cursor()

    querySQL = ('UPDATE TRANSPORTISTA '
        'SET CodRadioUsual = ?, '
        'Estado = ? '
        'WHERE NroTransportista = ?')
    
    try:
        cursor.execute(querySQL,(transportista.radio.codigo,transportista.estado,transportista.numero))

        conexion.commit()
        return True
    except:
        return False
    finally:
        cursor.close()


#Especial
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