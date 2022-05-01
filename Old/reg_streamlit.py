import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np


st.title("Estudi regressió automàtica")

# Read data
df = pd.read_csv('data.csv', delimiter=';')

# Create variables user input
n = st.slider("Número de punts a importar: ", 0, len(df.index))
Temp = st.number_input(label="Temperatura de canvi", step=1., format="%.2f")


if Temp and n:
    df_reg = df.truncate(after=n)
    var_x = df_reg["T"].var()
    cov = df_reg.cov().iat[0, 1]  # Selecionamos la covarianza x, y
    x_m = df_reg["T"].mean()
    y_m = df_reg["I"].mean()

    m = cov/(var_x)
    b = y_m - m*x_m

    # Calculo con numpy
    # x_np = df_reg['T'].to_numpy()
    # y_np = m*x_np + b

    # Primer plot hecho con numpy y plotly
    # fig1 = px.scatter(df_reg, x='T', y='I')
    # fig1.add_trace(px.line(x=x_np, y=y_np).data[0])
    # st.plotly_chart(fig1)

    # Primer plot hecho sin numpy, multiplocando pandas y ploteando en plotly.
    df_reg['I_reg'] = df_reg['T'].apply(lambda x: x*m+b)
    # df_reg["I_reg2"] = df_reg['T']*m+b

    # En pandas, ahora quiero crear la columna I_corr, que sera siempre la
    # inicial hasta que supere el limite de temperatura, que sumara distancia
    # anterior.
    # Calculamos todo igual pero para n-1 para saber qual seria el valor de I
    # en esta T
    df_reg2 = df.truncate(after=(n-1))
    var_x_a = df_reg2["T"].var()
    cov_a = df_reg.cov().iat[0, 1]  # Selecionamos la covarianza x, y
    x_m_a = df_reg2["T"].mean()
    y_m_a = df_reg2["I"].mean()

    m_a = cov_a/(var_x_a)
    b_a = y_m_a - m_a*x_m_a
    df_reg2['I_reg'] = df_reg2['T'].apply(lambda x: x*m_a+b_a)

    # Plots
    fig2 = px.scatter(df_reg, x='T', y='I', color_discrete_sequence=[
        'blue'])
    fig2.add_trace(px.scatter(df_reg2, x='T', y='I', color_discrete_sequence=['red']).data[0])

    fig2.add_trace(px.line(df_reg, x='T', y='I_reg', color_discrete_sequence=[
        'blue']).data[0])

    fig2.add_trace(px.line(df_reg2, x='T', y='I_reg', color_discrete_sequence=['red']).data[0])

    fig2.update_traces(selector=0, name='Punto n', showlegend=True)
    fig2.update_traces(selector=1, name='Puntos n-1', showlegend=True)
    fig2.update_traces(selector=2, name='Regression n', showlegend=True)
    fig2.update_traces(selector=3, name='Regression n-1', showlegend=True)
    st.plotly_chart(fig2)

    # Ahora tengo que calcular la distancia i plotear I_corr respecto su indice.
    # Distancia
    # x
    x_d = df_reg["T"].iat[n]
    # y
    y_d = df_reg["I"].iat[n]
    # m_anterior i b_anterior
    y_d_a = x_d*m_a+b_a
    st.text(x_d)
    st.text(y_d)
    st.text(y_d_a)
    # Calculamos la I que tendria que haber sido
    dist = y_d_a - y_d

    # Distancia entre la que tendria que haber sido y la que ha sido

    df_reg['I_corr'] = np.where(df_reg['T'] <= Temp, df_reg["I"].iat[0], df_reg["I"].iat[0]+dist)

    st.dataframe(df_reg)
    st.dataframe(df_reg2)
