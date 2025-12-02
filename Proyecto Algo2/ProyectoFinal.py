import random
import tkinter as tk
from tkinter import font  # Importa el módulo font de tkinter para configurar fuentes
from tkinter import messagebox
from PIL import Image, ImageTk
from random import randint, choice
from math import cos, sin


class SopaDeLetras:
    def __init__(self, ventana_menu):
        self.tamaño_tablero = 10
        self.tablero = self.inicializar_tablero()
        self.letras = "AAAAABBCCCDDEEEEFFGGHIIIJKLLMMNNÑOOOOPPPQRRSSSTTUUUVWXYZ"
        self.diccionario = self.cargar_diccionario(
            "diccionario.txt"
        )  # Carga el diccionario desde un archivo
        self.palabras_encontradas = []  # Lista de palabras encontradas por el jugador
        self.ventana_menu = ventana_menu  # Referencia a la ventana del menú
        self.puntaje = 0  # Puntaje inicial del jugador
        self.tiempo_restante = 300  # Tiempo de juego en segundos (5 minutos)

    def inicializar_tablero(self):
        tablero = []
        for x in range(self.tamaño_tablero):  # Crea una matriz 10x10 vacía
            tablero.append([""] * self.tamaño_tablero)
        return tablero

    def cargar_diccionario(self, nombreArchivo):
        with open(nombreArchivo, "r") as archivo:  # Abre el archivo del diccionario
            return [
                line.strip().upper() for line in archivo.readlines()
            ]  # Carga las palabras y las convierte a mayúsculas

    def generar_tablero(self):
        for i in range(self.tamaño_tablero):
            for j in range(
                self.tamaño_tablero
            ):  # Llena el tablero con letras aleatorias
                self.tablero[i][j] = random.choice(self.letras)

    def dibujar_tablero(self):
        self.canvas.delete("all")  # Limpia el canvas
        for i in range(self.tamaño_tablero):
            for j in range(self.tamaño_tablero):
                x0 = j * 40
                y0 = i * 40
                x1 = x0 + 40
                y1 = y0 + 40
                self.canvas.create_rectangle(
                    x0, y0, x1, y1, outline="black", width=2
                )  # Dibuja los rectángulos de la cuadrícula
                self.canvas.create_text(
                    (x0 + 20, y0 + 20), text=self.tablero[i][j], font=("Arial", 12)
                )  # Dibuja las letras

    def resaltar_palabra(self, palabra, posiciones, color):
        for fila, columna in posiciones:  # Resalta las letras de la palabra encontrada
            x0 = columna * 40
            y0 = fila * 40
            x1 = x0 + 40
            y1 = y0 + 40
            self.canvas.create_rectangle(
                x0, y0, x1, y1, fill=color, outline="black", width=2
            )  # Dibuja un rectángulo de color
            self.canvas.create_text(
                (x0 + 20, y0 + 20), text=self.tablero[fila][columna], font=("Arial", 12)
            )  # Dibuja la letra

    def es_palabra_valida(self, x, y):
        return (
            0 <= x < self.tamaño_tablero and 0 <= y < self.tamaño_tablero
        )  # Verifica si la posición está dentro del tablero

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
        ]  # Coordenadas de las direcciones posibles (diagonales, verticales y horizontales)
        if contador == len(palabra):  # Si se ha encontrado la palabra completa
            return True
        if (
            not self.es_palabra_valida(x, y)
            or (x, y) in visitados
            or self.tablero[x][y] != palabra[contador]
        ):
            return False  # Si la posición no es válida o ya ha sido visitada o no coincide con la letra actual
        visitados.add((x, y))  # Marca la posición como visitada
        path.append((x, y))  # Añade la posición al camino actual
        for dx, dy in coordenadas:  # Busca en todas las direcciones posibles
            if self.buscar_palabra(
                palabra, x + dx, y + dy, contador + 1, visitados, path
            ):
                return True
        visitados.remove((x, y))  # Desmarca la posición si no se encontró la palabra
        path.pop()  # Elimina la posición del camino actual
        return False

    def encontrar_palabra(self, palabra):
        path = []
        for i in range(self.tamaño_tablero):
            for j in range(self.tamaño_tablero):
                if (
                    self.tablero[i][j] == palabra[0]
                ):  # Empezar a buscar desde la primera letra
                    if self.buscar_palabra(palabra, i, j, 0, set(), path):
                        return path  # Retorna el camino si se encontró la palabra
        return []  # Retorna una lista vacía si no se encontró la palabra

    def ingresar_palabra(self, palabra):
        palabra = palabra.upper()  # Asegurar que la palabra esté en mayúsculas
        if palabra in self.palabras_encontradas:
            print(
                f"{palabra} ya ha sido encontrada."
            )  # Verifica si la palabra ya fue encontrada
        else:
            posiciones = self.encontrar_palabra(palabra)
            if posiciones:
                if palabra in self.diccionario:
                    self.palabras_encontradas.append(palabra)
                    self.resaltar_palabra(
                        palabra, posiciones, "lightgreen"
                    )  # Resalta la palabra en verde si está en el diccionario
                    print(f"{palabra} ha sido encontrada y está en el diccionario!")
                    self.actualizar_puntaje(len(palabra) * 10)  # Actualiza el puntaje
                else:
                    self.resaltar_palabra(
                        palabra, posiciones, "red"
                    )  # Resalta la palabra en rojo si no está en el diccionario
                    print(
                        f"{palabra} ha sido encontrada pero no está en el diccionario."
                    )
            else:
                print(f"{palabra} no está en la sopa de letras.")

    def actualizar_puntaje(self, puntos):
        self.puntaje += puntos
        self.label_puntaje.config(
            text=f"Puntaje: {self.puntaje}"
        )  # Actualiza la etiqueta del puntaje

    def actualizar_tiempo(self):
        if self.tiempo_restante > 0:
            minutos, segundos = divmod(self.tiempo_restante, 60)
            self.label_tiempo.config(
                text=f"Tiempo restante: {minutos:02d}:{segundos:02d}"
            )  # Actualiza el tiempo restante
            self.tiempo_restante -= 1
            self.ventana_juego.after(
                1000, self.actualizar_tiempo
            )  # Llama a esta función de nuevo después de 1 segundo
        else:
            self.label_tiempo.config(text="Tiempo restante: 00:00")
            self.entrada_usuario.config(
                state="disabled"
            )  # Deshabilita la entrada de usuario
            print("El tiempo se ha agotado. Fin del juego.")

    def calcular_puntaje(self):
        puntaje = 0
        for palabra in self.palabras_encontradas:
            if palabra in self.diccionario:
                puntaje += len(palabra) * 10
        return puntaje  # Calcula el puntaje total

    def enviar_palabra(self):
        palabra = (
            self.entrada_usuario.get().strip().upper()
        )  # Obtiene la palabra ingresada por el usuario
        self.ingresar_palabra(palabra)
        self.entrada_usuario.delete(0, tk.END)  # Limpia la entrada de usuario

    def volver_al_menu(self):
        self.ventana_juego.destroy()  # Cierra la ventana de juego
        self.ventana_menu.deiconify()  # Muestra la ventana del menú

    def jugar(self):
        self.ventana_menu.withdraw()  # Oculta la ventana del menú
        self.ventana_juego = tk.Toplevel(self.ventana_menu)
        self.ventana_juego.title("Sopa de Letras")
        self.ventana_juego.geometry("600x800")
        self.ventana_juego.configure(bg="#F3D0D7")

        self.label_puntaje = tk.Label(
            self.ventana_juego,
            text=f"Puntaje: {self.puntaje}",
            font=("Arial", 16),
            bg="#F3D0D7",
            fg="black",
        )
        self.label_puntaje.pack(anchor="ne", padx=10, pady=10)  # Muestra el puntaje

        self.label_tiempo = tk.Label(
            self.ventana_juego, text="", font=("Arial", 16), bg="#F3D0D7", fg="black"
        )
        self.label_tiempo.pack(
            anchor="nw", padx=10, pady=10
        )  # Muestra el tiempo restante
        self.actualizar_tiempo()

        self.canvas = tk.Canvas(self.ventana_juego, width=400, height=400, bg="white")
        self.canvas.pack(pady=20)  # Crea el canvas para el tablero

        self.generar_tablero()  # Genera el tablero de juego
        self.dibujar_tablero()  # Dibuja el tablero en el canvas

        frame = tk.Frame(self.ventana_juego, bg="#F3D0D7")
        frame.pack(pady=10)

        self.entrada_usuario = tk.Entry(frame, width=20, bg="white")
        self.entrada_usuario.pack(pady=5)  # Entrada de usuario para ingresar palabras

        boton_enviar = tk.Button(
            frame, text="Enviar", command=self.enviar_palabra, bg="purple", fg="black"
        )
        boton_enviar.pack(pady=5)  # Botón para enviar la palabra ingresada

        boton_volver_menu = tk.Button(
            frame,
            text="Volver al menú",
            command=self.volver_al_menu,
            bg="purple",
            fg="black",
        )
        boton_volver_menu.pack(pady=5)  # Botón para volver al menú

        self.ventana_juego.mainloop()  # Ejecuta el bucle principal de la ventana de juego


class BatallaNaval:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.pantalla.title("Batalla Naval")
        self.pantalla.configure(bg="light pink")
        self.cantidadceldas = 10
        self.tamanyocelda = 40
        self.canvas_size = 600  # Tamaño del canvas (600x600 píxeles)
        self.side_margin = 100  # Margen lateral para colocar los barcos
        self.start_x = (
            self.canvas_size - self.cantidadceldas * self.tamanyocelda
        ) // 2  # Coordenada x inicial para los barcos
        self.start_y = (
            self.canvas_size - self.cantidadceldas * self.tamanyocelda
        ) // 2  # Coordenada y inicial para los barcos
        self.canvas = tk.Canvas(
            self.pantalla, width=self.canvas_size * 2, height=self.canvas_size
        )  # Duplicamos el ancho del canvas
        self.canvas.pack()
        self.fondo = Image.open("FONDObatallanaval.jpg")
        self.fondo = self.fondo.resize(
            (
                self.cantidadceldas * self.tamanyocelda,
                self.cantidadceldas * self.tamanyocelda,
            ),
            Image.Resampling.LANCZOS,
        )
        self.bg_photo = ImageTk.PhotoImage(self.fondo)
        # Crear fondo para ambas grillas
        self.bg_image_id1 = self.canvas.create_image(
            0, 0, image=self.bg_photo, anchor="nw"
        )
        self.bg_image_id2 = self.canvas.create_image(
            self.canvas_size, 0, image=self.bg_photo, anchor="nw"
        )
        self.canvas.move(self.bg_image_id1, 100, self.canvas_size / 2 - 200)
        self.canvas.move(self.bg_image_id2, 100, self.canvas_size / 2 - 200)
        self.barcosfijados = set()
        self.posicionbarcos = {}
        self.angulo_barcos = {}
        self.ubicaciones_barcos = (
            []
        )  # Lista para almacenar las coordenadas de los barcos
        self.disparos_jugador = set()  # Para almacenar los disparos del jugador
        self.disparos_oponente = set()  # Para almacenar los disparos del oponente
        self.barcos_oponente = (
            []
        )  # Lista para almacenar las coordenadas de los barcos del oponente
        self.ultimo_disparo_acertado = (
            None  # Almacena la última posición del disparo acertado
        )
        self.crear_grilla(self.start_x, self.start_y)
        self.crear_grilla(
            self.start_x + self.canvas_size, self.start_y
        )  # Crear la segunda grilla a la derecha de la primera

        self.barcos = [
            {
                "coords": [
                    (10, 0),
                    (10, 1),
                    (10, 2),
                    (11, 1),
                    (12, 0),
                    (12, 1),
                    (12, 2),
                ]
            },  # Barco 1: forma de H
            {
                "coords": [
                    (11, 4),
                    (10, 5),
                    (11, 5),
                    (11, 6),
                    (12, 4),
                    (12, 5),
                    (12, 6),
                ]
            },  # Barco 2: forma rara
            {
                "coords": [(10, 8), (11, 8), (11, 9), (11, 10), (12, 10)]
            },  # Barco 3: forma rara 2
            {"coords": [(0, 10), (1, 10), (2, 10)]},  # Barco 4: horizontal
            {"coords": [(4, 10), (5, 10), (6, 10)]},  # Barco 5: horizontal
            {"coords": [(8, 10), (9, 10), (10, 10)]},  # Barco 6: horizontal
        ]
        self.current_barco = 0
        self.crear_siguiente_barco()
        self.ubicar_boton = tk.Button(
            self.pantalla, text="Ubicar barco", command=self.fijar_barco_actual
        )
        self.ubicar_boton.pack()

        # Vincula las teclas de flecha para mover los barcos
        self.pantalla.bind("<Key>", self.manejar_teclas)

        # Configurar disparo del jugador en la cuadrícula del oponente
        self.canvas.bind("<Button-1>", self.disparo_jugador)

        # Generar los barcos del oponente
        self.colocar_barcos_oponente()

        # Indicar el turno inicial
        self.turno_jugador = True
        self.barcos_ubicados = (
            False  # Nueva variable para rastrear si todos los barcos han sido ubicados
        )

    def MatrizACoordenadas(self, x, y):
        # Convierte coordenadas de matriz (x, y) a coordenadas alfanuméricas
        i = str(y + 1)  # Convierte la fila a cadena (0 se convierte en "1", 1 en "2", etc.)
        j = chr(ord("A") + x)  # Convierte la columna a letra (0 se convierte en "A", 1 en "B", etc.)
        return i, j

    def CoordenadasAMatriz(self, x, y):
        # Convierte coordenadas alfanuméricas (x, y) a coordenadas de matriz
        a = int(x) - 1  # Convierte la fila alfanumérica a índice de fila (por ejemplo, "1" a 0, "2" a 1, etc.)
        b = ord(y) - ord("A")  # Convierte la columna alfanumérica a índice de columna (por ejemplo, "A" a 0, "B" a 1, etc.)
        return a, b

    def crear_grilla(self, offset_x, offset_y):
        # Crea una cuadrícula en un canvas utilizando coordenadas y dimensiones especificadas
        for i in range(self.cantidadceldas):
            for j in range(self.cantidadceldas):
                # Calcula las coordenadas de los vértices del rectángulo para cada celda
                x1 = offset_x + i * self.tamanyocelda
                y1 = offset_y + j * self.tamanyocelda
                x2 = x1 + self.tamanyocelda
                y2 = y1 + self.tamanyocelda
                # Crea un rectángulo en el canvas para representar cada celda de la cuadrícula
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="white")
                # Agrega etiquetas de texto para las filas y columnas 
                if j == 0:
                    # Etiqueta para las letras 
                    self.canvas.create_text(
                        x1 + self.tamanyocelda / 2,
                        offset_y - 10,
                        text=chr(ord("A") + i),
                        fill="black",
                    )
                if i == 0:
                    # Etiqueta para los números
                    self.canvas.create_text(
                        offset_x - 10,
                        y1 + self.tamanyocelda / 2,
                        text=str(j + 1),
                        fill="black",
                    )

    def crear_siguiente_barco(self):
        # Verifica si todos los barcos han sido ubicados
        if self.current_barco >= len(self.barcos):
            messagebox.showinfo(
                "Todos los barcos ubicados", "Todos los barcos han sido ubicados."
            )
            return
        barco = self.barcos[self.current_barco] # Obtiene el próximo barco a ubicar
        barco["ids"] = [] # Inicializa una lista de IDs de rectángulos para este barco
        for x, y in barco["coords"]: # Itera sobre las coordenadas del barco para crear rectángulos en el canvas
            x1 = self.start_x + x * self.tamanyocelda
            y1 = self.start_y + y * self.tamanyocelda
            x2 = x1 + self.tamanyocelda
            y2 = y1 + self.tamanyocelda
            # Crea un rectángulo en el canvas para representar una parte del barco
            rect_id = self.canvas.create_rectangle(
                x1, y1, x2, y2, fill="pale violet red"
            )
            # Asocia eventos de ratón a cada rectángulo para interactuar con el barco
            self.canvas.tag_bind(rect_id, "<ButtonPress-1>", self.inicio)
            self.canvas.tag_bind(rect_id, "<B1-Motion>", self.mover)
            self.canvas.tag_bind(rect_id, "<Button-3>", self.rotar)
            barco["ids"].append(rect_id) # Guarda el ID del rectángulo en la lista de IDs del barco
        self.posicionbarcos[tuple(barco["ids"])] = barco["coords"] # Registra la posición inicial del barco en un diccionario
        self.angulo_barcos[tuple(barco["ids"])] = 0 # Inicializa el ángulo del barco en 0 y lo guarda en un diccionario

    def inicio(self, event):
         # Inicializa los datos de arrastre al comenzar a arrastrar un objeto
        self.drag_data = {"x": event.x, "y": event.y}  # Guarda la posición inicial del cursor
        self.drag_data["item"] = self.canvas.find_withtag("current")[0] # Encuentra el ID del objeto actual bajo el cursor
        self.drag_data["items"] = [self.drag_data["item"]] # Inicializa la lista de ítems a arrastrar con el objeto actual

        # Busca en los barcos para encontrar a cuál pertenece el ítem arrastrado
        for barco in self.barcos:
            if self.drag_data["item"] in barco["ids"]:
                self.drag_data["items"] = barco["ids"] # Actualiza la lista de ítems a arrastrar con todos los ítems del barco
                self.current_barco = self.barcos.index(
                    barco
                )  # Actualiza el barco actual
                break # Sale del bucle una vez encontrado el barco al que pertenece el ítem

    def mover(self, event):
        items = self.drag_data.get("items") # Obtiene la lista de ítems que están siendo arrastrados
        if items:
            delta_x = event.x - self.drag_data["x"] # Calcula el cambio en la posición x del cursor
            delta_y = event.y - self.drag_data["y"] # Calcula el cambio en la posición y del cursor
            valid_move = True # Inicializa el movimiento como válido

            # Verifica si el nuevo movimiento mantiene los ítems dentro de los límites de la cuadrícula
            for item in items:
                x1, y1, x2, y2 = self.canvas.coords(item) # Obtiene las coordenadas actuales del ítem
                new_x1 = x1 + delta_x
                new_y1 = y1 + delta_y
                new_x2 = x2 + delta_x
                new_y2 = y2 + delta_y
                # Verifica si el nuevo movimiento está fuera de los límites permitidos
                if (
                    new_x1 < self.start_x
                    or new_y1 < self.start_y
                    or new_x2 > self.start_x + self.cantidadceldas * self.tamanyocelda
                    or new_y2 > self.start_y + self.cantidadceldas * self.tamanyocelda
                ):
                    valid_move = False # Si está fuera de los límites, el movimiento no es válido
                    break
            if valid_move: # Si el movimiento es válido, mueve los ítems
                for item in items:
                    self.canvas.move(item, delta_x, delta_y)  #Mueve el ítem por delta_x y delta_y
                self.drag_data["x"] = event.x # Actualiza la posición x del cursor
                self.drag_data["y"] = event.y # Actualiza la posición y del cursor
                new_coords = []  # Actualiza las nuevas coordenadas de los ítems en la cuadrícula
                for item in items:
                    x1, y1, x2, y2 = self.canvas.coords(item) # Obtiene las nuevas coordenadas del ítem
                    new_coords.append(
                        (
                            int((x1 - self.start_x) // self.tamanyocelda), # Calcula la nueva posición x en la cuadrícula
                            int((y1 - self.start_y) // self.tamanyocelda), # Calcula la nueva posición y en la cuadrícula
                        )
                    )
                self.posicionbarcos[tuple(items)] = new_coords # Actualiza la posición de los barcos en el diccionario

    def rotar(self, event):
        item = self.canvas.find_withtag("current")[0] # Obtiene el ID del objeto actual bajo el cursor
        for barco in self.barcos:
            if item in barco["ids"]:
                items = barco["ids"] # Encuentra el barco al que pertenece el objeto y obtiene sus ítems
                break
        else:
            return # Si el objeto no pertenece a ningún barco, sale de la función
        if tuple(items) not in self.barcosfijados:
            # Incrementa el ángulo del barco en 90 grados (en sentido horario) y asegura que se mantenga dentro de 0-360 grados
            self.angulo_barcos[tuple(items)] = (
                self.angulo_barcos[tuple(items)] + 90
            ) % 360
            cx, cy = self.centro_figura(items) # Obtiene el centro del barco
            for part in items: # Rota cada parte del barco alrededor de su centro
                x1, y1, x2, y2 = self.canvas.coords(part) # Obtiene las coordenadas actuales de la parte del barco
                new_x1, new_y1 = self.rotarfig(
                    cx, cy, x1, y1, self.angulo_barcos[tuple(items)]
                ) # Rota la esquina superior izquierda
                new_x2, new_y2 = self.rotarfig(
                    cx, cy, x2, y2, self.angulo_barcos[tuple(items)]
                ) # Rota la esquina inferior derecha
                self.canvas.coords(part, new_x1, new_y1, new_x2, new_y2) # Actualiza las coordenadas de la parte del barco
            new_coords = [] # Actualiza las nuevas coordenadas de los ítems en la cuadrícula
            for part in items:
                x1, y1, x2, y2 = self.canvas.coords(part)  # Obtiene las nuevas coordenadas de la parte del barco
                new_coords.append(
                    (
                        int((x1 - self.start_x) // self.tamanyocelda), # Calcula la nueva posición x en la cuadrícula
                        int((y1 - self.start_y) // self.tamanyocelda), # Calcula la nueva posición y en la cuadrícula
                    )
                )
            self.posicionbarcos[tuple(items)] = new_coords # Actualiza la posición del barco en el diccionario

    def centro_figura(self, items):
        coords = [self.canvas.coords(item) for item in items] # Obtiene las coordenadas de cada ítem en la lista items
        x_coords = [x1 for x1, y1, x2, y2 in coords] + [x2 for x1, y1, x2, y2 in coords] # Extrae todas las coordenadas x1 y x2 en una lista
        y_coords = [y1 for x1, y1, x2, y2 in coords] + [y2 for x1, y1, x2, y2 in coords] # Extrae todas las coordenadas y1 y y2 en una lista
        return sum(x_coords) / len(x_coords), sum(y_coords) / len(y_coords) # Calcula y devuelve el centro de la figura

    def rotarfig(self, cx, cy, x, y, angle):
        angle = angle * 3.14159265 / 180.0 # Convierte el ángulo de grados a radianes

        # Calcula las nuevas coordenadas (nx, ny) después de la rotación
        nx = cos(angle) * (x - cx) - sin(angle) * (y - cy) + cx 
        ny = sin(angle) * (x - cx) + cos(angle) * (y - cy) + cy
        return nx, ny # Devuelve las nuevas coordenadas

    def barcosNoadyacentes(self):
        N = len(self.ubicaciones_barcos) # Obtiene el número de barcos en la lista de ubicaciones
        if N <= 1:
            return True #Si no hay barcos o solo hay uno, no puede haber adyacencia

        nuevas_coordenadas = self.ubicaciones_barcos[N - 1] # Obtiene las coordenadas del último barco añadido

        for ubicac in range(N - 1):  # Recorre todos los barcos excepto el último
            comparar = self.ubicaciones_barcos[ubicac] # Obtiene las coordenadas del barco actual a comparar
            # Compara cada coordenada del nuevo barco con cada coordenada de los barcos anteriores
            for coord_nueva in nuevas_coordenadas:
                for coord_comparar in comparar:
                    x1, y1 = coord_nueva    # Coordenadas de la nueva ubicación
                    x2, y2 = coord_comparar # Coordenadas a comparar

                    # Verificar si las coordenadas son adyacentes en cualquier dirección y que no esté colocado en el mismo lugar que otro barco
                    if (
                        (x1 == x2 and y1 == y2)
                        or abs(x1 - x2) <= 1
                        and abs(y1 - y2) <= 1
                    ):
                        return False  # Hay barcos adyacentes

        return True  # No hay barcos adyacentes

    def fijar_barco_actual(self):
        if self.current_barco < len(self.barcos): # Verifica si hay un barco actual a fijar
            items = tuple(self.barcos[self.current_barco]["ids"]) # Obtiene los IDs de las partes del barco actual
            if items not in self.barcosfijados: # Verifica si el barco actual no está ya fijado
                coords = [self.canvas.coords(item) for item in items] # Obtiene las coordenadas de las partes del barco
                # Verifica que todas las partes del barco estén dentro de la cuadrícula
                all_inside = all(
                    self.start_x
                    <= x1
                    < self.start_x + self.cantidadceldas * self.tamanyocelda
                    and self.start_y
                    <= y1
                    < self.start_y + self.cantidadceldas * self.tamanyocelda
                    and self.start_x
                    <= x2
                    <= self.start_x + self.cantidadceldas * self.tamanyocelda
                    and self.start_y
                    <= y2
                    <= self.start_y + self.cantidadceldas * self.tamanyocelda
                    for x1, y1, x2, y2 in coords
                )
                if all_inside:
                    self.ajustar_a_cuadricula(items) # Ajusta las partes del barco a la cuadrícula
                    # Convierte las coordenadas de la cuadrícula a coordenadas de la matriz
                    coordenadas = [
                        self.MatrizACoordenadas(x, y)
                        for x, y in self.posicionbarcos[items]
                    ]
                    coord_str = ", ".join([f"{i}{j}" for i, j in coordenadas])
                    # Agregar las coordenadas temporalmente
                    self.ubicaciones_barcos.append(self.posicionbarcos[items]) # Agrega las coordenadas del barco a la lista temporalmente

                    if self.barcosNoadyacentes(): # Verifica que los barcos no sean adyacentes
                        self.barcosfijados.add(items) # Fija el barco actual
                        # Cambia el color del barco a 'pink' y desactiva los eventos de movimiento y rotación
                        for item in items:
                            self.canvas.itemconfig(item, fill="pink")
                            self.canvas.tag_unbind(item, "<ButtonPress-1>")
                            self.canvas.tag_unbind(item, "<B1-Motion>")
                            self.canvas.tag_unbind(item, "<Button-3>")
                        print(f"Barco fijado en la posición {coord_str}")
                        self.current_barco += 1 #Incrementa el índice del barco actual
                        if self.current_barco == len(self.barcos):
                            self.barcos_ubicados = (
                                True  # Todos los barcos han sido ubicados
                            )
                        self.crear_siguiente_barco() # Crea el siguiente barco
                    else:
                        # Si no son válidas, quitar las coordenadas agregadas temporalmente
                        self.ubicaciones_barcos.pop()
                        messagebox.showwarning(
                            "Movimiento Inválido",
                            "El barco no puede estar al lado de otro",
                        )
                else:
                    messagebox.showwarning(
                        "Movimiento Inválido",
                        "El barco no puede ser fijado fuera de la cuadrícula.",
                    )

    def ajustar_a_cuadricula(self, items):
        # Ajusta las coordenadas de cada parte del barco a la cuadrícula
        for item in items:
            # Obtiene las coordenadas actuales de la parte del barco
            x1, y1, x2, y2 = self.canvas.coords(item)
            # Calcula la nueva coordenada x1 ajustada a la cuadrícula
            new_x1 = (
                round((x1 - self.start_x) / self.tamanyocelda) * self.tamanyocelda
                + self.start_x
            )
            # Calcula la nueva coordenada y1 ajustada a la cuadrícula
            new_y1 = (
                round((y1 - self.start_y) / self.tamanyocelda) * self.tamanyocelda
                + self.start_y
            )
            # Calcula las nuevas coordenadas x2 y y2 basadas en el tamaño de la celda
            new_x2 = new_x1 + self.tamanyocelda
            new_y2 = new_y1 + self.tamanyocelda
            self.canvas.coords(item, new_x1, new_y1, new_x2, new_y2) # Actualiza las coordenadas de la parte del barco en el canvas
        new_coords = [] # Lista para almacenar las nuevas coordenadas ajustadas
        # Actualiza las nuevas coordenadas ajustadas para cada parte del barco
        for item in items:
            x1, y1, x2, y2 = self.canvas.coords(item)
            new_coords.append(
                (
                    int((x1 - self.start_x) // self.tamanyocelda),
                    int((y1 - self.start_y) // self.tamanyocelda),
                )
            )
        self.posicionbarcos[tuple(items)] = new_coords # Actualiza la posición del barco con las nuevas coordenadas ajustadas

    def manejar_teclas(self, event):
        # Obtiene las partes del barco actual. Si no hay barcos, retorna una lista vacía.
        items = (
            self.barcos[self.current_barco]["ids"]
            if self.current_barco < len(self.barcos)
            else []
        )
        # Si no hay partes de barco, no hace nada y retorna.
        if not items:
            return

        delta_x, delta_y = 0, 0  # Inicializa los deltas de movimiento en cero.
        # Ajusta los deltas de movimiento según la tecla presionada.
        if event.keysym == "Left": 
            delta_x = -self.tamanyocelda # Movimiento hacia la izquierda
        elif event.keysym == "Right":    
            delta_x = self.tamanyocelda  # Movimiento hacia la derecha
        elif event.keysym == "Up":
            delta_y = -self.tamanyocelda #Movimiento hacia arriba
        elif event.keysym == "Down":
            delta_y = self.tamanyocelda # Movimiento hacia abajo

        valid_move = True # Inicializa la variable para verificar si el movimiento es válido.
        # Verifica si el movimiento propuesto mantiene todas las partes del barco dentro de la cuadrícula.
        for item in items:
            x1, y1, x2, y2 = self.canvas.coords(item) # Obtiene las coordenadas actuales del item
            new_x1 = x1 + delta_x # Calcula la nueva coordenada x1
            new_y1 = y1 + delta_y # Calcula la nueva coordenada y1
            new_x2 = x2 + delta_x # Calcula la nueva coordenada x2
            new_y2 = y2 + delta_y # Calcula la nueva coordenada y2

            # Verifica si las nuevas coordenadas están dentro de los límites permitidos de la cuadrícula
            if (
                new_x1 < self.start_x
                or new_y1 < self.start_y
                or new_x2 > self.start_x + self.cantidadceldas * self.tamanyocelda
                or new_y2 > self.start_y + self.cantidadceldas * self.tamanyocelda
            ):
                valid_move = False
                break # Si alguna coordenada está fuera de los límites, el movimiento no es válido
        
        # Si el movimiento es válido, mueve las partes del barco                
        if valid_move:
            for item in items:
                self.canvas.move(item, delta_x, delta_y) # Mueve el item en el canvas
            new_coords = [] # Actualiza las coordenadas del barco en la posición de la cuadrícula.
            for item in items:
                x1, y1, x2, y2 = self.canvas.coords(item) # Obtiene las nuevas coordenadas del item
                new_coords.append(
                    (
                        int((x1 - self.start_x) // self.tamanyocelda), # Calcula la nueva coordenada x en la cuadrícula
                        int((y1 - self.start_y) // self.tamanyocelda), # Calcula la nueva coordenada y en la cuadrícula
                    )
                )
            self.posicionbarcos[tuple(items)] = new_coords # Actualiza la posición del barco en la cuadrícula

    def colocar_barcos_oponente(self):
        posicionbarcos_oponente = {}

        # Formas de los barcos basadas en las coordenadas proporcionadas
        formas_barcos = [
            [(0, 0), (0, 1), (0, 2), (1, 1), (2, 0), (2, 1), (2, 2)],  # Forma de H
            [(1, 4), (0, 5), (1, 5), (1, 6), (2, 4), (2, 5), (2, 6)],  # Forma rara
            [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)],  # Forma rara 2
            [(0, 0), (1, 0), (2, 0)],  # Horizontal 3x1
            [(0, 0), (1, 0), (2, 0)],  # Horizontal 3x1
            [(0, 0), (1, 0), (2, 0)],  # Horizontal 3x1
        ]

        for forma in formas_barcos:
            colocado = False
            while not colocado:
                dx, dy = choice([(0, 1), (1, 0)])  # Dirección horizontal o vertical
                if dx == 0:  # Vertical
                    start_x = randint(0, self.cantidadceldas - 1)
                    start_y = randint(0, self.cantidadceldas - max(y for x, y in forma))
                else:  # Horizontal
                    start_x = randint(0, self.cantidadceldas - max(x for x, y in forma))
                    start_y = randint(0, self.cantidadceldas - 1)

                new_coords = [(start_x + x, start_y + y) for x, y in forma]

                if self.verificar_espacio_libre(new_coords, posicionbarcos_oponente):
                    # Agregar las coordenadas del barco del oponente
                    self.barcos_oponente.append(new_coords)
                    posicionbarcos_oponente[tuple(new_coords)] = new_coords
                    colocado = True

        self.posicionbarcos.update(posicionbarcos_oponente)

    def verificar_espacio_libre(self, new_coords, posicionbarcos):
        # Recorre cada coordenada (x, y) en new_coords
        for x, y in new_coords:
            # Verifica si (x, y) está fuera de los límites de la cuadrícula
            if x < 0 or x >= self.cantidadceldas or y < 0 or y >= self.cantidadceldas:
                return False # Si está fuera de los límites, retorna False
            
            # Recorre las coordenadas de todos los barcos ya posicionados
            for coords in posicionbarcos.values():
                for cx, cy in coords:
                    # Verifica si la coordenada (x, y) está adyacente (o en la misma posición) a alguna coordenada (cx, cy)
                    if abs(cx - x) <= 1 and abs(cy - y) <= 1:
                        return False # Si está adyacente, retorna False       
        return True # Si ninguna coordenada (x, y) está fuera de los límites ni adyacente a un barco ya posicionado, retorna True

    def disparo_jugador(self, event):
        if not self.turno_jugador or not self.barcos_ubicados:
            return

        x, y = event.x, event.y

        # Asegurarse de que el disparo esté en la grilla del oponente
        if x < self.canvas_size:
            return

        # Convertir las coordenadas del clic a coordenadas de la cuadrícula
        grid_x = (x - self.start_x - self.canvas_size) // self.tamanyocelda
        grid_y = (y - self.start_y) // self.tamanyocelda

        # Verificar que las coordenadas estén dentro de los límites de la cuadrícula
        if (
            grid_x < 0
            or grid_x >= self.cantidadceldas
            or grid_y < 0
            or grid_y >= self.cantidadceldas
        ):
            return

        if (grid_x, grid_y) in self.disparos_jugador:
            return  # Ya se disparó en esta celda

        self.disparos_jugador.add((grid_x, grid_y))
        x1 = self.start_x + grid_x * self.tamanyocelda + self.canvas_size
        y1 = self.start_y + grid_y * self.tamanyocelda
        x2 = x1 + self.tamanyocelda
        y2 = y1 + self.tamanyocelda

        if self.colision_con_barco((grid_x, grid_y), self.barcos_oponente):
            self.canvas.create_text(
                (x1 + x2) / 2,
                (y1 + y2) / 2,
                text="X",
                fill="red",
                font=("Helvetica", 24, "bold"),
            )  # Impacto en el barco del oponente
        else:
            self.canvas.create_text(
                (x1 + x2) / 2,
                (y1 + y2) / 2,
                text="*",
                fill="blue",
                font=("Helvetica", 24, "bold"),
            )  # Agua

        self.turno_jugador = False
        self.check_game_over()
        self.pantalla.after(1000, self.disparo_oponente)

    def disparo_oponente(self):
        if not self.barcos_ubicados: # No realiza disparos si los barcos no han sido ubicados aún
            return

        if self.ultimo_disparo_acertado:
            # Si el último disparo fue acertado, intenta disparar en posiciones adyacentes
            grid_x, grid_y = self.ultimo_disparo_acertado
            posibles_disparos = [
                (grid_x - 1, grid_y),
                (grid_x + 1, grid_y),
                (grid_x, grid_y - 1),
                (grid_x, grid_y + 1),
            ]
            # Filtra las posiciones válidas que no han sido disparadas aún
            posibles_disparos = [
                (x, y)
                for x, y in posibles_disparos
                if 0 <= x < self.cantidadceldas
                and 0 <= y < self.cantidadceldas
                and (x, y) not in self.disparos_oponente
            ]
            if posibles_disparos: 
                grid_x, grid_y = choice(posibles_disparos) # Elige una posición aleatoria de las válidas
            else:
                # Si no hay posiciones adyacentes disponibles, reinicia aleatoriamente
                self.ultimo_disparo_acertado = None
                grid_x = randint(0, self.cantidadceldas - 1)
                grid_y = randint(0, self.cantidadceldas - 1)
                while (grid_x, grid_y) in self.disparos_oponente:
                    grid_x = randint(0, self.cantidadceldas - 1)
                    grid_y = randint(0, self.cantidadceldas - 1)
        else:
            # Si no hay último disparo acertado, dispara aleatoriamente
            grid_x = randint(0, self.cantidadceldas - 1)
            grid_y = randint(0, self.cantidadceldas - 1)
            while (grid_x, grid_y) in self.disparos_oponente:
                grid_x = randint(0, self.cantidadceldas - 1)
                grid_y = randint(0, self.cantidadceldas - 1)

        # Registra el disparo realizado por el oponente
        self.disparos_oponente.add((grid_x, grid_y))
        x1 = self.start_x + grid_x * self.tamanyocelda
        y1 = self.start_y + grid_y * self.tamanyocelda
        x2 = x1 + self.tamanyocelda
        y2 = y1 + self.tamanyocelda

        # Verifica si el disparo impacta en un barco del jugador o no
        if self.colision_con_barco((grid_x, grid_y), self.ubicaciones_barcos):
            self.canvas.create_text(
                (x1 + x2) / 2,
                (y1 + y2) / 2,
                text="X",
                fill="red",
                font=("Helvetica", 24, "bold"),
            )  # Impacto en el barco del jugador
            self.ultimo_disparo_acertado = (grid_x, grid_y)
        else:
            self.canvas.create_text(
                (x1 + x2) / 2,
                (y1 + y2) / 2,
                text="*",
                fill="blue",
                font=("Helvetica", 24, "bold"),
            )  # Agua

        self.turno_jugador = True # Cambia el turno al jugador después de disparar
        self.check_game_over() # Verifica si el juego ha terminado después de cada disparo

    def colision_con_barco(self, coordenada_disparo, barcos):
        # Verifica si la coordenada de disparo coincide con alguna coordenada de barco en la lista de barcos
        for barco in barcos:
            if coordenada_disparo in barco:
                return True # Retorna True si hay una colisión (el disparo impacta en un barco)
        return False # Retorna False si no hay colisión (el disparo es agua)

    def check_game_over(self):
        # Verifica si alguno de los jugadores ha perdido todos sus barcos
        if self.verificar_derrota(self.barcos_oponente, self.disparos_jugador):
            self.mostrar_mensaje_final("¡Ganaste!")
        elif self.verificar_derrota(self.ubicaciones_barcos, self.disparos_oponente):
            self.mostrar_mensaje_final("¡Perdiste!")

    def verificar_derrota(self, barcos, disparos):
        # Verificar si todos los barcos han sido hundidos
        return all(all(coord in disparos for coord in barco) for barco in barcos)

    def mostrar_mensaje_final(self, mensaje):
        messagebox.showinfo("Fin del juego", mensaje)
        self.pantalla.quit()

# Función para iniciar la sopa de letras
def iniciar_sopa_de_letras():
    juego = SopaDeLetras(ventana_menu)
    juego.jugar()  # Inicia el juego de sopa de letras


# Función para iniciar la batalla naval
def iniciar_batalla_naval():
    # Ocultar la ventana del menú principal
    ventana_menu.withdraw()
    
    # Crear la ventana del juego
    ventana_juego = tk.Toplevel()
    ventana_juego.title("Batalla Naval")
    ventana_juego.geometry("1200x12000")
    ventana_juego.configure(bg="#F3D0D7")
    
    # Iniciar la instancia del juego
    juego = BatallaNaval(ventana_juego)
    
    # Botón para volver al menú principal desde la ventana del juego
    boton_volver_menu = tk.Button(
        ventana_juego,
        text="Volver al menú",
        command=lambda: [ventana_juego.destroy(), ventana_menu.deiconify()],
        bg="purple",
        fg="black",
    )
    boton_volver_menu.pack(pady=20)
    
    # Ejecutar el bucle principal de la ventana del juego
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