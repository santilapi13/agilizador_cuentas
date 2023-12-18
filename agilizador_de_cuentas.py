import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter
from CTkListbox import *
from CTkMessagebox import CTkMessagebox
import random
import csv

ARCHIVO_PRECIOS = "precios.csv"

class App:
    def __init__(self):
        self.root= customtkinter.CTk()
        self.root.resizable(False, False)
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        self.root.title("Agilizador de cuentas")
        self.root.geometry("970x640")

        self.buttons = []

        self.billetes_recibidos = [[10, 0], [20, 0], [50, 0], [100, 0], [200, 0], [500, 0], [1000, 0], [2000, 0]]
        self.billetes_seleccionados = [[10, 0], [20, 0], [50, 0], [100, 0], [200, 0], [500, 0], [1000, 0], [2000, 0]]
        self.labels_billetes_seleccionados = []
        self.valor_a_cobrar = 0
        self.valor_recibido = 0
        self.precios = []
        self.cargar_precios()

        self.create_ui()
    
    def cargar_precios(self):
        with open(ARCHIVO_PRECIOS, encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                self.precios.append(int(row[1].replace('$', '').replace(',', '.')))
        print(self.precios)

    def generar_problema(self):
        self.valor_a_cobrar = 0
        for i in range(random.randint(1, 3)):
            precios_unicos = list(set(self.precios))
            self.valor_a_cobrar += random.choice(precios_unicos)
        self.label_cobrar.configure(text="Cobrar: $" + str(self.valor_a_cobrar))

        self.valor_recibido = 0
        self.billetes_recibidos = [[10, 0], [20, 0], [50, 0], [100, 0], [200, 0], [500, 0], [1000, 0], [2000, 0]]

        valor_redondo = (self.valor_a_cobrar // 1000) * 1000
        centenas = ((self.valor_a_cobrar - valor_redondo) // 100) * 100
        billetes_dosmil = valor_redondo / 2000
        # Si no es múltiplo de 2000, agrego 1 billete de 1000 o 2 de 500
        if billetes_dosmil != valor_redondo // 2000:
            como_pagan = random.randint(0, 1)
            if como_pagan == 0:
                self.billetes_recibidos[6][1] += 1
            elif como_pagan == 1:
                self.billetes_recibidos[5][1] += 2

        # Luego, agrego billetes de 2000, 1000 o 500 hasta llegar a cubrir el valor redondo
        for i in range(valor_redondo // 2000):
            como_pagan = random.randint(0, 2)
            if como_pagan == 0:
                self.billetes_recibidos[7][1] += 1
            elif como_pagan == 1:
                self.billetes_recibidos[6][1] += 2
            elif como_pagan == 2:
                self.billetes_recibidos[5][1] += 4

        # Agrego 1 billete de 500 o 1 de 1000. 
        if centenas < 500:
            self.billetes_recibidos[5][1] += 1
        else:
            self.billetes_recibidos[6][1] += 1

        for billete in self.billetes_recibidos:
            self.valor_recibido += billete[0] * billete[1]

        self.como_pagan.configure(text=f"Te pagan con:\n{self.billetes_recibidos[7][1]} de $2000\n{self.billetes_recibidos[6][1]} de $1000\n{self.billetes_recibidos[5][1]} de $500")
        
    def enviar_solucion(self):
        pass

    def restar_billete(self, tipo_billete):
        if self.billetes_seleccionados[tipo_billete][1] <= 0:
            return
        
        self.billetes_seleccionados[tipo_billete][1] -= 1
        self.labels_billetes_seleccionados[tipo_billete].configure(text=str(self.billetes_seleccionados[tipo_billete][1]))

    def sumar_billete(self, tipo_billete):
        self.billetes_seleccionados[tipo_billete][1] += 1
        self.labels_billetes_seleccionados[tipo_billete].configure(text=str(self.billetes_seleccionados[tipo_billete][1]))


    def create_ui(self):
        self.root.configure(padx=10, pady=10)

        # Contenedor de todos los elementos
        self.contenedor1 = customtkinter.CTkFrame(self.root, width=950, height=600)
        self.contenedor1.pack_propagate(False)
        self.contenedor1.grid(row=0, column=0, padx=10, pady=10)

        # 2 subcontenedores para organizar los elementos

        self.sub_contenedor1 = customtkinter.CTkFrame(self.contenedor1)
        self.sub_contenedor1.pack(side="top", expand=True, fill="both")
        self.sub_contenedor1.pack(pady=0)

        self.sub_contenedor2 = customtkinter.CTkFrame(self.contenedor1)
        self.sub_contenedor2.pack(side="top", expand=True, fill="both")
        self.sub_contenedor2.pack(pady=5)
        
        # Contenido subcontenedor superior: 

        self.button_generar = customtkinter.CTkButton(
            self.sub_contenedor1,
            text="Generar",
            font=("Verdana", 20),
            command=self.generar_problema,
        )
        self.button_generar.pack(pady=25)


        self.label_cobrar = customtkinter.CTkLabel(
            self.sub_contenedor1,
            text="Cobrar: -",
            font=("Verdana", 20),
        )
        self.label_cobrar.pack(pady=10, padx=20, side=customtkinter.LEFT)

        self.como_pagan = customtkinter.CTkLabel(
            self.sub_contenedor1,
            text="Te pagan con: -",
            font=("Verdana", 20),
        )
        self.como_pagan.pack(
            pady=10, padx=15, side=customtkinter.RIGHT
        )

        # Contenido subcontenedor inferior

        self.label_seleccionar_vuelto = customtkinter.CTkLabel(
            self.sub_contenedor2,
            text="Seleccionar vuelto",
            font=("Verdana", 20),
            wraplength=400,
        )
        self.label_seleccionar_vuelto.pack(pady=10, side=customtkinter.TOP)

        self.sub_contenedor_billetes = customtkinter.CTkFrame(self.sub_contenedor2)
        self.sub_contenedor_billetes.pack(side="top", expand=True, fill="both")
        self.sub_contenedor_billetes.pack(pady=5)

        # Fila superior: Valores de los billetes
        for columna in range(8):
            billete_label = customtkinter.CTkLabel(
                self.sub_contenedor_billetes,
                text=str(self.billetes_seleccionados[columna][0]),
                font=("Verdana", 20),
            )
            billete_label.grid(row=0, column=1+columna*3, padx=5, pady=30)

        # Fila inferior: Cantidades y botones
        for columna in range(8):
            button_restar = customtkinter.CTkButton(
                self.sub_contenedor_billetes,
                text="-",
                font=("Verdana", 20),
                width=2,
                height=1,
                command=lambda tipo_billete=columna: self.restar_billete(tipo_billete),
            )
            button_restar.grid(row=1, column=columna*3, padx=15, pady=10)

            label_cantidad = customtkinter.CTkLabel(
                self.sub_contenedor_billetes,
                text=str(self.billetes_seleccionados[columna][1]),
                font=("Verdana", 20),
            )
            label_cantidad.grid(row=1, column=columna*3+1, padx=2, pady=10)
            self.labels_billetes_seleccionados.append(label_cantidad)

            button_sumar = customtkinter.CTkButton(
                self.sub_contenedor_billetes,
                text="+",
                font=("Verdana", 20),
                width=3,
                height=2,
                command=lambda tipo_billete=columna: self.sumar_billete(tipo_billete),
            )
            button_sumar.grid(row=1, column=columna*3+2, padx=2, pady=10)

        self.button_enviar = customtkinter.CTkButton(
            self.sub_contenedor2,
            text="Enviar",
            font=("Verdana", 20),
            command=self.enviar_solucion,
        )
        self.button_enviar.pack(pady=25)


    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()