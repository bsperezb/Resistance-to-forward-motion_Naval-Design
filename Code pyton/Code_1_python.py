# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Diseño naval
# %% [markdown]
# ## Importamos las librerias

# %%
import pandas as pd
import numpy as np
import math

# %% [markdown]
# ## Declaramos las variables de entrada

# %%
#variables de entrada
Fn = 0.3        #numero de froude

LWL = 74.4
Ls = LWL
L = Ls
B = 12.6
Tm = 3.8
Ta = 3.8
Tpp = 3.8
T = Ta
LCB = 35.712
Cb = 0.501
Cm = 0.823
Cp = 0.61
Cwp = 0.796
S = 1168
Ss = S
Sapp = 2
At = 1.3
Abt = 5.4
Dens_a_s = 1025.9
Visc_a_s = (1.188 * ((10)**(-6)))
hb = 1.65
ie = 36
g = 9.8
d_bto = 0               # 0
C_bto = 0               #[0.003, 0.012]

#   Entrada para C13----------------------------------------------------------------------
#Aft_form ={"Afterbody form":['V-shaped section','Normal section shape','U-shaped section with Hogner stern']}

Afterbody_form = input(""" 
Ingrese el numero correspodiente para la forma de la popa:\n
0. Prom
1. Sección en V
2. Sección normal
3. Sección en U
\n
""")
Afterbody_form = int(Afterbody_form)
# Verificar ie -------------------------------------------------------
try:
    ie
except NameError:
    ie_test = False
    print("ie no está definida. será calculada")
else:
    ie_test = True
    print("ie ya está definida")

# %% [markdown]
# ## Rango de Aplicabilidad (monocasco) Fn
# ### Usamos la libreria de pandas para crear un dataframe con los datos de la tabla del rango de aplicavilidad para posterirormente interpolar

# %%
Tabla1 = {"type of ship":['Tankers, bulk carriers','Trawler, tugs','Container ships, destroyers','cargo liners','RoRo Ships car ferries'],'Max Fn':[0.24, 0.38, 0.45, 0.3, 0.35], 'Min Cp':[0.73, 0.55, 0.55, 0.56, 0.55],'Max Cp':[0.85, 0.65, 0.67, 0.75, 0.67],'Min L/B':[5.1, 3.9, 6, 5.3, 5.3], 'Max L/B':[7.1, 6.3, 9.5, 8, 8],'Min B/T':[2.4, 2.1, 3, 2.4, 3.2],'Max B/T':[3.2, 3, 4, 4, 4]}

Tabla_Rango_aplicabilidad = pd.DataFrame(Tabla1)
print('Tabla rango de aplicabilidad \n\n')
print(Tabla_Rango_aplicabilidad)

Tabla3 = {'Cp min':[0.55],'Cp max':[0.85],'L/B min':[3.9],'L/B max':[15],'B/T min':[2.1],'B/T max':[4]}
Tabla_3 = pd.DataFrame(Tabla3)

#print(Tabla_3)

# %% [markdown]
# ## Calculo de rango de aplicabilidad (Figura 1)
# ### se interpola en la tabla de rango de aplicabilidad con el valor definido de la variable "Fn" y "Tipo de envarcacion" para obtener las variables : 
# ### L/B             B/T             Cp
# 

# %%
# definir para rango dee froude de (0.45 - 0.55)
Fn = 0.2
#Cp = 20
Tabla_aux1 = Tabla_Rango_aplicabilidad
def Rango_Aplicabilidad_funtion (Fn, Cp, L, B):
    """
    esta funcion calcula el el Fn maximo y
    el tipo de embarcaion a partir de L B y Fn

    """

    if (Fn >= 0.45) and (Fn < 0.55) :
        Fn = 0.55
        tos = np.nan
        regreso=[Fn,tos]
        return regreso
    elif Fn >= 0.55:
        Fn = Fn
        tos = np.nan
        regreso=[Fn,tos]
        return regreso
    else:
        # Se definen variables de entrada para la tabla
        #Fn = Fn
        #Cp = Cp
        L_B = L/B
        B_T = B/T
        print('Variables de entrada a la tabla \n')
        print('Fn = ',Fn,'\nCp = ', Cp,'\nL/B = ',L_B,'\nB/T=',B_T, '\n\n')

        # Comparamos el Froude
        #print(Tabla_Rango_aplicabilidad)
        Fn_true = Tabla_Rango_aplicabilidad['Max Fn'] >= Fn
        Tabla_aux1 = Tabla_Rango_aplicabilidad.loc[Fn_true] # en esta tabla se irán almacenando las filas en las que vayan encajando las variables
        
        # comparamos Cp
        Cp_max_true = Tabla_aux1['Max Cp'] >= Cp
        Tabla_aux1 = Tabla_aux1.loc[Cp_max_true]

        Cp_min_true = Tabla_aux1['Min Cp'] <= Cp
        Tabla_aux1 = Tabla_aux1.loc[Cp_min_true]

        # Comparamos L/B
        L_B_max_true = Tabla_aux1['Max L/B']> L_B
        Tabla_aux1 = Tabla_aux1.loc[L_B_max_true]

        L_B_min_true = Tabla_aux1['Min L/B']< L_B
        Tabla_aux1 = Tabla_aux1.loc[L_B_min_true]

        # Comparamos B_T
        B_T_max_true = Tabla_aux1['Max B/T'] > B_T
        Tabla_aux1 = Tabla_aux1.loc[B_T_max_true]

        B_T_min_true = Tabla_aux1['Min B/T'] < B_T
        Tabla_aux1 = Tabla_aux1.loc[B_T_min_true]

        # Seleccionar Fila con mayor Fn
        #ordenamos con respecto a fn de mayor a menor la tabla
        Tabla_aux1 = Tabla_aux1.sort_values(by="Max Fn", ascending=False)
        #print (Tabla_aux1)
        #Seleccinamos la primera fila (mayor valor)
        Tabla_aux1 = Tabla_aux1.head(1)
        if Tabla_aux1.empty == False:
            Fn = Tabla_aux1.iloc[0 ,1]
            tos = Tabla_aux1.iloc[0,0]
            print('valores dentro de los rangos de aplicabilidad')
        else:
            print('Valores fuera de los rangos de aplicabilidad')
            Fn = Fn
            tos = np.nan
        
        #print(Tabla_aux1)       
        #print(Fn, tos)
        regreso=[Fn,tos]
        #print(regreso)
        return regreso

    # Agregar la seleccion del mayor valor de Fn

Rango_Aplicabilidad = Rango_Aplicabilidad_funtion (Fn, Cp, L, B)
Fn = float(Rango_Aplicabilidad[0])
tipe_of_ship = Rango_Aplicabilidad[1]
print('\n')
print('Fn = ',Fn,', Tipo de embarcación = ',tipe_of_ship)
#Fn = 0.3

# %% [markdown]
# ## Calculo de Vs

# %%
def Vs_funtion (Fn,g,Ls):
    aux111= g * Ls
    aux111 = math.sqrt(aux111)
    out = Fn * aux111
    return out
    
Vs = Vs_funtion(Fn,g,Ls)
print('Vs = ',Vs)

# %% [markdown]
# ## Calculo de Re_s

# %%
def Re_s_funtion(Vs,Ls,Visc_a_s):
    Re_s = Vs * Ls / Visc_a_s
    return Re_s
    
Re_s = Re_s_funtion(Vs,Ls,Visc_a_s)
print('Reinold = ',Re_s)

# %% [markdown]
# ## Calculo de Cf

# %%
def Cf_funtion (Re_s):
    Cf = (0.075 / ((np.log10(Re_s) - 2)**2))
    return Cf
    
Cf = Cf_funtion (Re_s)
print('Cf = ',Cf)

# %% [markdown]
# ## Calculo de Rf

# %%
def Rf_funtion (Cf,Dens_a_s,Ss,Vs):
    Rf = Cf*((1/2)*Dens_a_s*Ss*Vs**2)
    return Rf
    
Rf = Rf_funtion(Cf,Dens_a_s,Ss,Vs)
print('Rf = ',Rf)

# %% [markdown]
# ## Calculo de Lcb

# %%
def Lcb_funtion(LCB,Ls):
   Lcb = ((Ls/2)-(LCB))/Ls
   return Lcb
   
Lcb = Lcb_funtion(LCB,Ls)
print('Lcb = ',Lcb)

# %% [markdown]
# ## Calculo de Lr 

# %%
def Lr_funtion(L,Cp,Lcb):
    Lr = L * ((1 - Cp) + (0.06 * Cp * Lcb) / ((4 * Cp) - 1))
    return Lr
    
Lr = Lr_funtion(L,Cp,Lcb)
print('Lr = ',Lr)

# %% [markdown]
# ## Calculo de C12

# %%
def C12_funtion(T,L):
    if T/L > 0.05:
        C12 = (T/L)**0.2228446
    elif 0.02 < T/L <= 0.05:
        C12 = 48.20 * ((T/L - 0.02)**2.078) + 0.479948
    elif T/L < 0.02:
        C12 = 0.479948
    return C12

C12 = C12_funtion(T,L)
print('C12 = ',C12)

# %% [markdown]
# ## Calculo de C13

# %%
def C13_funtion(Afterbody_form):
    if Afterbody_form == 0:
        C_stern = -25
    elif Afterbody_form == 1:
        C_stern = -10
    elif Afterbody_form == 2:
        C_stern = 0
    elif Afterbody_form == 3:
        C_stern = 10
    
    C13 = 1 + (0.003 * C_stern)
    return C13
    
C13 = C13_funtion(Afterbody_form)
print('C13 = ',C13)

# %% [markdown]
# ## triangulo 
# ### preguntar por la variable M en la formula(B)

# %%
def triangulo_funtion(Cb,LWL,T,B):
    triangulo = Cb * LWL * T * B
    return triangulo
    
triangulo = triangulo_funtion(Cb,LWL,T,B)
print('Volumen = ',triangulo)

# %% [markdown]
# ## Calculo de C14

# %%
def C14_funtion(Afterbody_form):
    if Afterbody_form == 0:
        C_stern = -25
    elif Afterbody_form == 1:
        C_stern = -10
    elif Afterbody_form == 2:
        C_stern = 0
    elif Afterbody_form == 3:
        C_stern = 10
    
    C14 = 1 + (0.011 * C_stern)
    return C13
    
C14 = C14_funtion(Afterbody_form)
print('C14 = ',C14)

# %% [markdown]
# ## Calculo de K + 1
# %% [markdown]
# ## Calculo de prueba Rf * (K+1)

# %%
def K_mas_1_funtion (C13,C12,B,Lr,Lcb,C14,triangulo):
    if Fn <= 0.5:

        def z_funtion(Lcb,Cp):
            z = (1 - Cp + (0.0225 * Lcb))**0.6906
            return(z)
        def y_funtion(Cp):
            y = (0.95 - Cp)**(-0.521448)
            return(y)
        def x_funtion(C12,B,Lr):
            x = C12 * ((B/Lr)**0.92497)
            return(x)

        z = z_funtion(Lcb,Cp)
        y = y_funtion(Cp)
        x = x_funtion(C12,B,Lr)
        k_1 = C13*(0.93 + x * y * z)
        return k_1

    else:
        def x_funtion(C14,B,L):
            x = C14 * (B/L)**1.06806
            return(x)
        def y_funtion(T,L):
            y = (T/L)**0.46106
            return(y)
        def z_funtion(L,Lr):
            z = (L/Lr)**0.121563
            return(z)
        def a_funtion(L,triangulo):
            a = ( (L**3) / triangulo )**0.36486
            return(a)
        def b_funtion(Cp):
            b = (1 + Cp)**(-0.604247)
            return b

        z = z_funtion(L,Lr)
        y = y_funtion(T,L)
        x = x_funtion(C14,B,L)
        a = a_funtion(L,triangulo)
        b = b_funtion(Cp)
        k_1 = 0.93 + (0.48711 * x * y * z * a *b)
        return k_1
        
K_mas_1 = K_mas_1_funtion (C13,C12,B,Lr,Lcb,C14,triangulo)
print('K + 1 = ',K_mas_1)

# %% [markdown]
# ## Prueba K_mas1 * Rf

# %%
def prueba_Rf(K_mas_1, Rf):
    x = K_mas_1 * Rf
    return x
    
x = prueba_Rf(K_mas_1, Rf)
print('Rf * (k+1) = ',x)

# %% [markdown]
# # Calculo de Rw
# %% [markdown]
# ## C7

# %%
def C7_funtion(L,B):
    B_L = B/L
    if B_L < 0.11:
        C7 = 0.229577 * (B_L**0.33333)
    elif B_L >= 0.11 and B_L <= 0.25:
        C7 = B_L
    elif B_L > 0.25 :
        C7 = 0.5 - 0.0625*(L/B)
    return C7
    
C7 = C7_funtion(L,B)
print('C7 = ', C7)

# %% [markdown]
# ## C15

# %%
def C15_funtion(L,triangulo):
    n = (L ** 3)/triangulo
    if n < 512 :
        C15 = -1.69385
    elif n > 1727:
        C15 = 0
    else:
        C15 = -1.69385 + ((L/(triangulo ** (1/3)))-0.8) / 2.36
    return C15
    
C15 = C15_funtion(L,triangulo)
print('C15 = ',C15)

# %% [markdown]
# ## M3

# %%
def M3_funtion(B,L,T):
    M3 = -7.2035 * ((B/L)**0.326869) * ( (T/B)**0.605375 )
    return M3
    
M3 = M3_funtion(B,L,T)
print('M3 = ',M3)

# %% [markdown]
# ## M4 

# %%
def M4_funtion(C15, Fn):
    M4 = C15 * 0.4 * math.exp(-0.034*(Fn ** (-3.29)))
    return M4
    
M4 = M4_funtion(C15, Fn)
print('M4 = ',M4)

# %% [markdown]
# ## C16

# %%
def C16_funtion(Cp):
    if Cp < 0.8:
        C16 = 8.07981 * Cp - 13.8673 * (Cp ** 2) + 6.984388 * (Cp ** 3)
    else:
        C16 = 1.73014 - 0.7067 * Cp
    return C16
    
C16 =C16_funtion(Cp)
print('C16 = ',C16)

# %% [markdown]
# ## C17

# %%
def C17_funtion(Cm,triangulo,L):
    C17 = 6919.3 * (Cm**(-1.3346)) * ( ( triangulo/(L**3) )**2.00977)
    return C17
    
C17 =  C17_funtion(Cm,triangulo,L)
print('C17 = ',C17)

# %% [markdown]
# ## M1

# %%
def M1_funtion(L,T,triangulo,B,C16):
    M1 = 0.0140407 * (L/T) - (1.75254 * (triangulo**(1/3))/L) - 4.79323 * (B/L) - C16
    return M1
    
M1 = M1_funtion(L,T,triangulo,B,C16)
print('M1 = ',M1)

# %% [markdown]
# ## Lamda

# %%
def Lamda_funtion(L,B,Cp):
    L_B = L/B
    if L_B < 12 :
        Lamda = 1.446 * Cp - 0.03 * L_B
    elif L_B >= 12:
        Lamda = 1.446 * Cp - 0.36
    return Lamda
    
Lamda = Lamda_funtion(L,B,Cp)
print('Lambda = ',Lamda)

# %% [markdown]
# ## C5

# %%
def C5_funtion(At,B,T,Cm):
    C5 =1 - ((0.8 * At))/(B * T * Cm)
    return C5
    
C5 = C5_funtion(At,B,T,Cm)
print('C5 = ',C5)

# %% [markdown]
# ## C3

# %%
def C3_funtion(Abt,B,T,hb):
    def x_funtion(Abt):
        x = 0.56 *(Abt**1.5)
        return x
    def y_funtion(B,T,Abt,hb):
        y = B * T * (0.31 * (Abt ** (1/2)) + T - hb)
        return y
    x = x_funtion(Abt)
    y = y_funtion(B,T,Abt,hb)

    C3 = x/y
    return C3

C3 = C3_funtion(Abt,B,T,hb)
print('C3 = ',C3) 

# %% [markdown]
# ## C2

# %%
def C2_funtion(C3):
    C2 = math.exp(-1.89 * ((C3)**(1/2)))
    return C2

C2 = C2_funtion(C3)
print('C2 = ',C2)

# %% [markdown]
# ## ie

# %%
## Define funcion para ie
def ie_funtion(L,B,Cwp,Cp,Lcb,Lr,triangulo):

    def expo_funtion(L,B,Cwp,Cp,Lcb,Lr,triangulo):
        expo = ( -(L/B) ** 0.80856 ) * ( (1 - Cwp) ** 0.30484 ) * (( 1 - Cp - 0.0225 * Lcb) ** 0.6367 ) * ( (Lr/B) ** 0.34574 ) * ((100 * triangulo / (L ** 3)) ** 0.16302)
        return expo
    expo = expo_funtion(L,B,Cwp,Cp,Lcb,Lr,triangulo)
    ie = 1 + 89 * math.exp(expo)
    return ie
## verifica si se definió, sino, se calcula
if ie_test == False:
    ie = ie_funtion(L,B,Cwp,Cp,Lcb,Lr,triangulo)

print('ie = ',ie)

# %% [markdown]
# ## C1

# %%
def C1_futnion(C7, T,B,ie):
    def x_funtion(C7):
        x = 2223105 * (C7**3.78613)
        return x
    def y_funtion(T,B):
        y = (T/B)**1.07961
        return y
    def z_funtion(ie):
        z = (90 - ie)**(-1.37565)
        return z

    x = x_funtion(C7)
    y = y_funtion(T,B)
    z = z_funtion(ie)

    C1 = x*y*z
    return C1
    
C1 = C1_futnion(C7, T,B,ie)
print('C1 = ',C1)

# %% [markdown]
# ## RW 

# %%
# Rw_a-----------------------
def Rw_a_funtion(C1,C2,C5,triangulo,Dens_a_s,M1,Fn,M4,Lamda,g):
    d = -0.9 
    def expo_funtion(Fn,M1,d,M4,Lamda):
        expo = (M1 * (Fn**d)) + (M4 * math.cos(Lamda * (Fn**(-2))))     #resultado en radianes del exponente
        return expo
    expo = expo_funtion(Fn,M1,d,M4,Lamda)
    Rw_a = C1 * C2 * C5 * triangulo * Dens_a_s * g * math.exp(expo)       
    # -6.5401587 resultado en grados hexadecimales del exponente
    return Rw_a
# Rw_b -------------------------------------
def Rw_b_funtion(C17,C2,C5,triangulo,Dens_a_s,M3,Fn,M4,Lamda):
    d = -0.9
    def expo_funtion(Fn,M3,d,M4,Lamda):
        expo = (M3 * (Fn**d)) + (M4 * math.cos(Lamda * (Fn**(-2))))
        return expo
    expo = expo_funtion(Fn,M3,d,M4,Lamda)
    Rw_b = C17 * C2 * C5 * triangulo * Dens_a_s * g * math.exp(expo)
    return Rw_b

# Rw-----------------------------------------
def Rw_funtion(C1,C2,C5,triangulo,Dens_a_s,M1,Fn,M4,Lamda,g,C17,M3):

    if (Fn < 0.4):
        Rw = Rw_a_funtion(C1,C2,C5,triangulo,Dens_a_s,M1,Fn,M4,Lamda,g)
        print('Fn < 0.4')
    elif (Fn >= 0.4) and (Fn <= 0.55):
        Rw_a = Rw_a_funtion(C1,C2,C5,triangulo,Dens_a_s,M1,0.4,M4,Lamda,g)
        Rw_b = Rw_b_funtion(C17,C2,C5,triangulo,Dens_a_s,M3,0.55,M4,Lamda)

        Rw = Rw_a + (10 * Fn - 4) * ((Rw_b - Rw_a)/1.5)         # Rw*
        print('0.4 <= Fn <= 0.5')
    elif (Fn > 0.5): 
        Rw = Rw_b_funtion(C17,C2,C5,triangulo,Dens_a_s,M3,Fn,M4,Lamda)
        print('Fn > 0.5')
    return Rw

Rw = Rw_funtion(C1,C2,C5,triangulo,Dens_a_s,M1,Fn,M4,Lamda,g,C17,M3)
print('Rw = ',Rw)

# %% [markdown]
# ## Rb 
# ### Resistencia por bulbo
# %% [markdown]
# ## Pb

# %%
Tf = T
def Pb_funtion(Abt,Tf,hb):
    Pb = 0.56 * (Abt ** (1/2)) / (Tf - 1.5 * hb)
    return Pb
    
Pb = Pb_funtion(Abt,Tf,hb)
print('Pb = ',Pb)

# %% [markdown]
# ## Fn_i

# %%
def Fn_i_funtion(Vs,g,Tf,hb,Abt):
    Fn_i = Vs / (g*(Tf - hb - 0.25 * (Abt ** 0.5)) + 0.15 * (Vs ** 2)) ** 0.5
    return Fn_i
    
Fn_i = Fn_i_funtion(Vs,g,Tf,hb,Abt)
print ('Fn_i = ',Fn_i)

# %% [markdown]
# ## Rb

# %%
def Rb_funtion(Pb,Fn_i,Abt,Dens_a_s,g):
    Rb = 0.11 * math.exp(-3 * (Pb ** (-2))) * (Fn_i ** 3) * (Abt ** 1.5) * Dens_a_s * g /(1 + (Fn_i ** 2))
    return Rb
    
Rb = Rb_funtion(Pb,Fn_i,Abt,Dens_a_s,g)
print ('Rb = ',Rb)

# %% [markdown]
# # Rtr Resistencia por espejo sumergido
# %% [markdown]
# ## Fn_T 

# %%
def Fn_t_funtion(Vs,g,At,B,Cwp):
    Fn_t = Vs / (((2*g*At) / (B+B*Cwp)) ** 0.5)
    return Fn_t

Fn_t = Fn_t_funtion(Vs,g,At,B,Cwp)
print('Fn_t = ',Fn_t)

# %% [markdown]
# ## C6 

# %%
def C6_funtion(Fn_t):
    if Fn_t < 5:
        C6 = 0.2 * (1 - 0.2 * Fn_t)
    else:
        C6 = 0
    return C6

C6 = C6_funtion(Fn_t)
print('C6 = ',C6)

# %% [markdown]
# ## Rtr

# %%
def Rtr_funtion(Dens_a_s,Vs,At,C6):
    Rtr = 0.5 * Dens_a_s * (Vs ** 2) * At * C6
    return Rtr

Rtr = Rtr_funtion(Dens_a_s,Vs,At,C6)
print('Rtr = ',Rtr)

# %% [markdown]
# ## Ra Resistencia por correlación
# %% [markdown]
# ## C4

# %%
Tf = T
def C4_funtion(Tf,L):
    Tf_L = Tf / L
    if Tf_L <= 0.04:
        C4 = Tf_L
    else:
        C4 = 0.04
    return C4
    
C4 = C4_funtion(Tf,L)
print('C4 = ',C4)

# %% [markdown]
# ## Ca  ¿Se le coloca el incremento ?
# ### al ejercicio no se le coloca incremento

# %%
def Ca_funtion(L,Cb,C2,C4):
    ks = 150
    Ca = 0.006 * ((L + 100) ** -0.16) - 0.00205 + 0.003 * ((L/7.5) ** 0.5) * (Cb ** 4) * C2* (0.04 - C4)
    # no incluir incremento de de Ca
    #incremento = (0.105 * (ks ** (1/3)) - 0.005579) / (L ** (1/3))
    Ca_in = Ca 
    return Ca   # no se coloca el incremento

Ca =  Ca_funtion(L,Cb,C2,C4)
print('Ca = ',Ca)

# %% [markdown]
# ## Ra

# %%
def Ra_funtion(Dens_a_s,Vs,S,Ca):
    Ra = 0.5 * Dens_a_s * (Vs ** 2) * S * Ca
    return Ra

Ra = Ra_funtion(Dens_a_s,Vs,S,Ca)
print('Ra = ',Ra)

# %% [markdown]
# # Rapp
# 
# %% [markdown]
# ## Tabla de K_2 + 1

# %%
na = np.nan
tabla_K2_mas_1 = pd.DataFrame({'Apendices':['Rudder behind skeg', 'Rudder Behind stern', 'Twin-screw balance rudders', 'shaft brackets', 'Skeg', 'Strut bossings', 'hull bossings', 'Shafts', 'Stabilizer fins', 'Dome', 'Bilge keels'],'K2 + 1 min':[2,1.5,2.8,3,2,3,2,4,2.8,2.7,1.4]})
#print(tabla_K2_mas_1)

# %% [markdown]
# ## K_mas_1 equivalente

# %%
def K2_mas_1_eq_funtion(Sapp,tabla_K2_mas_1):
    x = input("Ingrese la cantidad de apendices de la embarcación : \n")
    x = int(x)
    Sapp = 0
    apendice = list(range(0,x))
    Sapp_i = list(range(0,x))
    K2_mas_1 = list(range(0,x))

    if x == 0:
        K2_mas_1_eq = 0
    else:
        apendice = list(range(0,x))
        Sapp_i = list(range(0,x))
        K2_mas_1 = list(range(0,x))
        
        print('\n')
        for i in list(range(0,x)):
            print(tabla_K2_mas_1)
            apendice[i]= int(input('ingrese el numero correspondiente al apendice en la tabla:\n'))
            Sapp_i[i] = float(input('ingrese el Area correspondiente al apendice [m]\n'))
            K2_mas_1[i] = tabla_K2_mas_1.iloc[apendice[i],1]
            print('\n \n')
        Numerador_1 = 0
        Denominador_1 = 0
        for i in list(range(0,x)):
            Numerador_1 = K2_mas_1[i]*Sapp_i[i] + Numerador_1
            Denominador_1 = Sapp_i[i] + Denominador_1

        Sapp = Denominador_1
        K2_mas_1_eq = Numerador_1 / Denominador_1   #resistencia sin Bow Thruster
        #print(apendice)
        #print(Sapp_i)
        #print(K2_mas_1)
    return K2_mas_1_eq, Sapp

Tabla_aux2 = K2_mas_1_eq_funtion(Sapp,tabla_K2_mas_1)
Sapp = Tabla_aux2[1]
K2_mas_1_eq = Tabla_aux2[0]
print('K2 + 1 eq = ',K2_mas_1_eq) 
print('Sapp = ',Sapp)

# %% [markdown]
# ##  Rapp = Rapp  + Rapp_bto

# %%
def Rapp_funtion(Dens_a_s,Vs,Sapp,K2_mas_1_eq,Cf):
    Rapp_bt = Dens_a_s * Vs**2 * np.pi * d_bto**2 * C_bto
    print(Rapp_bt)
    Rapp_simple = 0.5 * Dens_a_s * (Vs**2) * Sapp * K2_mas_1_eq * Cf
    Rapp = Rapp_simple + Rapp_bt
    return Rapp
Rapp = Rapp_funtion(Dens_a_s,Vs,Sapp,K2_mas_1_eq,Cf)
print('Rapp = ',Rapp)

# %% [markdown]
# # Resistencia total

# %%
def Rt_funtion(K_mas_1,Rf,Rw,Rb,Rtr,Rapp,Ra):
    Rt = (K_mas_1)*Rf + Rw + Rb + Rtr + Rapp + Ra
    return Rt
Rt = Rt_funtion(K_mas_1,Rf,Rw,Rb,Rtr,Rapp,Ra)
print('K + 1 = ', K_mas_1, ', Rf = ', Rf, ',')
print('Rw = ', Rw, ', Rb = ', Rb, ', Rtr = ', Rtr, ', Rapp = ', Rapp, ', Ra = ', Ra)
print('Rt = (K_mas_1)*Rf + Rw + Rb + Rtr + Rapp + Ra')
print('Rt = ', Rt)


# %%



