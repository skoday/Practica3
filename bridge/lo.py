from nlp.models import Create_model, Adjust_Document
from nlp.normalization import Normalization
import matplotlib.pyplot as plt
from pandas.plotting import table
import subprocess
import pandas as pd

class Bridge:

    def __init__(self, corpus, documentos, parametros) -> None:
        self.corpus = corpus
        self.documentos = documentos
        self.parametros = parametros


    def guardar_pdf(self, dfs):
        """
        self.documentos: es un data frame con n documetnos (registros)
        dfs: es una lista de n dataframes, y cada uno tiene una correspondencia
        con cada documetno de self.documentos
        """
        fig, axs = plt.subplots(len(dfs), figsize=(8, 5 * len(dfs)))

        for i, df in enumerate(dfs):
            # Crear una tabla para cada DataFrame y agregarla a su respectivo subplot
            tabla = table(axs[i], df, loc='upper center')

            # Ocultar los ejes
            axs[i].axis('off')

            # Establecer el formato de las tablas
            tabla.auto_set_font_size(False)
            tabla.set_fontsize(10)
            tabla.scale(1.2, 1.2)

        plt.tight_layout()

        plt.savefig('documentos.pdf', bbox_inches='tight', pad_inches=0.05)

        subprocess.Popen(['xdg-open', 'documentos.pdf'])


    def procesar_envio(self):
        #Normalizando documentos
        normalizer = Normalization(self.documentos)
        documentos_normalizados = normalizer.normalize()

        #Creando modelo
        model_selector = Create_model(self.corpus)

        model = None

        opciones_modelo = {
            "binary": model_selector.binary,
            "frequency": model_selector.frequency,
            "tfidf": model_selector.tfidf
        }

        if self.parametros[0] in opciones_modelo:
            model = opciones_modelo[self.parametros[0]](self.parametros[1], self.parametros[2])
        else:
            print("Parámetro de modelo no válido")

        adjustment = Adjust_Document(model, documentos_normalizados, self.corpus, self.parametros[2])
        simuilitudes = adjustment.compare()
        #print(simuilitudes)

        return simuilitudes
        #self.guardar_pdf(simuilitudes)

    def procesar_todo(self):

        dataframes = []

        for mode in ["binary", "frequency", "tfidf"]:
            for num in [1, 2]:
                for field in ["Título", "Contenido", "Título-Contenido"]:
                    bridge = Bridge(self.corpus, self.documentos, [mode, num, field])
                    similitudes = bridge.procesar_envio()
                    for elemento in similitudes:
                        elemento["Tipo"] = mode
                        elemento["ngram"] = num
                        elemento["Comparación"] = field

                    dataframes.append(similitudes)           

        dataframes_concatenados = []

        for i in range(len(self.documentos)):
            lista = [elemento[i] for elemento in dataframes]
            aux =  pd.concat(lista, axis = 0)
            aux.sort_values(by='Similarity', ascending=False, inplace=True)
            dataframes_concatenados.append(aux.head(10))

        #for elemento in dataframes_concatenados:
        #    elemento.sort_values(by='Similarity', ascending=False, inplace=True)
        #    elemento = elemento.head(10)

        return dataframes_concatenados