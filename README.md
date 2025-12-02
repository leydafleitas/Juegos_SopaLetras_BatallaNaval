# Batalla Naval y Sopa de Letras
Lenguaje: Python  
Materia: Algoritmos y Estructuras de Datos (ATOS II)  
Institución: Universidad Nacional de Asunción  

Este repositorio contiene dos proyectos desarrollados como parte del curso de Algoritmos y Estructuras de Datos. Ambos ejercicios implementan conceptos fundamentales de programación estructurada, listas, matrices, modularización y validación de datos.

---

## 1. Batalla Naval

El proyecto implementa una versión simplificada del clásico juego Batalla Naval, donde el usuario intenta localizar barcos distribuidos aleatoriamente dentro de una matriz.

### Características principales
- Generación automática del tablero mediante listas anidadas.
- Posicionamiento aleatorio de barcos.
- Validación de coordenadas ingresadas por el usuario.
- Registro de intentos y control del estado del juego.
- Representación visual del tablero:
  - `X`: impacto  
  - `O`: disparo fallado  
  - `-`: casilla no revelada  

### Conceptos aplicados
- Listas y listas anidadas (matrices).
- Uso de la librería `random` para distribución aleatoria de barcos.
- Funciones modularizadas para organizar la lógica del programa.
- Validación de datos de entrada.
- Control de flujo mediante condicionales y bucles.

### Ejecución
```bash
python batalla_naval.py
```
## 2. Sopa de Letras

Este programa genera una matriz de caracteres y permite al usuario buscar palabras dentro del tablero, verificando su presencia en forma horizontal o vertical.

###Características principales
Generación automática del tablero con letras aleatorias.

Inserción de palabras horizontalmente y verticalmente.

Búsqueda de palabras ingresadas por el usuario.

Confirmación sobre si la palabra fue encontrada utilizando backtracking.

Posibilidad de realizar múltiples consultas consecutivas.

Conceptos aplicados
Manipulación de matrices bidimensionales.

Recorridos horizontales y verticales.

Funciones modularizadas para búsqueda y validación.

Control de índices y manejo simple de errores.

Ejecución
bash
Copiar código
python sopa_de_letras.py
Tecnologías utilizadas
Python 3.x

Librería estándar random

Estructuras de datos básicas

## Objetivo académico
Este proyecto busca reforzar los conceptos fundamentales de:

Programación estructurada

Estructuras de datos básicas

Modularización del código

Manipulación de matrices

Implementación de juegos interactivos en consola

Posibles mejoras futuras
Implementación de una interfaz gráfica (Tkinter o PyQt).

Incorporación de niveles de dificultad.

Búsqueda diagonal en la Sopa de Letras.

Modo para dos jugadores en Batalla Naval.

## Autores
Leyda Fleitas

Andrea Nuñez

Elena Ramirez

Braian Romero
