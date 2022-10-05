#%%
from operator import index
from re import A
from unicodedata import name
import pandas as pd
import numpy as np



#df4 = pd.read_csv(
 #   "/Users/fede/Desktop/Metodología de la OP/probandopy.csv",
  #  delimiter=',',       # delimitador ',',';','|','\t'
   # header=0,            # número de fila como nombre de columna
    #names=None,          # nombre de las columnas (ojo con header)
    #index_col=0,         # que col es el índice
    #usecols=None,        # que col usar. Ej: [0, 1, 2], ['foo', 'bar', 'baz']
    #dtype=None,          # Tipo de col {'a': np.int32, 'b': str} 
    #skiprows=None,       # saltear filas al inicio
    #skipfooter=0,        # saltear filas al final
    #nrows=None,          # n de filas a leer
    #decimal='.',         # separador de decimal. Ej: ',' para EU dat
    #quotechar='"',       # char para reconocer str
    #encoding=None,      # archivos con tilde y ñ por lo general utilizan "utf-8" etc 
#)
#AGREGO UNA COLUMNA QUE NO ESTABA EN LA BASE DE DATOS ORIGINAL
#Agrego un index pisando el otro
#df4.index = ('AMC Concord', 'AMC Pacer', 'AMC Spirit', 'Buick Century', 'Buick Electra', 'Buick LeSabre', 'Buick Opel', 'Buick Regal','Buick Riviera', 'Buick Skylark', 'Cad. Deville', 'Cad. Eldorado', 'Cad. Seville', 'Chev. Chevette', 'Chev. Impala', 'Chev. Malibu', 'Chev. Monte Carlo', 'Chev. Monza', 'Chev. Nova', 'Dodge Colt','Dodge Diplomat', 'Dodge Magnum', 'Dodge St. Regis', 'Ford Fiesta','Ford Mustang', 'Linc. Continental', 'Linc. Mark V', 'Linc. Versailles','Merc. Bobcat', 'Merc. Cougar', 'Merc. Marquis', 'Merc. Monarch','Merc. XR-7', 'Merc. Zephyr', 'Olds 98', 'Olds Cutl Supr','Olds Cutlass', 'Olds Delta 88', 'Olds Omega', 'Olds Starfire', 'Olds Toronado', 'Plym. Arrow', 'Plym. Champ', 'Plym. Horizon','Plym. Sapporo', 'Plym. Volare', 'Pont. Catalina', 'Pont. Firebird','Pont. Grand Prix', 'Pont. Le Mans', 'Pont. Phoenix', 'Pont. Sunbird','Audi 5000', 'Audi Fox', 'BMW 320i', 'Datsun 200', 'Datsun 210','Datsun 510', 'Datsun 810', 'Fiat Strada', 'Honda Accord','Honda Civic', 'Mazda GLC', 'Peugeot 604', 'Renault Le Car', 'Subaru','Toyota Celica', 'Toyota Corolla', 'Toyota Corona', 'VW Dasher', 'VW Diesel', 'VW Rabbit', 'VW Scirocco', 'Volvo 260')
#armo la columna que perdi al pisarla en el index y la agrego.
#prices = [ 4099,  4749,  3799,  4816,  7827,  5788,  4453,  5189, 10372, 4082, 11385, 14500, 15906,  3299,  5705,  4504,  5104,  3667, 3955,  3984,  4010,  5886,  6342,  4389,  4187, 11497, 13594, 13466,  3829,  5379,  6165,  4516,  6303,  3291,  8814,  5172, 4733,  4890,  4181,  4195, 10371,  4647,  4425,  4482,  6486, 4060,  5798,  4934,  5222,  4723,  4424,  4172,  9690,  6295, 9735,  6229,  4589,  5079,  8129,  4296,  5799,  4499,  3995, 12990,  3895,  3798,  5899,  3748,  5719,  7140,  5397,  4697, 6850, 11995]
#df4["prices"] = prices
#cambio la posición de la colmna que arme para que quede primera
#df4 = df4.reindex(columns=["prices", "mpg",  "rep78",  "headroom", "trunk",  "weight", "length",  "turn", "displacement", "gear_ratio", "foreig"  ])
#df4.reset_index(inplace= True)
#print(df4.sort_values(by = ["prices"], ascending=False)) ORDENA DE MAYOR A MENOR --- print(df4.min())  print(df4.max())
# df4[["price","weight"]]

#print(df4)

#print(df4.iloc[1:6,0:3])
#print("AAAAAAAAAAAAAAAAAAAAAAAAAAAA")
#a = df4.loc[(df4["prices"] == 12990)|
#    (df4["prices"] == 4816)|
#    (df4["trunk"] == 11), 
#    ["prices","mpg","foreig","trunk"]]
#print(a)
#print(df4.describe())


#print((df4.groupby(["foreig","rep78","prices"])
#    .size()
#    .to_frame(name="count")
#))



#%%
#%%
#PIVOTEAR



#Creamos un dataframe para probar stack
#df7 = df4.groupby(["foreig","headroom","rep78"])[["prices","mpg","weight"]].mean()
#df7 = df7.stack().to_frame(name="Valor") #Cambio el nombre de la columna 0
#print(df7)


#Cantidad de reparaciones en 1978 según origen.
# df10= pd.crosstab(df4.foreig,df4.rep78)
#print(df10)



# Un profesor desea obtener rápidamente los nombres y las notas de sus alumnos aprobados. 
# Se pide realizar una función que reciba un diccionario con las notas de los alumnos y devuelva una serie con las notas 
# de los alumnos aprobados ordenadas de mayor a menor y de menor a mayor. La materia se aprueba con 7.

#def alumnos_notas(x):
 #   serie = pd.Series(x)
  #  df1=pd.DataFrame(serie,columns=["notas"])
   # serie1 = serie.loc[(["notas"] >= 7)] 
    #print("Las notas en orden descendente son: ", serie1.sort_values(by=["notas"]))
   # print("Las notas en orden ascendentes son: ", serie1.sort_values(by=["notas"]))




#a = {"Juan": 6, "Manuel":10, "Ricardo":2, "Salma":10, "Denis":7, "Ivan":8, "bruno": 9}
#alumnos_notas(a)

# %%
#df4 = pd.read_csv(
 #   "/Users/fede/Desktop/Metodología de la OP/probandopy.csv",
  #  delimiter=',',       # delimitador ',',';','|','\t'
   # header=0,            # número de fila como nombre de columna
    #names=None,          # nombre de las columnas (ojo con header)
    #index_col=0,         # que col es el índice
    #usecols=None,        # que col usar. Ej: [0, 1, 2], ['foo', 'bar', 'baz']
    #dtype=None,          # Tipo de col {'a': np.int32, 'b': str} 
    #skiprows=None,       # saltear filas al inicio
    #skipfooter=0,        # saltear filas al final
    #nrows=None,          # n de filas a leer
    #decimal='.',         # separador de decimal. Ej: ',' para EU dat
    #quotechar='"',       # char para reconocer str
    #encoding=None,      # archivos con tilde y ñ por lo general utilizan "utf-8" etc 
#%%
resultados_paso = pd.read_csv(
    "/Users/fede/Desktop/Metodología de la OP/Competencia/paso_x_partido.csv",
    delimiter=',',       # delimitador ',',';','|','\t'
    header=0,            # número de fila como nombre de columna
    names=None,          # nombre de las columnas (ojo con header)
    index_col=0,         # que col es el índice
    usecols=None,        # que col usar. Ej: [0, 1, 2], ['foo', 'bar', 'baz']
    dtype=None,          # Tipo de col {'a': np.int32, 'b': str} 
    skiprows=None,       # saltear filas al inicio
    skipfooter=0,        # saltear filas al final
    nrows=None,          # n de filas a leer
    decimal='.',         # separador de decimal. Ej: ',' para EU dat
    quotechar='"',       # char para reconocer str
    encoding=None,
      )

resultados_paso      # archivos con tilde y ñ por lo general utilizan "utf-8" etc 

comunas = pd.read_csv(
    "/Users/fede/Desktop/Metodología de la OP/Competencia/circuitos-electorales.csv",
    delimiter=',',       # delimitador ',',';','|','\t'
    header=0,            # número de fila como nombre de columna
    names=None,          # nombre de las columnas (ojo con header)
    index_col=0,         # que col es el índice
    usecols=None,        # que col usar. Ej: [0, 1, 2], ['foo', 'bar', 'baz']
    dtype=None,          # Tipo de col {'a': np.int32, 'b': str} 
    skiprows=None,       # saltear filas al inicio
    skipfooter=0,        # saltear filas al final
    nrows=None,          # n de filas a leer
    decimal='.',         # separador de decimal. Ej: ',' para EU dat
    quotechar='"',       # char para reconocer str
    encoding=None,
      )
comunas
circuito_comuna = comunas[["COMUNA","CIRCUITO_N","BARRIO"]].rename(columns={"CIRCUITO_N":"circuito"})
circuito_comuna = circuito_comuna.sort_values(by=["circuito"])
circuito_comuna = circuito_comuna.reset_index(drop=True)
#print(circuito_comuna)
print(resultados_paso)

tabla_final= pd.merge(resultados_paso, circuito_comuna, on="circuito", how="outer", indicator=True)

tabla_final

agrupados_x_comuna = tabla_final[["pp1","pp2","pp3","pp4","nv"]].groupby(tabla_final["COMUNA"]).sum()
agrupados_x_circuito = tabla_final[["pp1","pp2","pp3","pp4","nv"]].groupby(tabla_final["circuito"]).sum()
agrupados_x_barrio = tabla_final[["pp1","pp2","pp3","pp4","nv"]].groupby(tabla_final["BARRIO"]).sum()

print(agrupados_x_barrio)
print(agrupados_x_comuna)
print(agrupados_x_circuito)



import geopandas as gp
import numpy as np






#%%
