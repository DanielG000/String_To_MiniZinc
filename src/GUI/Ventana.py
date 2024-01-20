import customtkinter
from customtkinter import CTk, CTkFrame, CTkButton, CTkTextbox, CTkLabel
import os

class Ventana(customtkinter.CTk):

    __manager = None

    def __init__(self, main):
        super().__init__()
        self.__manager = main
        self.title("String To MiniZinc")
        self.geometry("900x600")
        self.create_widgets()
        pass

    def create_widgets(self):
        #creación de cada componente
        self.__frame = CTkFrame(self)
        self.__label = CTkLabel(self.__frame, text="String to MiniZinc - Optimización\n")
        self.__labelIn = CTkLabel(self.__frame, text="Input:")
        self.__labelOut = CTkLabel(self.__frame, text="Output Minizinc:")
        self.__input = CTkTextbox(self.__frame)
        self.__output = CTkTextbox(self.__frame)
        self.__resolver = CTkButton(self.__frame, text="Convertir", command=self.solucionar)

        
        #Mostrar en el frame
        self.__frame.pack()
        self.__label.pack()
        self.__labelIn.pack()
        self.__labelOut.pack()
        self.__input.pack()
        self.__output.pack()
        self.__resolver.pack()

        #Posicion de los componentes
        self.__frame.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)
        self.__label.place(relx=0.05, rely=0.025, relwidth=0.9, relheight=0.05)
        self.__labelIn.place(relx=0.05, rely=0.10, relwidth=0.1, relheight=0.05)
        self.__labelOut.place(relx=0.55, rely=0.10, relwidth=0.1, relheight=0.05)
        self.__input.place(relx=0.025, rely=0.15, relwidth=0.45, relheight=0.70)
        self.__output.place(relx=0.525, rely=0.15, relwidth=0.45, relheight=0.70)
        self.__resolver.place(relx=0.25, rely=0.9, relwidth=0.5, relheight=0.05)

        #texto por defecto
        self.example()
        pass

    def example(self):
        lineas = open("Examples/inputExample.txt", "r")

        ejemplo = ""

        for l in lineas:
            ejemplo += l

        self.__input.insert("0.0", ejemplo)
        pass

    def solucionar(self):
        textoInput = self.__input.get("0.0", "end")
        self.__manager.solucionar(self, textoInput)
        pass

    def mostrarSolucion(self, texto):
        texto = "Solución:\n" + texto
        self.__label.configure(text=texto)
        pass

    def mostrarMiniZinc(self, texto):
        self.__output.delete("0.0", "end")
        self.__output.insert("0.0", texto)
        pass

    pass
