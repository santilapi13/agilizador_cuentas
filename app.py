import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter
from CTkListbox import *
from CTkMessagebox import CTkMessagebox
import random
import csv

PRICES_FILE = "prices.csv"

class App:
    def __init__(self):
        self.root= customtkinter.CTk()
        self.root.resizable(False, False)
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        self.root.title("Agilizador de cuentas")
        self.root.geometry("970x640")

        self.buttons = []

        self.received_bills = [[10, 0], [20, 0], [50, 0], [100, 0], [200, 0], [500, 0], [1000, 0], [2000, 0]]
        self.selected_bills = [[10, 0], [20, 0], [50, 0], [100, 0], [200, 0], [500, 0], [1000, 0], [2000, 0]]
        self.labels_selected_bills = []
        self.to_charge_value = 0
        self.received_value = 0
        self.prices = []
        self.load_prices()

        self.create_ui()
    
    def load_prices(self):
        with open(PRICES_FILE, encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                self.prices.append(int(row[1].replace('$', '').replace(',', '.')))
        print(self.prices)

    def generate_problem(self):
        self.to_charge_value = 0
        while self.to_charge_value == 0 or self.to_charge_value > 25000:
            self.to_charge_value = 0
            for i in range(random.randint(1, 3)):
                prices_unicos = list(set(self.prices))
                self.to_charge_value += random.choice(prices_unicos)
            self.label_cobrar.configure(text="Cobrar: $" + str(self.to_charge_value))

        self.received_value = 0
        self.received_bills = [[10, 0], [20, 0], [50, 0], [100, 0], [200, 0], [500, 0], [1000, 0], [2000, 0]]

        whole_value = (self.to_charge_value // 1000) * 1000
        centenas = ((self.to_charge_value - whole_value) // 100) * 100
        two_thousand_bills = whole_value / 2000
        # Si no es múltiplo de 2000, agrego 1 billete de 1000 o 2 de 500
        if two_thousand_bills != whole_value // 2000:
            payment_method = random.randint(0, 5)
            if payment_method < 4:
                self.received_bills[6][1] += 1
            else:
                self.received_bills[5][1] += 2

        # Luego, agrego billetes de 2000, 1000 o 500 hasta llegar a cubrir el valor redondo
        for i in range(whole_value // 2000):
            payment_method = random.randint(0, 10)
            if payment_method < 6:
                self.received_bills[7][1] += 1
            elif payment_method < 10:
                self.received_bills[6][1] += 2
            else:
                self.received_bills[5][1] += 4

        # Agrego 1 billete de 500 o 1 de 1000. 
        if centenas < 500:
            self.received_bills[5][1] += 1
        else:
            self.received_bills[6][1] += 1

        for bill in self.received_bills:
            self.received_value += bill[0] * bill[1]

        self.payment_method.configure(text=f"Te pagan con:\n{self.received_bills[7][1]} de $2000\n{self.received_bills[6][1]} de $1000\n{self.received_bills[5][1]} de $500")
        
    def send_solution(self):
        real_change = self.received_value - self.to_charge_value

        for bill in self.selected_bills:
            real_change -= bill[0] * bill[1]
        
        if real_change != 0:
            CTkMessagebox(title="Error", message="El vuelto indicado no es correcto", icon="cancel")
            return
        
        CTkMessagebox(title="¡Bien!", message="El vuelto indicado es correcto", icon="check")
        self.received_bills = [[10, 0], [20, 0], [50, 0], [100, 0], [200, 0], [500, 0], [1000, 0], [2000, 0]]
        self.selected_bills = [[10, 0], [20, 0], [50, 0], [100, 0], [200, 0], [500, 0], [1000, 0], [2000, 0]]
        self.to_charge_value = 0
        self.received_value = 0
        for bill_type in range(8):
            self.labels_selected_bills[bill_type].configure(text=str(self.selected_bills[bill_type][1]))
        self.generate_problem()

    def substract_bill(self, bill_type):
        if self.selected_bills[bill_type][1] <= 0:
            return
        
        self.selected_bills[bill_type][1] -= 1
        self.labels_selected_bills[bill_type].configure(text=str(self.selected_bills[bill_type][1]))

    def add_bill(self, bill_type):
        self.selected_bills[bill_type][1] += 1
        self.labels_selected_bills[bill_type].configure(text=str(self.selected_bills[bill_type][1]))


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
            command=self.generate_problem,
        )
        self.button_generar.pack(pady=25)


        self.label_cobrar = customtkinter.CTkLabel(
            self.sub_contenedor1,
            text="Cobrar: -",
            font=("Verdana", 20),
        )
        self.label_cobrar.pack(pady=10, padx=20, side=customtkinter.LEFT)

        self.payment_method = customtkinter.CTkLabel(
            self.sub_contenedor1,
            text="Te pagan con: -",
            font=("Verdana", 20),
        )
        self.payment_method.pack(
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
                text=str(self.selected_bills[columna][0]),
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
                command=lambda bill_type=columna: self.substract_bill(bill_type),
            )
            button_restar.grid(row=1, column=columna*3, padx=15, pady=10)

            label_cantidad = customtkinter.CTkLabel(
                self.sub_contenedor_billetes,
                text=str(self.selected_bills[columna][1]),
                font=("Verdana", 20),
            )
            label_cantidad.grid(row=1, column=columna*3+1, padx=2, pady=10)
            self.labels_selected_bills.append(label_cantidad)

            button_sumar = customtkinter.CTkButton(
                self.sub_contenedor_billetes,
                text="+",
                font=("Verdana", 20),
                width=3,
                height=2,
                command=lambda bill_type=columna: self.add_bill(bill_type),
            )
            button_sumar.grid(row=1, column=columna*3+2, padx=2, pady=10)

        self.button_enviar = customtkinter.CTkButton(
            self.sub_contenedor2,
            text="Enviar",
            font=("Verdana", 20),
            command=self.send_solution,
        )
        self.button_enviar.pack(pady=25)


    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()