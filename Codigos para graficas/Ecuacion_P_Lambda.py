import pandas as pd
import numpy as np

import math

#   Definen Funciones

def P1_funtion (Z):
    P1 = (10045 * (math.e**(0.314*Z))) - (10045 * Z)
    return P1

def P2_funtion (Z):
    P2 = 10045 * math.exp(0.157*Z) - 10045 * Z
    return P2
def P3_funtion (Z):
    P2 = 10045 * math.exp(0.105 * Z) - 10045 * Z
    return P2

#generar Vector Z de 101 pocicones desdes 0 hasta -100
Z = list(range(0,-101,-1))
print(Z)

#   Evaluar vector Z en p1 p2 p3
P1 = list(Z)
for i in Z:
    P1[i] =   P1_funtion(Z[i])
#print(P1)

P2 = list(Z)
for i in Z:
    P2[i] =   P2_funtion(Z[i])
#print(P2)

P3 = list(Z)
for i in Z:
    P3[i] =   P3_funtion(Z[i])
#print(P3)

#   Generar datframe con Z P1, P2, P3

P = pd.DataFrame({'Z':Z,'P1':P1,'P2':P2,'P3':P3})
print(P)

#generar Excel

#P.to_excel('P_vs_lambda.xlsx', sheet_name='example')
# Plot con mathplotlib
import matplotlib.pyplot as plt


plt.plot(Z, P.iloc[:,1:4])
plt.grid(True)


#plt.xticks([-100,-50, 0],[r'$- Cien$', r'$- Cincuenta$', r'$Cero$'])

s = list(range(-100,10,10))
print(s)
plt.xticks(list(range(-100,10,10)))
plt.legend(P.iloc[:,1:4],loc=2)
plt.show()


