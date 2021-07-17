import pandas as pd
import numpy as np
#import matplotlib
import math

#   Se definen las funciones

#funcion para caluclar F3
def F5_funtion(k,w,t):
    F5 = -(12054000/k) * (math.exp(-5.9 * k)) * (math.cos(40*k))*(math.sin(w*t))
    return F5

#funcion para calcular k
def w_funtion(k):
    w = (k * 9.8) ** (1/2)
    return w

#   Se definen las variables de entrada
k = [0.157079633, 0.104719755, 0.078539816, 0.062831853, 0.052359878, 0.044879895, 0.039269908]
t = [1,5,10]
print(k)
contador = list(range(0,7,1))
contador_2 = list(range(0,3,1))
w = list(contador)

#   Generamos w a partir de k
for i in contador:
    w[i] = w_funtion(k[i])
print(w)

# calculamos funcion 
F5=pd.DataFrame(columns=['t1 = 1' ,'t2 = 5', 't3 = 10'], index=range(7))
print(F5)


for n in contador_2:
    for i in contador:
        F5.iloc[i,n] = F5_funtion(k[i],w[i],t[n])
print(k)
print(w)
print(F5)
F5.to_excel('F5.xlsx', sheet_name='F5')