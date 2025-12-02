import tkinter as tk
from tkinter import messagebox

class BattleshipGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Batalla Naval")
        
        self.board_size = 10  # Tamaño del tablero (10x10)
        self.cell_size = 40   # Tamaño de cada celda (40 píxeles)
        self.canvas_size = 600  # Tamaño del canvas (600x600 píxeles)
        self.side_margin = 100  # Margen lateral para colocar los barcos
        self.start_x = (self.canvas_size - self.board_size * self.cell_size) // 2  # Coordenada x inicial para los barcos
        self.start_y = (self.canvas_size - self.board_size * self.cell_size) // 2  # Coordenada y inicial para los barcos

        # Crear un canvas donde se dibujará el tablero
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()  # Añadir el canvas a la ventana

        # Inicializar el conjunto de barcos fijos y un diccionario para guardar sus posiciones
        self.fixed_ships = set()
        self.ship_positions = {}

        self.draw_grid()  # Dibujar la cuadrícula del tablero
        self.create_ships()  # Crear y colocar los barcos fuera del tablero

        # Crear un botón para fijar los barcos en sus posiciones actuales
        self.fix_button = tk.Button(self.root, text="Fijar Barcos", command=self.fix_ships)
        self.fix_button.pack()  # Añadir el botón a la ventana

    def draw_grid(self):
        # Dibujar una cuadrícula en el canvas
        for i in range(self.board_size):
            for j in range(self.board_size):
                x1 = self.start_x + i * self.cell_size
                y1 = self.start_y + j * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")


    def create_ships(self):
        # Definir los barcos con sus coordenadas iniciales (fuera del tablero)
        self.ships = [
            {"coords": [(10, 0), (10, 1), (10, 2), (11, 1), (12, 0), (12, 1), (12, 2)]},  # Barco 1: forma de H
            {"coords": [(11, 4), (10, 5), (11, 5),(11,6), (12,4), (12,5), (12,6)]},  # Barco 2: forma rara
            {"coords": [(10, 8), (11,8), (11,9), (11,10), (12,10)]},  # Barco 3: forma rara 2
            {"coords": [(0, 10), (1, 10), (2, 10)]},  # Barco 4: horizontal
            {"coords": [(4, 10), (5, 10), (6, 10)]},  # Barco 5: horizontal
            {"coords": [(8, 10), (9, 10), (10, 10)]},  # Barco 6: horizontal
        ]

        for ship in self.ships:
            ship["ids"] = []
            for (x, y) in ship["coords"]:
                x1 = self.start_x + x * self.cell_size
                y1 = self.start_y + y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill="gray")
                self.canvas.tag_bind(rect_id, "<ButtonPress-1>", self.on_start)
                self.canvas.tag_bind(rect_id, "<B1-Motion>", self.on_drag)
                ship["ids"].append(rect_id)
            self.ship_positions[tuple(ship["ids"])] = ship["coords"]

    def on_start(self, event):
        self.drag_data = {"x": event.x, "y": event.y}
        current_item = self.canvas.find_withtag("current")[0]
        for ship_ids in self.ship_positions.keys():
            if current_item in ship_ids:
                self.drag_data["items"] = ship_ids
                break

    def on_drag(self, event):
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
                if new_x1 < self.start_x or new_y1 < self.start_y or new_x2 > self.start_x + self.board_size * self.cell_size or new_y2 > self.start_y + self.board_size * self.cell_size:
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
                    new_coords.append((int((x1 - self.start_x) // self.cell_size), int((y1 - self.start_y) // self.cell_size)))
                self.ship_positions[items] = new_coords

    def fix_ships(self):
        for ship_ids, coords in self.ship_positions.items():
            if not any(item in self.fixed_ships for item in ship_ids):
                for item in ship_ids:
                    self.fixed_ships.add(item)
                    self.canvas.itemconfig(item, fill="darkgray")
                messagebox.showinfo("Fijar Barco", f"Barco {ship_ids} fijado en la posición {coords}")
                print(f"Barco {ship_ids} fijado en la posición {coords}")
    
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
    root = tk.Tk()
    game = BattleshipGame(root)
    root.mainloop()