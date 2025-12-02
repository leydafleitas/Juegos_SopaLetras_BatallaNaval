import turtle
import random
import time
import tkinter as tk
from tkinter import font

class SopaDeLetras:
    def __init__(self):
        self.tamaño_tablero = 10
        self.tablero = self.inicializar_tablero()
        self.letras = "AAAAABBCCCDDEEEEFFGGHIIIJKLLMMNNÑOOOOPPPQRRSSSTTUUUVWXYZ"
        self.diccionario = self.cargar_diccionario("diccionario.txt")
        self.palabras_encontradas = []

    def inicializar_tablero(self):
        tablero = []
        for x in range(self.tamaño_tablero):
            tablero.append([""] * self.tamaño_tablero)
        return tablero

    def cargar_diccionario(self, nombreArchivo):
        with open(nombreArchivo, "r") as archivo:
            return [line.strip().upper() for line in archivo.readlines()]

    def generar_tablero(self):
        for i in range(self.tamaño_tablero):
            for j in range(self.tamaño_tablero):
                self.tablero[i][j] = random.choice(self.letras)

    def dibujar_tablero(self, tortuga):
        tortuga.clear()
        tortuga.penup()
        tortuga.goto(-180, 200)
        tortuga.pendown()
        tortuga.speed(0)
        for i in range(self.tamaño_tablero):
            for j in range(self.tamaño_tablero):
                tortuga.penup()
                tortuga.goto(-180 + j * 40, 200 - i * 40)
                tortuga.write(self.tablero[i][j], align="center", font=("Arial", 12, "normal"))
        tortuga.hideturtle()

    def resaltar_palabra(self, tortuga, palabra, posiciones, color):
        tortuga.penup()
        tortuga.color(color)
        for fila, columna in posiciones:
            tortuga.goto(-180 + columna * 40, 200 - fila * 40)
            tortuga.write(palabra[posiciones.index((fila, columna))], align="center", font=("Arial", 12, "normal"))
        tortuga.color("black")  # Restablece el color de la tortuga a negro
        tortuga.hideturtle()

    def es_palabra_valida(self, x, y):
        return 0 <= x < self.tamaño_tablero and 0 <= y < self.tamaño_tablero

    def buscar_palabra(self, palabra, x, y, contador, visitados, path):
        coordenadas = [
            [-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1],
            [1, -1], [1, 0], [1, 1]
        ]

        if contador == len(palabra):
            return True

        if (
            not self.es_palabra_valida(x, y)
            or (x, y) in visitados
            or self.tablero[x][y] != palabra[contador]
        ):
            return False

        visitados.add((x, y))
        path.append((x, y))

        for dx, dy in coordenadas:
            if self.buscar_palabra(palabra, x + dx, y + dy, contador + 1, visitados, path):
                return True

        visitados.remove((x, y))
        path.pop()
        return False

    def encontrar_palabra(self, palabra):
        path = []
        for i in range(self.tamaño_tablero):
            for j in range(self.tamaño_tablero):
                if self.tablero[i][j] == palabra[0]:  # Empezar a buscar desde la primera letra
                    if self.buscar_palabra(palabra, i, j, 0, set(), path):
                        return path
        return []

    def ingresar_palabra(self, palabra):
        palabra = palabra.upper()  # Asegurar que la palabra esté en mayúsculas
        if palabra in self.palabras_encontradas:
            print(f"{palabra} ya ha sido encontrada.")
        else:
            posiciones = self.encontrar_palabra(palabra)
            if posiciones:
                if palabra in self.diccionario:
                    self.palabras_encontradas.append(palabra)
                    self.resaltar_palabra(t, palabra, posiciones, "green")
                    print(f"{palabra} ha sido encontrada y está en el diccionario!")
                else:
                    self.resaltar_palabra(t, palabra, posiciones, "red")
                    print(f"{palabra} ha sido encontrada pero no está en el diccionario.")
            else:
                print(f"{palabra} no está en la sopa de letras.")

    def calcular_puntaje(self):
        puntaje = 0
        for palabra in self.palabras_encontradas:
            if palabra in self.diccionario:
                puntaje += len(palabra) * 10
        return puntaje

    def enviar_palabra(self):
        palabra = self.entrada_usuario.get().strip().upper()
        self.ingresar_palabra(palabra)
        self.entrada_usuario.delete(0, tk.END)

    def dibujar_botones(self):
        boton_atras = tk.Button(root, text="Atrás", command=self.volver_al_menu)
        boton_atras.place(relx=1, rely=1, anchor="se")

    def jugar(self):
        # Lógica principal del juego
        self.generar_tablero()
        self.dibujar_tablero(t)
        tiempo_inicio = time.time()

        # Configura la entrada de usuario y el botón
        root = tk.Tk()
        root.title("Sopa de Letras")
        frame = tk.Frame(root)
        frame.pack()

        self.entrada_usuario = tk.Entry(frame, width=20)
        self.entrada_usuario.pack(side=tk.LEFT)

        boton_enviar = tk.Button(frame, text="Enviar", command=self.enviar_palabra)
        boton_enviar.pack(side=tk.LEFT)

        # Dibujar los botones
        self.dibujar_botones()

        while time.time() - tiempo_inicio < 300:  # 5 minutos = 300 segundos
            root.update_idletasks()
            root.update()

        root.destroy()
        puntaje = self.calcular_puntaje()
        print(f"Tu puntaje total es: {puntaje}")

        # Configurar la pantalla y la tortuga gráfica
        ventana = turtle.Screen()
        t = turtle.Turtle()
        t.hideturtle()  # Esconde el cursor

        # Dibujar la sopa de letras
        self.generar_tablero()
        self.dibujar_tablero(t)

        ventana.mainloop()

       
