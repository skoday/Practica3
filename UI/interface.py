import tkinter as tk
from tkinter import filedialog
import pandas as pd
from bridge.lo import Bridge

class Interfaz:
    def __init__(self, master):
        self.corpus = None

        self.master = master
        self.master.title("Interfaz")
        self.master.geometry("800x600")  # Ajustar el tamaño de la ventana principal

        self.frame_csv = tk.Frame(self.master)
        self.frame_csv.pack(pady=10)
        self.btn_cargar_csv = tk.Button(self.frame_csv, text="Cargar CSV", command=self.cargar_csv)
        self.btn_cargar_csv.pack(side=tk.LEFT)

        self.frame_inputs = tk.Frame(self.master)
        self.frame_inputs.pack(pady=10)
        self.txt_input = tk.Text(self.frame_inputs, width=70, height=15)  # Ajustar el tamaño del cuadro de texto
        self.txt_input.pack(padx=5, side=tk.LEFT)

        opciones_1 = ["binary", "frequency", "tfidf"]
        opciones_2 = ["1", "2", "3"]
        opciones_3 = ["Título", "Contenido", "Título-Contenido"]

        self.dropdown_1 = tk.StringVar(self.master)
        self.dropdown_1.set(opciones_1[0])
        self.menu_1 = tk.OptionMenu(self.frame_inputs, self.dropdown_1, *opciones_1)
        self.menu_1.pack(padx=5, side=tk.LEFT)

        self.dropdown_2 = tk.StringVar(self.master)
        self.dropdown_2.set(opciones_2[0])
        self.menu_2 = tk.OptionMenu(self.frame_inputs, self.dropdown_2, *opciones_2)
        self.menu_2.pack(padx=5, side=tk.LEFT)

        self.dropdown_3 = tk.StringVar(self.master)
        self.dropdown_3.set(opciones_3[0])
        self.menu_3 = tk.OptionMenu(self.frame_inputs, self.dropdown_3, *opciones_3)
        self.menu_3.pack(padx=5, side=tk.LEFT)

        self.btn_enviar = tk.Button(self.master, text="Enviar", command=self.enviar)
        self.btn_enviar.pack(pady=10)

        self.btn_comparar_todo = tk.Button(self.master, text="Comparar todo", command=self.comparar_todo)
        self.btn_comparar_todo.pack(pady=10)

    def cargar_csv(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.corpus = pd.read_csv(filepath)

    def enviar(self):
        opcion_1 = self.dropdown_1.get()
        opcion_2 = int(self.dropdown_2.get())
        opcion_3 = self.dropdown_3.get()
        texto = self.txt_input.get("1.0", tk.END)

        lineas_limpias = [linea.strip() for linea in texto.split("\n") if linea.strip()] 
        data = {"Documento": lineas_limpias}
        df = pd.DataFrame(data)
        print(self.corpus)
        enlace = Bridge(self.corpus, df, [opcion_1, opcion_2, opcion_3])
        respuesta = enlace.procesar_envio()
        print(respuesta)

    def comparar_todo(self):

        texto = self.txt_input.get("1.0", tk.END)
        lineas_limpias = [linea.strip() for linea in texto.split("\n") if linea.strip()] 
        data = {"Documento": lineas_limpias}
        df = pd.DataFrame(data)

        enlace = Bridge(self.corpus, df, [])
        respuesta = enlace.procesar_todo()

        print(respuesta)


def iniciar_interfaz():
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()
