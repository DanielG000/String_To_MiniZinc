from GUI.Ventana import Ventana
import math
import random

class app:

    #Objectos GUI
    __ventana = None


    #Constructor
    def __init__(self):
        self.__ventana = Ventana(self)
        self.startGUI()
        pass

    #Inicio de la aplicación gráfica
    def startGUI(self):
        self.__ventana.mainloop()
        pass

    #Funcion de ejecución general
    def solucionar(self, quien, input):

        miniZinc = self.toMiniZinc(input)
        quien.mostrarMiniZinc(miniZinc)

        pass


    def toMiniZinc(self, texto):

        variables = "%Variables\n\n"
        noNegativo = "%No Negatividad\n\n"
        restricciones = "%Restricciones\n\n"
        funcion = "%Funcion Objetivo\n\nsolve maximize "
        show = "\n%salida MiniZinc\n\noutput["


        lineas = texto.split("\n")

        #guarda los numeros de la cantidad de productos y materias
        nProductos = int(lineas.pop(0))
        mMaterias = int(lineas.pop(0))

        #arreglos
        productos = []
        materias = []
        ganancias = []

        #guarda N Productos en el arreglo productos
        for n in range(nProductos):
            #agrega variables conforme se agregan productos
            variables += F"var int: x{n+1};\n"

            #agrega la restricción de no negatividad a cada variable
            noNegativo += F"constraint x{n+1} >= 0;\n"

            productos.append(lineas.pop(0).split(" "))
        
        #para apariencia las 2 siguientes lineas se pueden eliminar
        variables += "\n"
        noNegativo += "\n"

        #guarda N Materias Primas en el arreglo materias
        for m in range(mMaterias):
            materias.append(lineas.pop(0).split(" "))

            #agregamos las restricción de material segun los productos
            restricciones += "constraint "
            for n in range(nProductos):
                cantidad = productos[n][2+m]

                restricciones += F" x{n+1} * {cantidad} + "
            restricciones += F" 0 <= {materias[m][2]};\n"

        #para apariencia
        restricciones += "\n"


        for n in range(nProductos):
            ganancia = int(productos[n][1])
            for m in range(mMaterias):
                costo = int(materias[m][1]) * int(productos[n][2+m]) 
                ganancia -= costo
            ganancias.append(ganancia)

            funcion += F"x{n+1} * {ganancias[n]} + "
            show += F"\"+\", \" {productos[n][0]}: \", show(x{n+1}), "
        
        #cierre de la funcion objetivo
        funcion += "0;\n"

        #cierre de la funcion output/salida
        show += "]"

        minizinc = variables + noNegativo + restricciones + funcion + show

        self.nProductos = nProductos
        self.mMaterias = mMaterias
        self.rangeP = range(nProductos)
        self.rangeM = range(mMaterias)
        self.productos = productos
        self.materias = materias
        self.ganancias = ganancias

        return minizinc


app()
