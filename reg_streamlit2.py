import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import re

st.set_page_config(layout="wide")
st.title("Estudi regressió automàtica")

# Read data
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df1 = pd.read_csv(uploaded_file, delimiter=';')
    # Select witch intensity
    intensity = st.selectbox('Selecciona Intensidad: ', ('Ip', 'In',
                                                         'I1+', 'I1-', 'I2+',
                                                         'I2-', 'I3+', 'I3-',
                                                         'I4+', 'I4-', 'I5+',
                                                         'I5-', 'I6+',
                                                         'I6-', 'I7+', 'I7-',
                                                         'I8+', 'I8-'))
    temperature = st.selectbox('Selecciona Temperatura: ', ('TempVAT',
                                                            'TempCabine'))

    df = df1[[temperature, intensity]]
    df = df.rename(columns={temperature: "T", intensity: "I"})
    #df["T"] = df["T"].astype(float)
    #df["T"] = pd.to_numeric(df["T"])
    df["T"] = pd.to_numeric(df["T"].apply(lambda x: re.sub(',', '.', str(x))))
    st.text(df.dtypes)

    # Create variables user input
    n = st.slider("Número de punts a importar: ", 1, len(df.index)+1)
    Temp = st.number_input(label="Temperatura de canvi", step=1., format="%.2f")

    if Temp and n and intensity and temperature:
        df_reg = df.truncate(after=n-1)
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
        df_reg2 = df.truncate(after=(n-2))
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
        col1, col2 = st.columns(2)
        col1.subheader("Regressió lineal")
        col1.plotly_chart(fig2)
        col2.subheader("Intensitat corregida")

        # Ahora tengo que calcular la distancia i plotear I_corr respecto su indice.
        # Distancia
        # x
        for i in range(n):
            if i > 1:
                x_d = df_reg["T"].iat[i]
                # y
                y_d = df_reg["I"].iat[i]
                # m_anterior i b_anterior
                df_reg3 = df.truncate(after=(i-1))
                var_x_i = df_reg3["T"].var()
                cov_i = df_reg3.cov().iat[0, 1]  # Selecionamos la covarianza x, y
                x_m_i = df_reg3["T"].mean()
                y_m_i = df_reg3["I"].mean()

                m_i = float(cov_i/(var_x_i))
                b_i = float(y_m_i - m_i*x_m_i)
                y_d_a = float(x_d*m_i+b_i)
                # Calculamos la I que tendria que haber sido
                dist = float(y_d_a - y_d)
                if float(x_d) > float(Temp):
                    df_reg['Dist'].iat[i] = -dist
                else:
                    df_reg['Dist'].iat[i] = 0.
            else:
                df_reg['Dist'] = 0.

        # Distancia entre la que tendria que haber sido y la que ha sido
        df_reg['I_corr'] = df_reg['Dist'] + df_reg["I"].iat[0]
        fig3 = px.line(df_reg, y='I_corr', color_discrete_sequence=['red'])
        fig3.update_traces(selector=0, name='I_corr', showlegend=True)
        col2.plotly_chart(fig3)
        # df_reg['I_corr'] = np.where(df_reg['T'] <= Temp, df_reg["I"].iat[0], df_reg["I"].iat[0]+dist)
        st.subheader('Dades')
        st.dataframe(df_reg)
        # st.dataframe(df_reg2)
