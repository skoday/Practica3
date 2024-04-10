import streamlit as st
import pandas as pd
from bridge.lo import Bridge

def cargar_csv():
    filepath = st.file_uploader("Cargar corpus", type=["csv"], key="csv_uploader")
    if filepath is not None:
        return pd.read_csv(filepath)
    return None


def cargar_txt():
    txt_file = st.file_uploader("Cargar documentos txt", type=["txt"], key="txt_uploader")
    if txt_file is not None:
        text_content = txt_file.getvalue().decode("utf-8")
        return pd.DataFrame({"Documento": text_content.splitlines()})
    return None

def main():
    st.title("Similaridad entre documetos")

    corpus = cargar_csv() 

    df_archivo = cargar_txt()

    txt_input = st.text_area("Ingrese el texto aquí", height=200)

    opciones_1 = st.selectbox("Opción 1", ["binary", "frequency", "tfidf"])
    opciones_2 = st.selectbox("Opción 2", ["1", "2", "3"])
    opciones_3 = st.selectbox("Opción 3", ["Título", "Contenido", "Título-Contenido"])

    if st.button("Enviar"):
        lineas_limpias = [linea.strip() for linea in txt_input.split("\n") if linea.strip()] 
        data = {"Documento": lineas_limpias}
        df = pd.DataFrame(data)
        
        if len(df) == 0:
            df = df_archivo

        if corpus is not None:
            enlace = Bridge(corpus, df, [opciones_1, int(opciones_2), opciones_3])
            respuesta = enlace.procesar_envio()

            for elemento in respuesta:
                elemento["Vector representation"] = opciones_1
                elemento["Extracted features"] = int(opciones_2)
                elemento["Comparison element"] = opciones_3

            enviar(df, respuesta)
            enlace.guardar_pdf(df, respuesta)

    if st.button("Comparar todo"):
        lineas_limpias = [linea.strip() for linea in txt_input.split("\n") if linea.strip()] 
        data = {"Documento": lineas_limpias}
        df = pd.DataFrame(data)

        if len(df) == 0:
            df = df_archivo

        if corpus is not None:
            enlace = Bridge(corpus, df, [])
            respuesta = enlace.procesar_todo()
            enviar(df, respuesta)
            enlace.guardar_pdf(df, respuesta)

def enviar(df, respuesta):
    for i, (index, row) in enumerate(df.iterrows()):
        st.write(f"Documento {i + 1}:\n {row['Documento']}")
        st.dataframe(respuesta[i])


if __name__ == "__main__":
    main()
