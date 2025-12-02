import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class BatallaNaval:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.pantalla.title("Batalla Naval")
        self.cantidadceldas = 10
        self.tamanyocelda = 40 
        self.canvas = tk.Canvas(self.pantalla, width=(self.cantidadceldas+5)*self.tamanyocelda,
                                height=self.cantidadceldas*self.tamanyocelda)
        self.canvas.pack()  
        self.fondo = Image.open("C:\\Users\\Usuario\\OneDrive\\Escritorio\\Proyecto Algo2\\WhatsApp Image 2024-06-06 at 3.42.01 PM.jpeg")
        self.fondo = self.fondo.resize(((self.cantidadceldas+5)*self.tamanyocelda, self.cantidadceldas*self.tamanyocelda), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.fondo)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        self.barcosfijados = set()
        self.posicionbarcos = {}  
        self.angulo_barcos = {}
        self.creargrilla()
        self.crearbarcos()
        self.ubicarboton = tk.Button(self.pantalla, text="ubicar Barcos", command=self.fijar_barcos)
        self.ubicarboton.pack()
    
    def creargrilla(self):
        for i in range(self.cantidadceldas):
            for j in range(self.cantidadceldas):
                self.canvas.create_rectangle(i*self.tamanyocelda, j*self.tamanyocelda,
                                             (i+1)*self.tamanyocelda, (j+1)*self.tamanyocelda, outline="white")
                
    def crearbarcos(self):
        self.barcos = [
            {"coords": [(10, 0), (10, 1), (10, 2), (11, 1), (12, 0), (12, 1), (12, 2)]},  # Barco 1: forma de H
            {"coords": [(11, 4), (10, 5), (11, 5),(11,6), (12,4), (12,5), (12,6)]},  # Barco 2: forma rara
            {"coords": [(10, 8), (11,8), (11,9), (11,10), (12,10)]},  # Barco 3: forma rara 2
            {"coords": [(0, 10), (1, 10), (2, 10)]},  # Barco 4: horizontal
            {"coords": [(4, 10), (5, 10), (6, 10)]},  # Barco 5: horizontal
            {"coords": [(8, 10), (9, 10), (10, 10)]},  # Barco 6: horizontal
        ]

        for barco in self.barcos:
            # Convertir las coordenadas de celdas a coordenadas de píxeles
            x1, y1, x2, y2 = [c*self.tamanyocelda for c in barco["coords"]]
            # Dibujar el barco en el canvas como un rectángulo
            barco["id"] = self.canvas.create_rectangle(x1, y1, x2 + self.tamanyocelda, y2 + self.tamanyocelda, fill="pink")
            # Hacer que el barco sea interactivo (se pueda arrastrar y rotar)
            self.canvas.tag_bind(barco["id"], "<ButtonPress-1>", self.inicio)
            self.canvas.tag_bind(barco["id"], "<B1-Motion>", self.mover)
            self.canvas.tag_bind(barco["id"], "<Button-3>", self.rotar)
            # Guardar la posición inicial del barco en el diccionario
            self.posicionbarcos[barco["id"]] = barco["coords"]
            self.angulo_barcos[barco["id"]] = 0

    def inicio(self, event):
        # Guardar las coordenadas iniciales del ratón al empezar a arrastrar
        self.drag_data = {"x": event.x, "y": event.y}
        # Guardar el identificador del elemento que se está arrastrando
        self.drag_data["item"] = self.canvas.find_withtag("current")[0]

    def mover(self, event):
        item = self.drag_data.get("item")
        # Solo mover el barco si no está fijo
        if item and item not in self.barcosfijados:
            # Calcular el desplazamiento
            delta_x = event.x - self.drag_data["x"]
            delta_y = event.y - self.drag_data["y"]
            # Obtener las coordenadas actuales del barco
            x1, y1, x2, y2 = self.canvas.coords(item)
            # Calcular nuevas coordenadas
            new_x1 = x1 + delta_x
            new_y1 = y1 + delta_y
            new_x2 = x2 + delta_x
            new_y2 = y2 + delta_y
            # Verificar que las nuevas coordenadas no estén fuera del tablero
            if new_x1 >= 0 and new_y1 >= 0 and new_x2 <= self.cantidadceldas * self.tamanyocelda and new_y2 <= self.cantidadceldas * self.tamanyocelda:
                # Mover el barco en el canvas
                self.canvas.move(item, delta_x, delta_y)
                # Actualizar las coordenadas del ratón
                self.drag_data["x"] = event.x
                self.drag_data["y"] = event.y
                # Actualizar la posición del barco en la matriz
                self.posicionbarcos[item] = [int(new_x1 // self.tamanyocelda), int(new_y1 // self.tamanyocelda), int(new_x2 // self.tamanyocelda), int(new_y2 // self.tamanyocelda) - 1]

    def rotar(self, event):
        item = self.drag_data.get("item")
        if item and item not in self.barcosfijados:
            # Rotar el barco 90 grados
            self.angulo_barcos[item] = (self.angulo_barcos[item] + 90) % 360
            x1, y1, x2, y2 = self.canvas.coords(item)
            # Calcular el nuevo tamaño del barco después de la rotación
            new_x1, new_y1, new_x2, new_y2 = girarfigura(x1, y1, x2, y2, self.angulo_barcos[item])
            # Ajustar las nuevas coordenadas del barco en el canvas
            self.canvas.coords(item, new_x1, new_y1, new_x2, new_y2)
            # Actualizar la posición del barco en la matriz
            self.posicionbarcos[item] = [int(new_x1 // self.tamanyocelda), int(new_y1 // self.tamanyocelda), int(new_x2 // self.tamanyocelda), int(new_y2 // self.tamanyocelda) - 1]
    
    def fijar_barcos(self):
        # Fijar todos los barcos en sus posiciones actuales
        for item in self.posicionbarcos.keys():
            if item not in self.barcosfijados:
                self.barcosfijados.add(item)
                self.canvas.itemconfig(item, fill="pink")
                messagebox.showinfo("Ubicar Barco", f"Barco {item} fijado en la posición {self.posicionbarcos[item]}")
                # Mostrar la posición fijada en la consola
                print(f"Barco {item} fijado en la posición {self.posicionbarcos[item]}")

def girarfigura(x1, y1, x2, y2, angle):
    width = x2 - x1
    height = y2 - y1

    if angle == 90:
        return x1, y1, x1 + height, y1 + width
    elif angle == 180:
        return x1, y1, x1 + width, y1 + height
    elif angle == 270:
        return x1, y1, x1 + height, y1 + width
    else:  # angle == 0
        return x1, y1, x1 + width, y1 + height

if __name__ == "__main__":
    pantalla = tk.Tk()
    game = BatallaNaval(pantalla)
    pantalla.mainloop()
