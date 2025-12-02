import random
import time
import tkinter as tk
from tkinter import font


class SopaDeLetras:
    def __init__(self, ventana_menu):
        self.tamaño_tablero = 10
        self.tablero = self.inicializar_tablero()
        self.letras = "AAAAABBCCCDDEEEEFFGGHIIIJKLLMMNNÑOOOOPPPQRRSSSTTUUUVWXYZ"
        self.diccionario = self.cargar_diccionario("diccionario.txt")
        self.palabras_encontradas = []
        self.ventana_menu = ventana_menu

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

    def dibujar_tablero(self):
        self.canvas.delete("all")
        for i in range(self.tamaño_tablero):
            for j in range(self.tamaño_tablero):
                x0 = j * 40
                y0 = i * 40
                x1 = x0 + 40
                y1 = y0 + 40
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", width=2)
                self.canvas.create_text(
                    (x0 + 20, y0 + 20), text=self.tablero[i][j], font=("Arial", 12)
                )

    def resaltar_palabra(self, palabra, posiciones, color):
        for fila, columna in posiciones:
            x0 = columna * 40
            y0 = fila * 40
            x1 = x0 + 40
            y1 = y0 + 40
            self.canvas.create_rectangle(
                x0, y0, x1, y1, fill=color, outline="black", width=2
            )
            self.canvas.create_text(
                (x0 + 20, y0 + 20), text=self.tablero[fila][columna], font=("Arial", 12)
            )

    def es_palabra_valida(self, x, y):
        return 0 <= x < self.tamaño_tablero and 0 <= y < self.tamaño_tablero

    def buscar_palabra(self, palabra, x, y, contador, visitados, path):
        coordenadas = [
            [-1, -1],
            [-1, 0],
            [-1, 1],
            [0, -1],
            [0, 1],
            [1, -1],
            [1, 0],
            [1, 1],
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
            if self.buscar_palabra(
                palabra, x + dx, y + dy, contador + 1, visitados, path
            ):
                return True
        visitados.remove((x, y))
        path.pop()
        return False

    def encontrar_palabra(self, palabra):
        path = []
        for i in range(self.tamaño_tablero):
            for j in range(self.tamaño_tablero):
                if (
                    self.tablero[i][j] == palabra[0]
                ):  # Empezar a buscar desde la primera letra
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
                    self.resaltar_palabra(palabra, posiciones, "lightgreen")
                    print(f"{palabra} ha sido encontrada y está en el diccionario!")
                else:
                    self.resaltar_palabra(palabra, posiciones, "red")
                    print(
                        f"{palabra} ha sido encontrada pero no está en el diccionario."
                    )
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

    def volver_al_menu(self):
        self.ventana_juego.destroy()
        self.ventana_menu.deiconify()

    def jugar(self):
        self.ventana_menu.withdraw()
        self.ventana_juego = tk.Toplevel(self.ventana_menu)
        self.ventana_juego.title("Sopa de Letras")
        self.ventana_juego.geometry("600x600")
        self.ventana_juego.configure(bg="#F3D0D7")

        self.canvas = tk.Canvas(
            self.ventana_juego, width=400, height=400, bg="white"
        )
        self.canvas.pack(pady=20)

        self.generar_tablero()
        self.dibujar_tablero()

        frame = tk.Frame(self.ventana_juego, bg="#F3D0D7")
        frame.pack(pady=10)

        self.entrada_usuario = tk.Entry(frame, width=20, bg="white")
        self.entrada_usuario.pack(pady=5)

        boton_enviar = tk.Button(
            frame, text="Enviar", command=self.enviar_palabra, bg="purple", fg="black"
        )
        boton_enviar.pack(pady=5)

        boton_volver_menu = tk.Button(
            frame,
            text="Volver al menú",
            command=self.volver_al_menu,
            bg="purple",
            fg="black",
        )
        boton_volver_menu.pack(pady=5)

        self.ventana_juego.mainloop()


# Función para iniciar la sopa de letras
def iniciar_sopa_de_letras():
    juego = SopaDeLetras(ventana_menu)
    juego.jugar()


# Función para iniciar la batalla naval
def iniciar_batalla_naval():
    ventana_menu.withdraw()
    ventana_juego = tk.Toplevel(ventana_menu)
    ventana_juego.title("Batalla Naval")
    ventana_juego.geometry("600x600")
    ventana_juego.configure(bg="#F3D0D7")

    canvas = tk.Canvas(ventana_juego, width=400, height=400, bg="white")
    canvas.pack(pady=20)

    # Dibujar el tablero
    for i in range(11):
        x0 = 50 + i * 30
        y0 = 50
        x1 = x0
        y1 = 350
        canvas.create_line(x0, y0, x1, y1)
        canvas.create_line(y0, x0, y1, x1)

    boton_volver_menu = tk.Button(
        ventana_juego,
        text="Volver al menú",
        command=lambda: [ventana_juego.destroy(), ventana_menu.deiconify()],
        bg="purple",
        fg="black",
    )
    boton_volver_menu.pack(pady=20)

    ventana_juego.mainloop()


# Crear la ventana de Tkinter
ventana_menu = tk.Tk()
ventana_menu.title("Menú Principal")
ventana_menu.geometry("600x600")
ventana_menu.configure(bg="#F3D0D7")

# Configurar la fuente y los colores
titulo_font = font.Font(family="Arial", size=24, weight="bold")
subtitulo_font = font.Font(family="Arial", size=16)
boton_font = font.Font(family="Arial", size=16, weight="bold")

# Crear un título
titulo = tk.Label(
    ventana_menu,
    text="BIENVENIDO/A A JUEGOS DIVERTIDOS",
    font=titulo_font,
    fg="black",
    bg="#F3D0D7",
)
titulo.pack(pady=20)

# Crear un subtítulo
subtitulo = tk.Label(
    ventana_menu,
    text="Seleccione qué juego le gustaría jugar",
    font=subtitulo_font,
    fg="black",
    bg="#F3D0D7",
)
subtitulo.pack(pady=10)

# Crear botones para cada juego
btn_sopa_de_letras = tk.Button(
    ventana_menu,
    text="Sopa de Letras",
    command=iniciar_sopa_de_letras,
    font=boton_font,
    bg="purple",
    fg="black",
    width=20,
    height=2,
)
btn_sopa_de_letras.pack(pady=20)

btn_batalla_naval = tk.Button(
    ventana_menu,
    text="Batalla Naval",
    command=iniciar_batalla_naval,
    font=boton_font,
    bg="light blue",
    fg="black",
    width=20,
    height=2,
)
btn_batalla_naval.pack(pady=20)

# Ejecutar el bucle principal de Tkinter
ventana_menu.mainloop()