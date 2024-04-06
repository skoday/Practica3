from nlp.models import Create_model, Adjust_Document
from nlp.normalization import Normalization
import matplotlib.pyplot as plt
from pandas.plotting import table
import subprocess
import pandas as pd
import numpy as np

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer


class Bridge:

    def __init__(self, corpus, documentos, parametros) -> None:
        self.corpus = corpus
        self.documentos = documentos
        self.parametros = parametros


    def guardar_pdf(self, documentos_originales, documentos_similares):
        # Columnas requeridas para la practica
        columnas_practica = ['Vector representation', 'Extracted features',
                             'Comparison element', 'Similarity']
        
        columnas_practica_final = ['Documento','Vector representation', 'Extracted features',
                             'Comparison element', 'Similarity']
        # Destilando las columnas requeridas por cada df en documentos_similares
        documentos_similares_usables = [element[columnas_practica] for element in documentos_similares]
        """
        for element in documentos_similares_usables:
            element["Similarity"] = np.round(element["Similarity"], 5)
            """

        
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        
        
        pdf_filename = "documentos.pdf"
        pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)
        story = []
        
        
        for i in range(len(documentos_originales)):
            
            fila_originales = documentos_originales.iloc[[i]].values.tolist()[0]
            df_similares = documentos_similares_usables[i].copy()
            
            tabla_originales = Table([["Documento"], fila_originales])
            tabla_originales.setStyle(style)
            story.append(tabla_originales)
            story.append(Spacer(1, 12))

            df_similares["Documento"] = df_similares.index
            df_similares = df_similares[columnas_practica_final]
            
            tabla_similares = Table([columnas_practica_final] + df_similares.values.tolist())
            tabla_similares.setStyle(style)
            story.append(tabla_similares)
            story.append(Spacer(1, 12))

        pdf.build(story)
        subprocess.run(['xdg-open', pdf_filename])

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
                        elemento["Vector representation"] = mode
                        elemento["Extracted features"] = num
                        elemento["Comparison element"] = field

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