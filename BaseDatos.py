import sqlite3 as sql

from datetime import datetime
import Recursos

def conectarBase():
    rutaBase = Recursos.rutaArchivo(Recursos.nombreBase)
    return sql.connect(rutaBase)

def encontrarTransportista(NroTransportista):
    conexion = conectarBase()
    cursor = conexion.cursor()

    querySQL = 'SELECT * FROM TRANSPORTISTA WHERE NroTransportista=?'
    filaTransportista = cursor.execute(querySQL,(NroTransportista,))
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
        listaChicos = recepcion.listaFarmaboxChico
        listaGrandes = recepcion.listaFarmaboxGrande
        tapas = recepcion.tapas

        #Armo y ejecuto la Query
        now = datetime.now()
        fechaHora = now.strftime("%Y/%m/%d %H:%M:%S")
        querySQL = 'INSERT INTO RECEPCION (NroTransportista, FechaRecepcion, Tapas) VALUES (?,?,?)'
        cursor.execute(querySQL,(nroTransportista,fechaHora,tapas))
        

        #Obtengo ID
        idGenerado = cursor.lastrowid

        #Obtengo toda la fila
        querySQL = 'SELECT * FROM RECEPCION WHERE NroRecepcion=?'
        resultadoQuery = cursor.execute(querySQL,(idGenerado,))
        ultimaFila = resultadoQuery.fetchone()

        #Copio los valores de la nueva recepción en la clase
        recepcion.setNroRecepcion(idGenerado)
        recepcion.setFecha(ultimaFila[3])
        recepcion.agregarTapas(ultimaFila[4])
                

        for cubeta in listaChicos:
            querySQL = 'INSERT INTO FB_X_RECEPCION (NroFarmabox, NroRecepcion) VALUES (?,?)'
            cursor.execute(querySQL,(cubeta,idGenerado))

        for cubeta in listaGrandes:
            querySQL = 'INSERT INTO FB_X_RECEPCION (NroFarmabox, NroRecepcion) VALUES (?,?)'
            cursor.execute(querySQL,(cubeta,idGenerado))

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


