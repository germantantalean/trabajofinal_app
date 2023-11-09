#!/usr/bin/env python
# coding: utf-8
# In[ ]:
# INSTALAMOS LAS LIBREIRAS NECESARIAS
import pandas as pd
import streamlit as st 
import plotly.express as px
#from PIL import Image

st.set_page_config(page_title="Terremotos Peru") # Nombre para configurar paginma WEB
st.header('Resultados de Movimientos Sismicos  1960 - 2022') #Va a ser el titulo de la pagina
st.subheader('Como son los diferentes sismos en Peru?') #Subtitulo
excel_file = 'Catalogo1960_2022.xlsx' #Nombre archivo a importar
sheet_name = 'Catalogo1960_2021' #Hoja de Excel a importar

df= pd.read_excel(excel_file, #importo archivo excel
                   sheet_name=sheet_name,#Le digo cual hoja necesito
                   usecols='B:H', #columnas ha usar
                   header=0) #desde que fila debe empezar a tomarse la información *empieza en cero*
df_personas = df.groupby(['ANO_UTC'],as_index=False)['MAGNITUD'].count() # hago tipo TABLA DINAMICA para agrupar datos. por cada magnitud cuente

df_personas2 = df_personas # por si acaso

st.dataframe(df) #de esta forma nos muestra dataframe de streamlim

st.write(df_personas2) #nos sirve cuando no tenemos dataframe sino object

#Crear un grafico de pie chart

pie_chart=px.pie(df_personas2, #tomo el dataframe2
                 title = 'Cantidad de Sismos por Año', # Titulo
                 values = 'MAGNITUD', ## columna
                 names = 'ANO_UTC') ## para verlo por año --> colores

st.plotly_chart(pie_chart) # se muestra el dataframe en streamlit

# crear una lista con los parametros de la columna

ano = df['ANO_UTC'].unique().tolist() # se crea una lista con columna AÑO
profundidad = df['PROFUNDIDAD'].unique().tolist() # se crea una lista con columna PROFUNDIDAD
magnitud = df['MAGNITUD'].unique().tolist() # se crea una lista con columna MAGNITUD

# Se crea slicer de magnitud

magnitud_selector = st.slider('Magnitud del Sismo :',
                    min_value = min(magnitud), # Valor minimo de columna Magnitud
                    max_value = max(magnitud), # Valor maximo de columna Magnitud
                    value = (min(magnitud),max(magnitud))) # que tome desde el minimo al maximo

# crear multisectores

ano_selector = st.multiselect('Año:',
                ano,
                default = ano)

profundidad_selector = st.multiselect('Profundidad:',
                                      profundidad,
                                      default = profundidad)

# Ahora se usara selectores y slider filtren informacion

mask=(df['MAGNITUD'].between(*magnitud_selector))&(df['ANO_UTC'].isin(ano_selector))&(df['PROFUNDIDAD'].isin(profundidad_selector))

numero_resultados = df[mask].shape[0] ##numero de filas disponibles
st.markdown(f'*Resultados Disponibles:{numero_resultados}*') ## sale como un titulo

#nueva agrupacion

df_agrupado = df[mask].groupby(by=['ANO_UTC']).count()[['MAGNITUD']] #que agrupe por PROFUNDIDAD y MAGNITUD

#datos de Magnitud

df_agrupado=df_agrupado.rename(columns={'Magnitud': 'Año'})
df_agrupado=df_agrupado.reset_index()

#Crear un grafico de barras

bar_chart = px.bar(df_agrupado,
            x='ANO_UTC',
            y='MAGNITUD',
            text= 'MAGNITUD',
            color_discrete_sequence = ['#f5b632']*len(df_agrupado),
            template = 'plotly_white')

st.plotly_chart(bar_chart) # mostrar grafico








