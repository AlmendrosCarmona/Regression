import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('data.csv', delimiter=';')

df_t = pd.DataFrame(columns=['T', 'I'])

Temp = int(input('Introduce temperatura limite: '))

df_t = pd.DataFrame(columns=['T', 'I'])

x = []
y = []
a = 0
y_corr = []

for d in range(df.shape[0]):

    x_i = float(df['T'].iloc[[d]])
    y_i = float(df['I'].iloc[[d]])
    x.append(x_i)
    y.append(y_i)
    if d == 0:
        y_corr.append(y_i)  # Guardamos la Intensidad inicial
        print(y_corr)
        print(len(y_corr))
    if d == 1:

        # Calculamos las medias
        x_m = (x[0]+x[1])/2.
        y_m = (y[0]+y[1])/2.
        # Calculamos las desviaciones
        x_s = (((x[0]-x_m)**2+(x[1]-x_m)**2))/(2-1)
        y_s = (((y[0]-y_m)**2+(y[1]-y_m)**2))/(2-1)

        # Calculamos la covarianza
        cov_xy = ((x[0]-x_m)*(y[0]-y_m)+(x[1]-x_m)*(y[1]-y_m))/(2-1)
    elif d > 1 and x_i < Temp:
        # Calculamos la nueva media para cada step (FALTA PONER HASTA QUE LLEGUEMOS A ESE PUNTO TEMP)
        oldx_m = x_m
        oldy_m = y_m
        k = len(x)
        x_m = x_m + (x_i-x_m)/k
        y_m = y_m + (y_i-y_m)/k

        # Calculamos la nueva varianza WELDFORD ALGORITHM
        x_s = (x_s + (x_i-x_m)*(x_i-oldx_m))
        y_s = (y_s + (y_i-y_m)*(y_i-oldy_m))
        var_x = x_s/(k-1)
        var_y = y_s/(k-1)

        # Calculamos la neuva covarianza
        cov_xy = cov_xy - (cov_xy-(x_i-x_m)*(y_i-oldy_m))/(k-1)

        m = cov_xy/(var_x)
        b = y_m - m*x_m
        x_reg = np.array(x)

        fig = plt.figure(1)
        fig1 = plt.scatter(x, y, c="blue", label='Data')
        # Aqui utilizo todos los puntos para hacer la recta, no es necessario.
        fig1 = plt.plot(x, m*x_reg+b, c="red", label='Regression lineal')
        fig1 = plt.ion()
        fig1 = plt.legend()
        fig.show()
        input("Press Enter to continue...")
        fig1 = plt.clf()

        # Chekcing tool
        # m2, b2 = np.polyfit(x, y, 1)
        # fig1 = plt.plot(x, m2*x_reg+b2, c="black")
    elif x_i > Temp or a == 1:
        a = 1
        # Primero calculamos la distancia del valor y_i
        # al valor esperado por la recta de regression calculado anteriormente
        dist = y_i - (m*x_i+b)
        y_corr = np.append(y_corr, y_corr[0] + dist)
        # Hacemos el plot
        fig = plt.figure(2)
        fig2 = plt.plot(y_corr,  c='red', label="Intensitat corregida")
        fig2 = plt.axhline(y_corr[0], c='black', linestyle='--', label="Intensitat inicial")
        fig2 = plt.ylim([0, 85])
        fig2 = plt.ion()
        fig2 = plt.title("Intesitat corregida")
        fig2 = plt.legend()
        fig.show()
        x_reg = np.array(x)
        fig = plt.figure(1)
        fig1 = plt.scatter(x, y, c="blue")
        # Aqui utilizo todos los puntos para hacer la recta, no es necessario.
        fig1 = plt.plot(x, m*x_reg+b, c="red", label="RegressiÃ³ anterior")

        # Una vez tenemos la distancia claculada i ploteada, actualizamos la recta
        # de regression.
        # Calculamos la nueva media para cada step (FALTA PONER HASTA QUE LLEGUEMOS A ESE PUNTO TEMP)
        oldx_m = x_m
        oldy_m = y_m
        k = len(x)
        x_m = x_m + (x_i-x_m)/k
        y_m = y_m + (y_i-y_m)/k

        # Calculamos la nueva varianza WELDFORD ALGORITHM
        x_s = (x_s + (x_i-x_m)*(x_i-oldx_m))
        y_s = (y_s + (y_i-y_m)*(y_i-oldy_m))
        var_x = x_s/(k-1)
        var_y = y_s/(k-1)

        # Calculamos la neuva covarianza
        cov_xy = cov_xy - (cov_xy-(x_i-x_m)*(y_i-oldy_m))/(k-1)

        m = cov_xy/(var_x)
        b = y_m - m*x_m
        x_reg = np.array(x)

        fig1 = plt.scatter(x, y, c="blue")
        # Aqui utilizo todos los puntos para hacer la recta, no es necessario.
        fig1 = plt.plot(x, m*x_reg+b, c="yellow", label="Regressió actual")
        fig1 = plt.ion()
        fig1 = plt.title("RegressiÃ³ step actual i regressió step anterior")
        fig1 = plt.text(60, 30, f'La desviacion es: {int(dist)}', fontsize=10)
        fig1 = plt.legend()

        # Dibujamos la distancia entre plots.

        fig.show()
        input("Press Enter to continue...")
        fig2 = plt.clf()
        fig1 = plt.clf()
        # plt.close("all")
