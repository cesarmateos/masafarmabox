import Recursos
import Ventanas
import Scanners


Recursos.leerConfig()

ventana = Ventanas.Ventana()

Scanners.ManagerScanner(ventana)

ventana.mainloop()

#archivo = Recursos.rutaArchivo('Recursos/FarmaboxAlta.csv')
#BaseDatos.cargarFarmaboxDesdeCSV(archivo,1)