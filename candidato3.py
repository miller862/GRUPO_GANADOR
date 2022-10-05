# %%
from itertools import count
import pandas as pd
import numpy as np
# %%
resultados_paso = pd.read_csv(
    "/Users/camilaherrero/Desktop/Python/met4opv/Candidato 3/paso_x_partido.csv",
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
    "/Users/camilaherrero/Desktop/Python/met4opv/Candidato 3/circuitos-electorales.csv",
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
#print(comunas)

# %%
circuito_comuna = comunas[["COMUNA","CIRCUITO_N","BARRIO"]].rename(columns={"CIRCUITO_N":"circuito"})
circuito_comuna = circuito_comuna.sort_values(by=["circuito"])
circuito_comuna = circuito_comuna.reset_index(drop=True)
#print(circuito_comuna)
#print(resultados_paso)

tabla_final= pd.merge(resultados_paso, circuito_comuna, on="circuito", how="outer", indicator=True)
print(tabla_final)
# %%

#agrup_circuito = tabla_final[["circuito","pp1","pp2","pp3", "pp4", "nv", "COMUNA", "BARRIO"]].groupby(tabla_final["circuito", "COMUNA"]).sum()
#print(agrup_circuito)


# %%
#agrup_cir = tabla_final.groupby(["circuito", "COMUNA", "urna"]).sum()
#print(agrup_cir)
# %%

agrup_comunas = tabla_final[["pp1","pp2","pp3", "pp4", "nv"]].groupby(tabla_final["COMUNA"]).sum()
print(agrup_comunas)

# %%
import pandas as pd, matplotlib.pyplot as plt, geopandas as gpd, contextily as ctx, numpy as np

# %%
