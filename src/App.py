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


    #esta funcion busca la combinacion que maximice la funcion objetivo
    def calcular(self):
        self.variables = []
        z = 0
        for n in self.rangeP:
            self.variables.append(0)
        self.inicioVariables()
        resultado = self.variar()
        show = ""
        for n in self.rangeP:
            show += F" {self.productos[n][0]}: {resultado[n]},"
        show += F" Ganancias: {self.funcionZ()}"
        return show

    def inicioVariables(self):
        for n in self.rangeP:
            mayorMateria = -1
            cantidad = 0
            for m in self.rangeM:
                cantNueva = int(self.productos[n][2+m])
                if cantidad <= cantNueva:
                    mayorMateria = m
                    cantidad = cantNueva

            #ponemos de valir inicial de cada variable el mayor maximo que se puede hacer con la restricción de materia prima. para que vaya reduciendo y buscando la mejor combinación
            inicial = math.ceil(int(self.materias[mayorMateria][2]) / cantidad) - 1
            self.variables[n] = inicial
            self.mejorCombinacion = self.variables.copy()
        pass

    def reinicioVariables(self):
        for n in self.rangeP:
            mayorMateria = -1
            cantidad = 0
            for m in self.rangeM:
                cantNueva = int(self.productos[n][2+m])
                if cantidad <= cantNueva:
                    mayorMateria = m
                    cantidad = cantNueva

            #ponemos de valir inicial de cada variable el mayor maximo que se puede hacer con la restricción de materia prima. para que vaya reduciendo y buscando la mejor combinación
            inicial = math.ceil(int(self.materias[mayorMateria][2]) / cantidad) - 1
            self.variables[n] = inicial
        pass

    def cumplePrimaDisponible(self):
        condicion = False
        for m in self.rangeM:
            r = int(self.materias[m][2])
            v = 0
            for n in self.rangeP:
                v += self.variables[n] * int(self.productos[n][2+m])
            if v <= r and v >= 0:
                condicion = True
            elif v > r or v < 0:
                condicion = False

        return condicion

    def cumpleAllZero(self):
        condicion = True
        valorT = 0
        for n in self.rangeP:
            valor = self.variables[n]
            valorT += valor
            if valor < 0 and valorT >=0:
                self.variables[n] = 0
                condicion = False
            elif valor > 0:
                condicion = False
        return condicion

    def cumpleNoNegatividad(self):
        condicion = True
        for n in self.rangeP:
            valor = self.variables[n]
            if valor < 0:
                condicion = False
                break
        return condicion

    def funcionZ(self):
        z = 0
        for n in self.rangeP:
            z += self.variables[n] * self.ganancias[n]
        return z

    def variar(self):
        self.zOptimo = 0
        for x in self.rangeP:
            self.reinicioVariables()
            #while((self.cumpleNoNegatividad() and not self.cumpleAllZero()) or (self.cumplePrimaDisponible() and not self.cumpleAllZero)):
            while(True):
                n = random.randint(0,(len(self.variables)-1))

                z = self.funcionZ()
                if z >= self.zOptimo and self.cumpleNoNegatividad() and self.cumplePrimaDisponible():
                    self.zOptimo = z
                    self.mejorCombinacion = self.variables.copy()
                self.variables[n] -= 1
                if (self.cumpleAllZero()):
                    break
                
            if z >= self.zOptimo and self.cumpleNoNegatividad() and self.cumplePrimaDisponible():
                self.zOptimo = z
                self.mejorCombinacion = self.variables.copy()
            if (self.cumpleAllZero()):
                break
        return self.mejorCombinacion
    pass

app()
