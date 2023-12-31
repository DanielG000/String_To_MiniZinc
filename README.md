# String To MiniZinc

Esta aplicación convierte el formato establecido de texto a un lenguaje de programacion para el IDE MiniZinc.El formato de texto contiene las cantidades y 2 tablas respectivamente, la primer tabla es de las variables o productos objetivo, la segunda de los materiales y costos para la anterior tabla.

## Formato de las Tablas en Texto

La primera linea contiene la cantidad de tuplas para la primera tabla,

La segunda linea contiene la cantidad de tuplas para la segunda tabla,

Acorde a el numero n de la primera linea, las siguientes n lineas son tuplas de la primera tabla.

Al igual que lo anterior acorde al numero m de la segunda linea, las m lineas son tuplas de la segunda tabla.

Las tuplas de la primera contiene el nombre de la variable, el precio, las cantidades de materiales, deben ser adorde a la cantidad de materias primas.

Las tuplas de las segunda contiene el nombre de la materia, el costo, y la cantidad disponible.

### Ejemplo

> + 3
> + 3
> + Empanada 2000 2 1 3
> + Rellena 5000 3 9 9
> + Marranita 3000 2 0 4
> + Materia_prima_1 100 305
> + Materia_prima_2 250 405
> + Materia_prima_3 400 525
