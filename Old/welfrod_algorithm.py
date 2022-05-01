# Comentar que todo esto es mejor hacerlo con el metodo de minimos quadrados
# pero es mas dificil de resolver con PLC

import numpy as np
from pylab import *
import matplotlib.pyplot as plt

i = 0
a = 0

while True:
    if i == 0:
        # Este loop solo se hace la primera vez.
        i += 1
        # Entrada de datos
        print('Introduce x1')
        x1 = float(input())
        print('Introduce y1')
        y1 = float(input())
        print('Introduce x2')
        x2 = float(input())
        print('Introduce y2')
        y2 = float(input())
        # Creamos los vectores
        x = [x1, x2]
        y = [y1, y2]
        # MEDIA
        x_m = (x[0]+x[1])/2.
        y_m = (y[0]+y[1])/2.
        print(f'La media de las x es {x_m}')
        print(f'La media de las y es {y_m}')
        # DESVIACION
        k = len(x)
        # Desviacion de la poblacion calculada a partir de los datos de una
        # muestra
        x_s = (((x[0]-x_m)**2+(x[1]-x_m)**2))/(k-1)
        print(f'La varianza de las x es {x_s}')
        y_s = (((y[0]-y_m)**2+(y[1]-y_m)**2))/(k-1)
        print(f'La varianza de las y es {y_s}')
        # COVARIANZA XY
        cov_xy = ((x[0]-x_m)*(y[0]-y_m)+(x[1]-x_m)*(y[1]-y_m))/(k-1)
        print(f'La covarianza de las xy es {cov_xy}')
        # cov_xy_R = np.cov(x, y, ddof=1)
        # print(f'La covarianza de las xy es {cov_xy_R}')

    elif i < 100:  # Aixo es fara realment en funcio de la temperatura.
        # Introduce nuvevos datos
        print(f'Introduce x{i+2}')
        x_i = float(input())
        print(f'Introduce y{i+2}')
        y_i = float(input())

        # Se adjuntan al vector para tenerlo guardado (no ara falta en el PLC)x
        x = np.array(x)
        y = np.array(y)
        x = np.append(x, x_i)
        y = np.append(y, y_i)
        # Se calculan las nuevas variables con el metodo welfrod
        # MEDIA
        oldx_m = x_m
        oldy_m = y_m
        k = len(x)
        x_m = x_m + (x_i-x_m)/k
        y_m = y_m + (y_i-y_m)/k
        print(f'La media de las x es {x_m}')
        # print(f'La media real de las x es {np.mean(x)}')
        print(f'La media de las y es {y_m}')
        # print(f'La media real de las y es {np.mean(y)}')

        # VARIANZA WELFROD ALGORITHM
        x_s = (x_s + (x_i-x_m)*(x_i-oldx_m))
        y_s = (y_s + (y_i-y_m)*(y_i-oldy_m))
        var_x = x_s/(k-1)
        var_y = y_s/(k-1)
        print(f'La varianza de las x es {var_x} (Welford Algorithm)')
        print(f'La varianza de las y es {var_y} (Welford Algorithm)')
        # Varianza real
        # x_s_r = np.var(x, ddof=1)
        # print(f'La varianza de las x es {x_s_r}')

        # COVARIANZA ONLINE ALGORITHM

        cov_xy = cov_xy - (cov_xy-(x_i-x_m)*(y_i-oldy_m))/(k-1)
        print(f'La covarianza xy es: {cov_xy}(Online Algorithm)')
        cov_xy_R = np.cov(x, y, ddof=1)
        # cov_xy_R = cov_xy_R[0, 1]
        print(f'La covarianza de las xy es {cov_xy_R}')

        # REGRESION
        fig = plt.figure()
        fig1 = plt.scatter(x, y, c="blue")
        # trend = polyfit(x, y, 1)
        # trendpoly = np.poly1d(trend)
        # fig1 = plt.plot(x, trendpoly(x))
        m = cov_xy/(var_x)
        b = y_m - m*x_m
        print(m)
        # Amb la m y la b ja pots plotejarte la recta de mil maneras,
        # jo utilitzo tot el dataset pero no es necessari.
        y_line = m*x+b
        fig1 = plt.plot(x, y_line)
        fig.show(fig1)
        # Ahora nos guardamos estos datos para mantener siempre estos datos
        # y ir actualizando
        x_m_1 = x_m
        y_m_1 = y_m
        x_s_1 = x_s
        y_s_1 = y_s
        cov_xy_1 = cov_xy

        i += 1
    else:
        # Introduce nuvevos datos
        print(f'Introduce x{i+2}')
        x_i = float(input())
        print(f'Introduce y{i+2}')
        y_i = float(input())
        if a == 0:
            x = np.append(x, x_i)
            y = np.append(y, y_i)
            a += 1
        else:
            x = np.delete(x, -1)
            y = np.delete(y, -1)
            x = np.append(x, x_i)
            y = np.append(y, y_i)
            a += 1

        # Se calculan las nuevas variables con el metodo welfrod
        # Antes de calcular las variables, se importan los ultimos valores
        # calculados
        x_m = x_m_1
        y_m = y_m_1
        x_s = x_s_1
        y_s = y_s_1
        cov_xy = cov_xy_1

        # MEDIA
        oldx_m = x_m
        oldy_m = y_m
        k = len(x)
        x_m = x_m + (x_i-x_m)/k
        y_m = y_m + (y_i-y_m)/k
        print(f'La media de las x es {x_m}')
        # print(f'La media real de las x es {np.mean(x)}')
        print(f'La media de las y es {y_m}')
        # print(f'La media real de las y es {np.mean(y)}')

        # VARIANZA WELFROD ALGORITHM
        x_s = (x_s + (x_i-x_m)*(x_i-oldx_m))
        y_s = (y_s + (y_i-y_m)*(y_i-oldy_m))
        var_x = x_s/(k-1)
        var_y = y_s/(k-1)
        print(f'La varianza de las x es {var_x} (Welford Algorithm)')
        print(f'La varianza de las y es {var_y} (Welford Algorithm)')
        # Varianza real
        # x_s_r = np.var(x, ddof=1)
        # print(f'La varianza de las x es {x_s_r}')

        # COVARIANZA ONLINE ALGORITHM

        cov_xy = cov_xy - (cov_xy-(x_i-x_m)*(y_i-oldy_m))/(k-1)
        print(f'La covarianza xy es: {cov_xy}(Online Algorithm)')
        cov_xy_R = np.cov(x, y, ddof=1)
        # cov_xy_R = cov_xy_R[0, 1]
        print(f'La covarianza de las xy es {cov_xy_R}')

        # REGRESION
        fig = plt.figure()
        fig1 = plt.scatter(x, y, c="blue")
        fig1 = plt.scatter(x_i, y_i, c="red")
        #trend = polyfit(x, y, 1)
        #trendpoly = np.poly1d(trend)
        #fig1 = plt.plot(x, trendpoly(x))
        m = cov_xy/(var_x)
        b = y_m - m*x_m
        print(m)
        # Amb la m y la b ja pots plotejarte la recta de mil maneras,
        # jo utilitzo tot el dataset pero no es necessari.
        y_line = m*x+b
        fig1 = plt.plot(x, y_line)
        fig.show(fig1)

        i += 1
