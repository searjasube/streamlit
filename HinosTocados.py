# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 14:19:40 2024

@author: Sear.Castro
"""



import pandas as pd
import streamlit as st
import plotly.express as px

import time
import datetime
from datetime import date, timedelta
import datetime as dt     
from math import floor
import numpy as np


#########CARREGA DATA#########
DT_ATUAL = date.today()
DELTA = timedelta(365)
DELTADIA = timedelta(1)
DT_REL = DT_ATUAL-DELTA
DT_FILE = DT_REL.strftime('%d-%m-%Y')


df=pd.read_excel("C:/Users/sear.castro/Desktop/2024/Orquestra/base_hinos.xlsx")

df_ensaio=pd.read_excel("C:/Users/sear.castro/Desktop/2024/Orquestra/ensaios.xlsx")
df_ensaio['Hoje']=date.today()
df_ensaio['Hoje'] = pd.to_datetime(df_ensaio['Hoje'])
df_ensaio['calc'] = df_ensaio['Ensaio']-df_ensaio['Hoje']
df_ensaio['calc']=df_ensaio['calc'].dt.days
df_ensaio['TempoEnsaio']=df_ensaio['calc']



df_ensaio['Hoje']=date.today()
df_ensaio['Hoje'] = pd.to_datetime(df_ensaio['Hoje'])
df_ensaio['calc'] = df_ensaio['Culto']-df_ensaio['Hoje']
df_ensaio['calc']=df_ensaio['calc'].dt.days
df_ensaio['TempoCulto']=df_ensaio['calc']



df['Freq'] = df.groupby('Hinos')['Hinos'].transform('count')
df['Hoje']=date.today()
df['Hoje'] = pd.to_datetime(df['Hoje'])
df['Hoje']=df['Hoje']
df['calc'] = df['Hoje']-df['Data']
df['calc']=df['calc'].dt.days/6
df['Tocado']= df['calc'].apply(np.floor) 
df['Tocado']=df['Tocado'].map(str) + str(" Semana")

df.drop(['Hoje','calc'], axis=1, inplace=True)

st.set_page_config(
    page_title="Hinos Tocados-2024",
    page_icon=":saxophone:",
    layout="wide"
    )


# ---------PAGINA PRINCIPAL ---------
st.title(":saxophone: Hinos Tocados - 2024 "+str(":violin:"))



# --------- BARRA LATERAL FILTROS ---------
st.sidebar.header("Selecione os Filtros :church:")

#st.sidebar.image('/home/bot/Bot_Telefonia/PainelTelefonia/pages/logo.png')
data_inicio = st.sidebar.date_input("Data Inicial", datetime.date(2024, 3, 2))
data_fim = st.sidebar.date_input("Data Final", DT_ATUAL)


depto = st.sidebar.multiselect(
    "Selecione o Departamento:",
    options=df["TipoCulto"].unique(),
    default=df["TipoCulto"].unique()
)



hino = st.sidebar.multiselect(
    "Selecione um Hino:",
    options=df["Hinos"].unique(),
    default=df["Hinos"].unique(),
)

df_selection = df.query(
    "TipoCulto == @depto & Hinos == @hino & Data >= @data_inicio & Data <= @data_fim" 
)


df_selection['Data']=df_selection['Data'].dt.strftime('%d/%m/%Y')
left_column, middle_column1,middle_column2, right_column = st.columns(4)


#df_selection[df_selection['Tocado'] > 1].sort_values('Tocado')['Titulo Hino	'].head(5)
top = (df_selection.groupby(['Hinos','Titulo Hino'])["Hinos"].agg("count")).reset_index(name='count').head(5)
top=top.sort_values(by='count', ascending=False).head(2)
top_hino=top.iloc[0]['Hinos']

proximo_ensaio = df_ensaio.query(
    "TempoEnsaio >=0" 
).head(1)

int_prox_ensaio=int((proximo_ensaio.iloc[0]['TempoEnsaio']))



congresso_ensaios = len(df_ensaio.query(
    "TempoEnsaio >=0" 
))




proximo_culto= df_ensaio.query(
    "TempoCulto >=0" 
).head(1)
int_prox_culto=proximo_culto.iloc[0]['TempoCulto']



mais_novo= df_selection.query(
    "Tipo =='Novo'" 
).head(1)
mais_novo_str=mais_novo.iloc[0]['Hinos']



#st.markdown("###")

st.markdown("""---""")

column0, column1, column2, column3, column4 = st.columns(5)

with column0:
    st.subheader("+ Tocado:chart_with_upwards_trend:")
    st.subheader(f"{top_hino}")

with column1:
    st.subheader("+ Novo:newspaper:")
    st.subheader(f"{mais_novo_str}")
    
with column2:
    st.subheader("Ensaio em:stopwatch:")
    st.subheader(f"{int_prox_ensaio} Dias")
    
with column3:
    st.subheader("Culto em:timer_clock:")
    st.subheader(f"{int_prox_culto} Dias")
    

with column4:
    st.subheader("Até Congresso:hourglass_flowing_sand:")
    st.subheader(f"{congresso_ensaios} Ensaios")
    

st.markdown("""---""") 
        
        

## --------- CONFIGURAÇÕES FILTROS ---------
fig_rank = px.box(df_selection, x="Hinos", y="Freq")
fig_rank.update_xaxes(type='category')


# --------- MOSTRA GRÁFICOS ---------
#st.plotly_chart(fig_rank)


df_selection = df_selection.drop('Tipo', axis=1)
st.table(df_selection)




