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


    def guardar_pdf(self, documentos_originales, documentos_similares):
        """
                        AQUI ES DONDE SE DEBE IMPLEMENTAR

        Consideraciones: Para nosotros aqui un documento es el texto de entrada al que le
            queremos buscar a registros similares del corpus, lo cual es lo que paso el profesor.
            En la interfaz del programa corriendo "python main.py" podras ver que hay un cuadro de
            texto. Cada renglón en ese cuadro de texto es un documento, por lo cual puedes poner solo
            uno o varios documentos y el programa te dara los 10 similares para cada uno de ellos.

            Otra cosa a considerar es que enlistar los documentos en la interfaz no lo considere en el
            primer momento por la poca versatilidad que tendria mostrar las tablas, por lo cual opte pore
            por que se produjiera un pdf final que cuando este listo se abra automaticamente, para eso es el
            modulo se subprocess que importe, pero como como ven no esta usado.

        Funcionamiento: Tiene varios botones, el primero "Cargar CSV", este boton abrirar una ventana
            para que puedas seleccionar el corpus que sea, pero en este caso es el que esta en la carpeta
            raiz de este programa, una vez seleccionado es momento de escribir documentos en en el cuadro
            de texto (tomar a consideración lo de arriba), recuerda, cada que haces un salto de linea es 
            un documento diferente.

            Despues seccionas las caracteristicas que quieras en los tres menus dropdown a la derecha
            del cuadro de texto, luego le aumentamos los ngramas si quieren.

            Eentonces ya puedes presionar "Enviar" y lo que va a a pasar es que por cada documento que
            pusiste en el cuadro de texto se buscaran los 10 registros mas similares en el corpues
            con las caracteristicas especificadas. Mira, si pusiste 3 textos diferentes (recuerda cada
            renglón es un documento) se generara una lista con 3 datagrames, cada uno con los 10 registros
            del corpues más similares a cada uno de tus documentos.

            El boton que queda es "Comparar todo", este boton ignorara los parametros que seleccionaste en los
            menus dropdown y va a generar todas las posibles combinaciones posibles
            (3 tipos de representción * 2 diferente gramas * 3 difeentes partes a comprarar = 27) que son 27.
            Entonces por cada documento ingresado regresara un dataframe con los 10 registros del corpues
            más parecidos. 

        Parametros: 
        * documentos_originales: es una lista la cual contiene los documetnos puestos en el recuadro de texto
        * documentos_similares: es una lista con los dataframes, cada uno con los 10 elementos más parecidos
            a cada documento.

            COnsideraciones aqui: NO IMPORTA SI SOLO INGRESASTE UN DOCUMENTO SIEMPRE SERAN LISTAS LAS QUE SE
            RECIBEN EN ESTA FUNCIÓN. Entonces por ejemplo si te pusieron un documento en el cuadro de texto
            cada parametro tendra una lista con un solo elemento, entonces tendrias que accesar al indice 0 de
            cada lista para obtener el elemento. Y si se pusiern n documentos en el cuadro de texto, pues se
            reciben listas de n elementos en cada dataframe, recuerda los elementos son rexpectivos, lo que
            que significa que cada documetno tiene su tabla de registros similares en el mismo indice, pero en 
            el otro parametro.

            RECUERDA: cada lista contiene dataframes, por lo que cada documento en la variavble documentos_originales y
                cada tabla con elementos similares en documentos_similares es un dataframe. Esto lo hice para que
                se facilite el proceso de crear el pdf, y no haya que crear la tabla con reportlab, por lo que 
                puedes buscar como pasar dataframes a pdf en googgle  o preguntar a chatpgt o bard:)

            OTRA ACLARACIÓN: las unica columna en los dataframes que estan en documentos_originales se llama: "Documento".
                Y las columnas de los otros dataframe en documentos_similares son:
                ['Fuente', 'Título', 'Contenido', 'Sección', 'Url', 'Fecha',
                'Título-Contenido', 'Similarity', 'Vector representation',
                'Extracted features', 'Comparison element']

                Les deje todos los atributos para que pudieras elegir los necesarios para el pdf,
                en el pdf de la practica 3 que mando el profesor esta cuales columnas son relevantes.

                Sin nada más por el momento eso es todo, caulquier duda pregunta, para implementar esto
                con la informción que te di es suficiente, ire documentando el resto de codigo y tal vez
                un diagrama de flujo para que entiendan como sirve, de mientras que ir avanzando,
                Por cierto como les dije generado el pdf lo pueden abrir con subprocess con el abredor
                de pdf prededeterminado del dispositivo.

            PARA PROBAR:
                En la carpeta UI esta el archivo interface.py, en el casi hasta abajo hay dos funciones,
                sus nombres son "comparar_todo" y "comparar_todo", dentro de cada una de ellas hay
                una linea que es la que se debe descomentar para que esta fución se use, la linea es
                la misma en cada función "enlace.guardar_pdf(df, respuesta)" solo descomentala,
                y recuerda, siempre ejecuta todo desde el archvio main.py en la carpeta raíz por que
                si no te dara error en los modulos. Eso es todo, suerte


            Por cierto a veces cuando u renglon no es suficiente para un documento solo el cuadro de texto
            lo partira para que se ajuste, ustedes no hagan un salto de linea explicito a menos que sea otro
            documento
        """
        pass

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