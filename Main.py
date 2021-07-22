import Recursos
import Ventanas

Recursos.leerConfig()

ventana = Ventanas.Ventana()

Recursos.ManagerScanner(ventana)

ventana.mainloop()
