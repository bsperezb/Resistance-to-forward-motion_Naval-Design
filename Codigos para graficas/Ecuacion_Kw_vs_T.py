import pandas as pd
import numpy as np
#import matplotlib
import math

#   Se definen las funciones

#funcion para caluclar F3
def F3_funtion(k,w,t):
    F3 = (301359/k) * (math.exp(-5.9 * k)) * (math.sin(40*k))*(math.sin(w*t))
    return F3

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
F3=pd.DataFrame(columns=['t1 = 1' ,'t2 = 5', 't3 = 10'], index=range(7))
print(F3)


#for i in contador:
#    F3.iloc[i,0] = F3_funtion(k[i],w[i],t[0])
    


for n in contador_2:
    for i in contador:
        F3.iloc[i,n] = F3_funtion(k[i],w[i],t[n])
print(k)
print(w)
print(F3)
print(math.sin(90))
F3.to_excel('F3.xlsx', sheet_name='F3')