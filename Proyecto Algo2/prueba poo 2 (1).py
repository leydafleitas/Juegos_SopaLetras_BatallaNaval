import tkinter as tk
from tkinter import messagebox
#from PIL import Image, ImageTk
from random import randint
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
        self.start_x = (self.canvas_size - self.cantidadceldas * self.tamanyocelda) // 2 # Coordenada x inicial para los barcos
        self.start_y = (self.canvas_size - self.cantidadceldas * self.tamanyocelda) // 2 # Coordenada y inicial para los barcos
        self.canvas = tk.Canvas(self.pantalla, width=self.canvas_size,
                                            height=self.canvas_size)
        self.canvas.pack()  
        #self.fondo = Image.open(r"C:\Users\Andy Núñez\Downloads\photo1717364836.jpeg") 
        #self.fondo = self.fondo.resize((self.cantidadceldas * self.tamanyocelda, self.cantidadceldas * self.tamanyocelda), Image.Resampling.LANCZOS)
        #self.bg_photo = ImageTk.PhotoImage(self.fondo)
        #self.bg_image_id = self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw") 
        #self.canvas.move(self.bg_image_id, 100, self.canvas_size / 2 - 200)
        self.barcosfijados = set()
        self.posicionbarcos = {}  
        self.angulo_barcos = {}
        self.crear_grilla()
        self.crear_barcos()
        self.ubicar_boton = tk.Button(self.pantalla, text="Fijar Barcos", command=self.fijar_barcos)
        self.ubicar_boton.pack()

    def MatrizACoordenadas(self, x, y):
        # Cambiar de [columna, fila] a [fila, columna]
        j = str(y + 1)
        i = chr(ord('A') + x)
        return j, i

    def CoordenadasAMatriz(self, x, y):
        # Cambiar de [columna, fila] a [fila, columna]
        b = int(y) - 1
        a = ord(x) - ord('A')
        return a, b

    def crear_grilla(self):
        for i in range(self.cantidadceldas):
            for j in range(self.cantidadceldas):
                x1 = self.start_x + i * self.tamanyocelda
                y1 = self.start_y + j * self.tamanyocelda
                x2 = x1 + self.tamanyocelda
                y2 = y1 + self.tamanyocelda
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="white")
                if j == 0:
                    self.canvas.create_text(x1 + self.tamanyocelda / 2, self.start_y - 10, text=chr(ord('A') + i), fill="black")
                if i == 0:
                    self.canvas.create_text(self.start_x - 10, y1 + self.tamanyocelda / 2, text=str(j + 1), fill="black")

    def crear_barcos(self):
        self.barcos = [
            {"coords": [(10, 0), (10, 1), (10, 2), (11, 1), (12, 0), (12, 1), (12, 2)]},  # Barco 1: forma de H
            {"coords": [(11, 4), (10, 5), (11, 5), (11, 6), (12, 4), (12, 5), (12, 6)]},  # Barco 2: forma rara
            {"coords": [(10, 8), (11, 8), (11, 9), (11, 10), (12, 10)]},  # Barco 3: forma rara 2
            {"coords": [(0, 10), (1, 10), (2, 10)]},  # Barco 4: horizontal
            {"coords": [(4, 10), (5, 10), (6, 10)]},  # Barco 5: horizontal
            {"coords": [(8, 10), (9, 10), (10, 10)]},  # Barco 6: horizontal
        ]

        for barco in self.barcos:
            barco["ids"] = []
            for (x, y) in barco["coords"]:
                x1 = self.start_x + x * self.tamanyocelda
                y1 = self.start_y + y * self.tamanyocelda
                x2 = x1 + self.tamanyocelda
                y2 = y1 + self.tamanyocelda
                rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill="pale violet red")
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
                if new_x1 < self.start_x or new_y1 < self.start_y or new_x2 > self.start_x + self.cantidadceldas * self.tamanyocelda or new_y2 > self.start_y + self.cantidadceldas * self.tamanyocelda:
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
                    new_coords.append((int((x1 - self.start_x) // self.tamanyocelda), int((y1 - self.start_y) // self.tamanyocelda)))
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
            self.angulo_barcos[tuple(items)] = (self.angulo_barcos[tuple(items)] + 90) % 360
            cx, cy = self.centro_figura(items)
            for part in items:
                x1, y1, x2, y2 = self.canvas.coords(part)
                new_x1, new_y1 = self.rotarfig(cx, cy, x1, y1, self.angulo_barcos[tuple(items)])
                new_x2, new_y2 = self.rotarfig(cx, cy, x2, y2, self.angulo_barcos[tuple(items)])
                self.canvas.coords(part, new_x1, new_y1, new_x2, new_y2)
            new_coords = []
            for part in items:
                x1, y1, x2, y2 = self.canvas.coords(part)
                new_coords.append((int((x1 - self.start_x) // self.tamanyocelda), int((y1 - self.start_y) // self.tamanyocelda)))
            self.posicionbarcos[tuple(items)] = new_coords

    def centro_figura(self, items):
        x_coords = []
        y_coords = []
        for item in items:
            x1, y1, x2, y2 = self.canvas.coords(item)
            x_coords.extend([(x1 + x2) / 2])
            y_coords.extend([(y1 + y2) / 2])
        return sum(x_coords) / len(x_coords), sum(y_coords) / len(y_coords)

    def rotarfig(self, cx, cy, x, y, angle):
        angle_rad = angle * 3.14159 / 180  # Convertir a radianes
        cos_val = cos(angle_rad)
        sin_val = sin(angle_rad)
        dx = x - cx
        dy = y - cy
        new_x = cx + dx * cos_val - dy * sin_val
        new_y = cy + dx * sin_val + dy * cos_val
        return new_x, new_y

    def actualizar_coordenadas_logicas(self, items):
        new_coords = []
        for item in items:
            x1, y1, x2, y2 = self.canvas.coords(item)
            new_coords.append((int((x1 - self.start_x) // self.tamanyocelda), int((y1 - self.start_y) // self.tamanyocelda)))
        self.posicionbarcos[tuple(items)] = new_coords

    def fijar_barcos(self):
        if self.barcos_actuales:
            items = self.barcos_actuales["ids"]
            if tuple(items) not in self.barcosfijados:
                # Verificar si las coordenadas del barco actual están disponibles
                if self.verificar_disponibilidad(items):
                    self.barcosfijados.append(tuple(items))
                    coordenadas = [self.MatrizACoordenadas(x, y) for x, y in self.posicionbarcos[tuple(items)]]
                    coord_str = ', '.join([f'{i}{j}' for i, j in coordenadas])
                    for item in items:
                        self.canvas.itemconfig(item, fill="pink")  
                        self.canvas.tag_unbind(item, "<ButtonPress-1>")
                        self.canvas.tag_unbind(item, "<B1-Motion>")
                        self.canvas.tag_unbind(item, "<Button-3>")
                    messagebox.showinfo("Ubicar Barco", f"Barco fijado en la posición {coord_str}")
                    print(f"Barco fijado en la posición {coord_str}")
                else:
                    messagebox.showwarning("Error", "El barco está en una posición ocupada o adyacente a otro barco fijado.")


if __name__ == "__main__":
    pantalla = tk.Tk()
    game = BatallaNaval(pantalla)
    pantalla.mainloop()
