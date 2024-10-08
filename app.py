import streamlit as st
import pandas as pd
import sweetviz as sv
import streamlit.components.v1 as components  # Para mostrar HTML en Streamlit
from ydata_profiling import ProfileReport
import klib
import matplotlib.pyplot as plt

# Configurar la página para usar todo el ancho
st.set_page_config(layout="wide")

# Título de la aplicación
st.title('Automating EDA')

# Subtítulo de la aplicación
st.subheader('Useful python libraries')

# Subir base desde el computador
archivo_base = st.file_uploader('Upload your data', type=['xlsx', 'csv'])

# Verificar si se ha subido un archivo
if archivo_base is not None:
    # Obtener el nombre del archivo
    nombre_archivo = archivo_base.name
    
    # Verificar el tipo de archivo según la extensión
    if nombre_archivo.endswith('.xlsx'):
        st.write("El archivo subido es un Excel.")
        data = pd.read_excel(archivo_base)
        st.write(data.head())
    elif nombre_archivo.endswith('.csv'):
        st.write("El archivo subido es un CSV.")
        sep = st.text_input("Sep: ")
        if sep:
            data = pd.read_csv(archivo_base, sep=sep)
            st.write(data.head())
    else:
        st.write("Tipo de archivo no reconocido.")
    
    # Generar y mostrar el reporte de pandas-profiling
    if 'data' in locals():
        st.write("Generando el reporte de EDA con pandas-profiling...")
        profile = ProfileReport(data, explorative=True)
        profile_html = profile.to_html()
        components.html(profile_html, height=800, scrolling=True)

        # Generar y mostrar el reporte de Sweetviz
        st.write("Generando el reporte de EDA con Sweetviz...")
        sweet_report = sv.analyze(data)
        sweet_report.show_html('sweet_report.html')  # Guardar el reporte en un archivo HTML
        
        # Leer el contenido del archivo y mostrarlo en Streamlit
        with open('sweet_report.html', 'r') as f:
            sweetviz_html = f.read()
        
        # Mostrar el HTML en Streamlit
        components.html(sweetviz_html, height=800, scrolling=True)
        
        # Generar las visualizaciones con Klib
        st.write("Generando visualizaciones con Klib...")

        # 1. Categorical Plot
        klib.cat_plot(data)
        plt.savefig('klib_cat_plot.png')
        plt.close()
        st.image('klib_cat_plot.png', caption='Categorical Plot', use_column_width=True)

        # 5. Distribution Plot
        klib.dist_plot(data)
        plt.savefig('klib_dist_plot.png')
        plt.close()
        st.image('klib_dist_plot.png', caption='Distribution Plot', use_column_width=True)

        # 6. Missing Value Plot
        klib.missingval_plot(data)
        plt.savefig('klib_missingval_plot.png')
        plt.close()
        st.image('klib_missingval_plot.png', caption='Missing Value Plot', use_column_width=True)
