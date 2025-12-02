import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from random import *
from math import cos, sin


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
        self.ubicaciones_barcos = []  # Lista para almacenar las coordenadas de los barcos
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

    def MatrizACoordenadas(self, x, y):
        i = str(y + 1)
        j = chr(ord("A") + x)
        return i, j

    def CoordenadasAMatriz(self, x, y):
        a = int(x) - 1
        b = ord(y) - ord("A")
        return a, b

    def crear_grilla(self, offset_x, offset_y):
        for i in range(self.cantidadceldas):
            for j in range(self.cantidadceldas):
                x1 = offset_x + i * self.tamanyocelda
                y1 = offset_y + j * self.tamanyocelda
                x2 = x1 + self.tamanyocelda
                y2 = y1 + self.tamanyocelda
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="white")
                if j == 0:
                    self.canvas.create_text(
                        x1 + self.tamanyocelda / 2,
                        offset_y - 10,
                        text=chr(ord("A") + i),
                        fill="black",
                    )
                if i == 0:
                    self.canvas.create_text(
                        offset_x - 10,
                        y1 + self.tamanyocelda / 2,
                        text=str(j + 1),
                        fill="black",
                    )

    def crear_siguiente_barco(self):
        if self.current_barco >= len(self.barcos):
            messagebox.showinfo(
                "Todos los barcos ubicados", "Todos los barcos han sido ubicados."
            )
            return
        barco = self.barcos[self.current_barco]
        barco["ids"] = []
        for x, y in barco["coords"]:
            x1 = self.start_x + x * self.tamanyocelda
            y1 = self.start_y + y * self.tamanyocelda
            x2 = x1 + self.tamanyocelda
            y2 = y1 + self.tamanyocelda
            rect_id = self.canvas.create_rectangle(
                x1, y1, x2, y2, fill="pale violet red"
            )
            self.canvas.tag_bind(rect_id, "<ButtonPress-1>", self.inicio)
            self.canvas.tag_bind(rect_id, "<B1-Motion>", self.mover)
            self.canvas.tag_bind(rect_id, "<Button-3>", self.rotar)
            barco["ids"].append(rect_id)
        self.posicionbarcos[tuple(barco["ids"])] = barco["coords"]
        self.angulo_barcos[tuple(barco["ids"])] = 0

    def inicio(self, event):
        self.drag_data = {"x": event.x, "y": event.y}
        self.drag_data["item"] = self.canvas.find_withtag("current")[0]
        self.drag_data["items"] = [self.drag_data["item"]]

        for barco in self.barcos:
            if self.drag_data["item"] in barco["ids"]:
                self.drag_data["items"] = barco["ids"]
                self.current_barco = self.barcos.index(
                    barco
                )  # Actualiza el barco actual
                break

    def mover(self, event):
        items = self.drag_data.get("items")
        if items:
            delta_x = event.x - self.drag_data["x"]
            delta_y = event.y - self.drag_data["y"]
            valid_move = True
            for item in items:
                x1, y1, x2, y2 = self.canvas.coords(item)
                new_x1 = x1 + delta_x
                new_y1 = y1 + delta_y
                new_x2 = x2 + delta_x
                new_y2 = y2 + delta_y
                if (
                    new_x1 < self.start_x
                    or new_y1 < self.start_y
                    or new_x2 > self.start_x + self.cantidadceldas * self.tamanyocelda
                    or new_y2 > self.start_y + self.cantidadceldas * self.tamanyocelda
                ):
                    valid_move = False
                    break
            if valid_move:
                for item in items:
                    self.canvas.move(item, delta_x, delta_y)
                self.drag_data["x"] = event.x
                self.drag_data["y"] = event.y
                new_coords = []
                for item in items:
                    x1, y1, x2, y2 = self.canvas.coords(item)
                    new_coords.append(
                        (
                            int((x1 - self.start_x) // self.tamanyocelda),
                            int((y1 - self.start_y) // self.tamanyocelda),
                        )
                    )
                self.posicionbarcos[tuple(items)] = new_coords

    def rotar(self, event):
        item = self.canvas.find_withtag("current")[0]
        for barco in self.barcos:
            if item in barco["ids"]:
                items = barco["ids"]
                break
        else:
            return
        if tuple(items) not in self.barcosfijados:
            self.angulo_barcos[tuple(items)] = (
                self.angulo_barcos[tuple(items)] + 90
            ) % 360
            cx, cy = self.centro_figura(items)
            for part in items:
                x1, y1, x2, y2 = self.canvas.coords(part)
                new_x1, new_y1 = self.rotarfig(
                    cx, cy, x1, y1, self.angulo_barcos[tuple(items)]
                )
                new_x2, new_y2 = self.rotarfig(
                    cx, cy, x2, y2, self.angulo_barcos[tuple(items)]
                )
                self.canvas.coords(part, new_x1, new_y1, new_x2, new_y2)
            new_coords = []
            for part in items:
                x1, y1, x2, y2 = self.canvas.coords(part)
                new_coords.append(
                    (
                        int((x1 - self.start_x) // self.tamanyocelda),
                        int((y1 - self.start_y) // self.tamanyocelda),
                    )
                )
            self.posicionbarcos[tuple(items)] = new_coords

    def centro_figura(self, items):
        coords = [self.canvas.coords(item) for item in items]
        x_coords = [x1 for x1, y1, x2, y2 in coords] + [x2 for x1, y1, x2, y2 in coords]
        y_coords = [y1 for x1, y1, x2, y2 in coords] + [y2 for x1, y1, x2, y2 in coords]
        return sum(x_coords) / len(x_coords), sum(y_coords) / len(y_coords)

    def rotarfig(self, cx, cy, x, y, angle):
        angle = angle * 3.14159265 / 180.0
        nx = cos(angle) * (x - cx) - sin(angle) * (y - cy) + cx
        ny = sin(angle) * (x - cx) + cos(angle) * (y - cy) + cy
        return nx, ny
    
    def barcosNoadyacentes(self):
        N = len(self.ubicaciones_barcos)
        if N <= 1:
            return True

        nuevas_coordenadas = self.ubicaciones_barcos[N-1]

        for ubicac in range(N-1):  # Recorre todos los barcos excepto el último
            comparar = self.ubicaciones_barcos[ubicac]

            for coord_nueva in nuevas_coordenadas:
                for coord_comparar in comparar:
                    x1, y1 = coord_nueva
                    x2, y2 = coord_comparar

                    # Verificar si las coordenadas son adyacentes en cualquier dirección y que no esté colocado en el mismo lugar que otro barco
                    if (x1 == x2 and y1 == y2) or abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                        return False  # Hay barcos adyacentes

        return True  # No hay barcos adyacentes

    def fijar_barco_actual(self):
        if self.current_barco < len(self.barcos):
            items = tuple(self.barcos[self.current_barco]["ids"])
            if items not in self.barcosfijados:
                coords = [self.canvas.coords(item) for item in items]
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
                    self.ajustar_a_cuadricula(items)
                    coordenadas = [
                        self.MatrizACoordenadas(x, y)
                        for x, y in self.posicionbarcos[items]
                    ]
                    coord_str = ", ".join([f"{i}{j}" for i, j in coordenadas])
                    # Agregar las coordenadas temporalmente
                    self.ubicaciones_barcos.append(self.posicionbarcos[items])
                    
                    if self.barcosNoadyacentes():
                        self.barcosfijados.add(items)
                        for item in items:
                            self.canvas.itemconfig(item, fill="pink")
                            self.canvas.tag_unbind(item, "<ButtonPress-1>")
                            self.canvas.tag_unbind(item, "<B1-Motion>")
                            self.canvas.tag_unbind(item, "<Button-3>")
                        messagebox.showinfo(
                            "Barco Ubicado", f"Barco fijado en la posición {coord_str}"
                        )
                        print(f"Barco fijado en la posición {coord_str}")
                        self.current_barco += 1
                        self.crear_siguiente_barco()
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
        for item in items:
            x1, y1, x2, y2 = self.canvas.coords(item)
            new_x1 = (
                round((x1 - self.start_x) / self.tamanyocelda) * self.tamanyocelda
                + self.start_x
            )
            new_y1 = (
                round((y1 - self.start_y) / self.tamanyocelda) * self.tamanyocelda
                + self.start_y
            )
            new_x2 = new_x1 + self.tamanyocelda
            new_y2 = new_y1 + self.tamanyocelda
            self.canvas.coords(item, new_x1, new_y1, new_x2, new_y2)
        new_coords = []
        for item in items:
            x1, y1, x2, y2 = self.canvas.coords(item)
            new_coords.append(
                (
                    int((x1 - self.start_x) // self.tamanyocelda),
                    int((y1 - self.start_y) // self.tamanyocelda),
                )
            )
        self.posicionbarcos[tuple(items)] = new_coords

    def manejar_teclas(self, event):
        items = (
            self.barcos[self.current_barco]["ids"]
            if self.current_barco < len(self.barcos)
            else []
        )
        if not items:
            return

        delta_x, delta_y = 0, 0
        if event.keysym == "Left":
            delta_x = -self.tamanyocelda
        elif event.keysym == "Right":
            delta_x = self.tamanyocelda
        elif event.keysym == "Up":
            delta_y = -self.tamanyocelda
        elif event.keysym == "Down":
            delta_y = self.tamanyocelda

        valid_move = True
        for item in items:
            x1, y1, x2, y2 = self.canvas.coords(item)
            new_x1 = x1 + delta_x
            new_y1 = y1 + delta_y
            new_x2 = x2 + delta_x
            new_y2 = y2 + delta_y
            if (
                new_x1 < self.start_x
                or new_y1 < self.start_y
                or new_x2 > self.start_x + self.cantidadceldas * self.tamanyocelda
                or new_y2 > self.start_y + self.cantidadceldas * self.tamanyocelda
            ):
                valid_move = False
                break

        if valid_move:
            for item in items:
                self.canvas.move(item, delta_x, delta_y)
            new_coords = []
            for item in items:
                x1, y1, x2, y2 = self.canvas.coords(item)
                new_coords.append(
                    (
                        int((x1 - self.start_x) // self.tamanyocelda),
                        int((y1 - self.start_y) // self.tamanyocelda),
                    )
                )
            self.posicionbarcos[tuple(items)] = new_coords

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

        for barco, forma in zip(self.barcos_oponente, formas_barcos):
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
                    # No dibujar los barcos en el canvas, solo almacenar las coordenadas
                    posicionbarcos_oponente[tuple(new_coords)] = new_coords
                    colocado = True

        self.posicionbarcos.update(posicionbarcos_oponente)

    def verificar_espacio_libre(self, new_coords, posicionbarcos):
        for x, y in new_coords:
            if x < 0 or x >= self.cantidadceldas or y < 0 or y >= self.cantidadceldas:
                return False
            for coords in posicionbarcos.values():
                for cx, cy in coords:
                    if abs(cx - x) <= 1 and abs(cy - y) <= 1:
                        return False
        return True


# Configurar la ventana principal
root = tk.Tk()
app = BatallaNaval(root)
root.mainloop()