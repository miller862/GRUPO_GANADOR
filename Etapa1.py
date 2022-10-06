# %%
from enum import unique
from itertools import groupby
from pydoc import describe
from tokenize import group


from itertools import count
from statistics import geometric_mean
import pandas as pd
import numpy as np

# %%
resultados_paso = pd.read_csv(
    "paso_x_partido.csv" "",
    delimiter=",",  # delimitador ',',';','|','\t'
    header=0,  # número de fila como nombre de columna
    names=None,  # nombre de las columnas (ojo con header)
    index_col=0,  # que col es el índice
    usecols=None,  # que col usar. Ej: [0, 1, 2], ['foo', 'bar', 'baz']
    dtype=None,  # Tipo de col {'a': np.int32, 'b': str}
    skiprows=None,  # saltear filas al inicio
    skipfooter=0,  # saltear filas al final
    nrows=None,  # n de filas a leer
    decimal=".",  # separador de decimal. Ej: ',' para EU dat
    quotechar='"',  # char para reconocer str
    encoding=None,
)

resultados_paso  # archivos con tilde y ñ por lo general utilizan "utf-8" etc
#%%
comunas = pd.read_csv(
    "circuitos-electorales.csv",
    delimiter=",",  # delimitador ',',';','|','\t'
    header=0,  # número de fila como nombre de columna
    names=None,  # nombre de las columnas (ojo con header)
    index_col=0,  # que col es el índice
    usecols=None,  # que col usar. Ej: [0, 1, 2], ['foo', 'bar', 'baz']
    dtype=None,  # Tipo de col {'a': np.int32, 'b': str}
    skiprows=None,  # saltear filas al inicio
    skipfooter=0,  # saltear filas al final
    nrows=None,  # n de filas a leer
    decimal=".",  # separador de decimal. Ej: ',' para EU dat
    quotechar='"',  # char para reconocer str
    encoding=None,
)
comunas
# %%
circuito_comuna = comunas[["COMUNA", "CIRCUITO_N", "BARRIO"]].rename(
    columns={"CIRCUITO_N": "circuito"}
)
circuito_comuna = circuito_comuna.sort_values(by=["circuito"])
circuito_comuna = circuito_comuna.reset_index(drop=True)

tabla_final = pd.merge(
    resultados_paso, circuito_comuna, on="circuito", how="outer", indicator=True
)
tabla_final
# %%
# PORCENTAJE SOBRE EL PROPIO CANDIDATO
distrib_candidatos = (
    tabla_final[["COMUNA", "pp1", "pp2", "pp3", "pp4", "nv", "BARRIO"]]
    .groupby(["COMUNA"])
    .sum()
    .transform(lambda x: (x + 0.0) / x.sum() * 100)
)
distrib_candidatos
# %%
total_votos_x_comunas = (
    tabla_final[["COMUNA", "pp1", "pp2", "pp3", "pp4", "nv", "BARRIO"]]
    .groupby(["COMUNA"])
    .sum()
)
total_votos_x_comunas
total_votos_x_candidatos = total_votos_x_comunas.sum()
total_votos_x_candidatos
#%%
total_votos_x_comunas = total_votos_x_comunas.assign(
    total_x_comuna=lambda x: (x["pp1"] + x["pp2"] + x["pp3"] + x["pp4"] + x["nv"])
)
total_votos_x_comunas
# %%
# PORCENTAJE DE VOTOS POR COMUNA
porcentaje_votos_x_comunas = total_votos_x_comunas.transform(
    (lambda x: (x + 0.0) / x["total_x_comuna"] * 100), axis=1
)
porcentaje_votos_x_comunas
# %%
porcentaje_orden = porcentaje_votos_x_comunas.sort_values(["pp3"], ascending=False)
porcentaje_orden.style  # .background_gradient(cmap="viridis")

# %%
hogar = pd.read_csv("censo/hogar.csv", sep=",")
hogar
#%%
vivienda = pd.read_csv("censo/vivienda.csv", sep=",")
vivienda
# %%
persona = pd.read_csv("censo/persona.csv", sep=",")
persona
# %%
prov = pd.read_csv("censo/prov.csv", sep=",")
prov
# %%
radio = pd.read_csv("censo/radio.csv")
radio
# %%
frac = pd.read_csv("censo/frac.csv")
frac
#%%
dpto = pd.read_csv("censo/dpto.csv")
dpto = dpto[["DPTO_REF_ID", "NOMDPTO"]]
dpto
# %%
dpto_frac = pd.merge(dpto, frac, on="DPTO_REF_ID", how="left")
dpto_frac.groupby = ["NOMDPTO"]
dpto_frac
# %%
dpto_frac_radio = pd.merge(dpto_frac, radio, on="FRAC_REF_ID", how="right")
dpto_frac_radio

# %%
dpto_frac_radio_vivienda = pd.merge(
    dpto_frac_radio, vivienda, on="RADIO_REF_ID", how="right", indicator=True
)
dpto_frac_radio_vivienda.rename(columns={"DPTO_REF_ID": "COMUNA"}, inplace=True)
dpto_frac_radio_vivienda
#%%
# dpto_frac_radio_vivienda[dpto_frac_radio_vivienda.columns[[0,6,7,8,9,10,11,12,13,14,15,16,17]]]
dpto_frac_radio_vivienda = dpto_frac_radio_vivienda[
    dpto_frac_radio_vivienda.columns[[0, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]]
].copy()
# %%
dpto_frac_radio_vivienda
# %%
hogarSUPREMO = pd.merge(
    dpto_frac_radio_vivienda, hogar, on="VIVIENDA_REF_ID", how="right"
)
hogarSUPREMO
# %%
df100 = hogarSUPREMO.groupby(["COMUNA", "ALGUNBI"]).sum()
df100
# %%
personaSUPREMO = pd.merge(hogarSUPREMO, persona, on="HOGAR_REF_ID", how="right")
Votantes = personaSUPREMO[personaSUPREMO["P03"] >= 18]
Votantes



# %%
