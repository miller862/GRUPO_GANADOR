# %%
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
# print(comunas)
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
porcentaje_orden


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
votantes = personaSUPREMO[personaSUPREMO["P03"] >= 18]
votantes
# %%
#COMUNA 1
is_comuna1 = votantes.loc[:,"COMUNA"] == 1
comuna1 = votantes[is_comuna1]
comuna1
# %%
#POBLACION COMUNA 1
comuna1_poblacion = comuna1[["COMUNA", "P03", "P05", "P07", "P08", "P09", "CONDACT"]].copy()
comuna1_poblacion
# %%
edad_c1 = comuna1_poblacion["P03"].describe()
edad_c1
# %%
moda_educacion_c1 = comuna1_poblacion["P09"].mode()
moda_educacion_c1

# %%
educacion_c1 = comuna1_poblacion.groupby(['P09']).count()
educacion_c1

#%%
porcentaje_educacion_c1 = educacion_c1.transform(
    (lambda x: (x + 0.0) / 168197 * 100), axis=1
)
porcentaje_educacion_c1

# %%
descripcion_educacion_c1 = comuna1_poblacion["P09"].describe()
descripcion_educacion_c1
# %%
moda_poblacion_actividad_c1 = comuna1_poblacion["CONDACT"].mode()
moda_poblacion_actividad_c1
# %%
poblacion_actividad_c1 = comuna1_poblacion.groupby(['CONDACT']).count()
poblacion_actividad_c1

# %%
porcentaje_actividad_c1 = poblacion_actividad_c1.transform(
    (lambda x: (x + 0.0) / 168197 * 100), axis=1
)
porcentaje_actividad_c1
# %%
#VIVIENDA COMUNA 1
comuna1_vivienda = comuna1[["COMUNA", "TIPVV", "V01", "INMAT", "INCALSERV", "INCALCONS"]].copy()
comuna1_vivienda
# %%
vivienda_agrupado_c1 = comuna1_vivienda["TIPVV"].mode()
vivienda_agrupado_c1
# %%
tipo_vivienda_c1 = comuna1_vivienda["V01"].mode()
tipo_vivienda_c1
# %%
cant_tipo_vivienda_c1 = comuna1_vivienda.groupby(['V01']).count()
cant_tipo_vivienda_c1

# %%
porcentaje_tipo_vivienda_c1 = cant_tipo_vivienda_c1.transform(
    (lambda x: (x + 0.0) / 168197 * 100), axis=1
)
porcentaje_tipo_vivienda_c1
# %%
moda_calidad_materiales_c1 = comuna1_vivienda["INMAT"].mode()
moda_calidad_materiales_c1
# %%
calidad_materiales_c1 = comuna1_vivienda.groupby(['INMAT']).count()
calidad_materiales_c1

# %%
porcentaje_calidad_materiales_c1 = calidad_materiales_c1.transform(
    (lambda x: (x + 0.0) / 168197 * 100), axis=1
)
porcentaje_calidad_materiales_c1
# %%
calidad_serv_c1 = comuna1_vivienda.groupby(['INCALSERV']).count()
calidad_serv_c1

# %%
porcentaje_calidad_serv_c1 = calidad_serv_c1.transform(
    (lambda x: (x + 0.0) / 168197 * 100), axis=1
)
porcentaje_calidad_serv_c1
# %%
calidad_cons_c1 = comuna1_vivienda.groupby(['INCALCONS']).count()
calidad_cons_c1

# %%
porcentaje_calidad_cons_c1 = calidad_cons_c1.transform(
    (lambda x: (x + 0.0) / 168197 * 100), axis=1
)
porcentaje_calidad_cons_c1
# %%
#HOGAR COMUNA 1
comuna1_hogar = comuna1[["COMUNA", "H05", "H06", "H07", "H08", "H09", "H10", "H13", "H16", "H19A", "H19B", "H19C", "PROP", "INDHAC"]].copy()
comuna1_hogar
# %%
hogar_agua_c1 = comuna1_hogar.groupby(['H08']).count()
hogar_agua_c1

# %%
porcentaje_agua_c1 = hogar_agua_c1.transform(
    (lambda x: (x + 0.0) / 168197 * 100), axis=1
)
porcentaje_agua_c1
# %%
hogar_bagno_c1 = comuna1_hogar.groupby(['H10']).count()
hogar_bagno_c1

# %%
porcentaje_bagno_c1 = hogar_bagno_c1.transform(
    (lambda x: (x + 0.0) / 168197 * 100), axis=1
)
porcentaje_bagno_c1
# %%
hogar_bagno_ex_c1 = comuna1_hogar.groupby(['H13']).count()
hogar_bagno_ex_c1

# %%
porcentaje_bagno_ex_c1 = hogar_bagno_ex_c1.transform(
    (lambda x: (x + 0.0) / 168197 * 100), axis=1
)
porcentaje_bagno_ex_c1
# %%
hogar_prop_c1 = comuna1_hogar.groupby(['PROP']).count()
hogar_prop_c1

# %%
porcentaje_hogar_prop_c1 = hogar_prop_c1.transform(
    (lambda x: (x + 0.0) / 168197 * 100), axis=1
)
porcentaje_hogar_prop_c1
# %%
hogar_hac_c1 = comuna1_hogar.groupby(['INDHAC']).count()
hogar_hac_c1

# %%
porcentaje_hogar_hac_c1 = hogar_hac_c1.transform(
    (lambda x: (x + 0.0) / 168197 * 100), axis=1
)
porcentaje_hogar_hac_c1
# %%
#COMUNA 2
is_comuna2 = votantes.loc[:,"COMUNA"] == 2
comuna2 = votantes[is_comuna2]
comuna2
# %%
#POBLACION COMUNA 2
comuna2_poblacion = comuna2[["COMUNA", "P03", "P05", "P07", "P08", "P09", "CONDACT"]].copy()
comuna2_poblacion
# %%
edad_c2 = comuna2_poblacion["P03"].describe()
edad_c2
# %%
moda_educacion_c2 = comuna2_poblacion["P09"].mode()
moda_educacion_c2
# %%
educacion_c2 = comuna2_poblacion.groupby(['P09']).count()
educacion_c2

# %%
porcentaje_educacion_c2 = educacion_c2.transform(
    (lambda x: (x + 0.0) / 136894 * 100), axis=1
)
porcentaje_educacion_c2
# %%
poblacion_actividad_c2 = comuna2_poblacion.groupby(['CONDACT']).count()
poblacion_actividad_c2

# %%
porcentaje_actividad_c2 = poblacion_actividad_c2.transform(
    (lambda x: (x + 0.0) / 136894 * 100), axis=1
)
porcentaje_actividad_c2
# %%
#VIVIENDA COMUNA 2
comuna2_vivienda = comuna2[["COMUNA", "TIPVV", "V01", "INMAT", "INCALSERV", "INCALCONS"]].copy()
comuna2_vivienda
# %%
cant_tipo_vivienda_c2 = comuna2_vivienda.groupby(['V01']).count()
cant_tipo_vivienda_c2

# %%
porcentaje_tipo_vivienda_c2 = cant_tipo_vivienda_c2.transform(
    (lambda x: (x + 0.0) / 136894 * 100), axis=1
)
porcentaje_tipo_vivienda_c2
# %%
calidad_materiales_c2 = comuna2_vivienda.groupby(['INMAT']).count()
calidad_materiales_c2

# %%
porcentaje_calidad_materiales_c2 = calidad_materiales_c2.transform(
    (lambda x: (x + 0.0) / 136894 * 100), axis=1
)
porcentaje_calidad_materiales_c2
# %%
calidad_serv_c2 = comuna2_vivienda.groupby(['INCALSERV']).count()
calidad_serv_c2

# %%
porcentaje_calidad_serv_c2 = calidad_serv_c2.transform(
    (lambda x: (x + 0.0) / 136894 * 100), axis=1
)
porcentaje_calidad_serv_c2
# %%
calidad_cons_c2 = comuna2_vivienda.groupby(['INCALCONS']).count()
calidad_cons_c2
# %%
porcentaje_calidad_cons_c2 = calidad_cons_c2.transform(
    (lambda x: (x + 0.0) / 136894 * 100), axis=1
)
porcentaje_calidad_cons_c2
# %%
#HOGAR COMUNA 2
comuna2_hogar = comuna2[["COMUNA", "H05", "H06", "H07", "H08", "H09", "H10", "H13", "H16", "H19A", "H19B", "H19C", "PROP", "INDHAC"]].copy()
comuna2_hogar
# %%
hogar_agua_c2 = comuna2_hogar.groupby(['H08']).count()
hogar_agua_c2
# %%
porcentaje_agua_c2 = hogar_agua_c2.transform(
    (lambda x: (x + 0.0) / 136894 * 100), axis=1
)
porcentaje_agua_c2
# %%
hogar_bagno_c2 = comuna2_hogar.groupby(['H10']).count()
hogar_bagno_c2
# %%
porcentaje_bagno_c2 = hogar_bagno_c2.transform(
    (lambda x: (x + 0.0) / 136894 * 100), axis=1
)
porcentaje_bagno_c2
# %%
hogar_bagno_ex_c2 = comuna2_hogar.groupby(['H13']).count()
hogar_bagno_ex_c2
# %%
porcentaje_bagno_ex_c2 = hogar_bagno_ex_c2.transform(
    (lambda x: (x + 0.0) / 136894 * 100), axis=1
)
porcentaje_bagno_ex_c2
# %%
hogar_prop_c2 = comuna2_hogar.groupby(['PROP']).count()
hogar_prop_c2
# %%
porcentaje_hogar_prop_c2 = hogar_prop_c2.transform(
    (lambda x: (x + 0.0) / 136894 * 100), axis=1
)
porcentaje_hogar_prop_c2
# %%
hogar_hac_c2 = comuna2_hogar.groupby(['INDHAC']).count()
hogar_hac_c2
# %%
porcentaje_hogar_hac_c2 = hogar_hac_c2.transform(
    (lambda x: (x + 0.0) / 136894 * 100), axis=1
)
porcentaje_hogar_hac_c2
# %%
#COMUNA 3
is_comuna3 = votantes.loc[:,"COMUNA"] == 3
comuna3 = votantes[is_comuna3]
comuna3
# %%
#POBLACION COMUNA 3
comuna3_poblacion = comuna3[["COMUNA", "P03", "P05", "P07", "P08", "P09", "CONDACT"]].copy()
comuna3_poblacion
# %%
edad_c3 = comuna3_poblacion["P03"].describe()
edad_c3
# %%
moda_educacion_c3 = comuna3_poblacion["P09"].mode()
moda_educacion_c3
# %%
educacion_c3 = comuna3_poblacion.groupby(['P09']).count()
educacion_c3
# %%
porcentaje_educacion_c3 = educacion_c3.transform(
    (lambda x: (x + 0.0) / 153918 * 100), axis=1
)
porcentaje_educacion_c3
# %%
poblacion_actividad_c3 = comuna3_poblacion.groupby(['CONDACT']).count()
poblacion_actividad_c3
# %%
porcentaje_actividad_c3 = poblacion_actividad_c3.transform(
    (lambda x: (x + 0.0) / 153918 * 100), axis=1
)
porcentaje_actividad_c3
# %%
#VIVIENDA COMUNA 3
comuna3_vivienda = comuna3[["COMUNA", "TIPVV", "V01", "INMAT", "INCALSERV", "INCALCONS"]].copy()
comuna3_vivienda
# %%
cant_tipo_vivienda_c3 = comuna3_vivienda.groupby(['V01']).count()
cant_tipo_vivienda_c3
# %%
porcentaje_tipo_vivienda_c3 = cant_tipo_vivienda_c3.transform(
    (lambda x: (x + 0.0) / 153918 * 100), axis=1
)
porcentaje_tipo_vivienda_c3
# %%
calidad_materiales_c3 = comuna3_vivienda.groupby(['INMAT']).count()
calidad_materiales_c3
# %%
porcentaje_calidad_materiales_c3 = calidad_materiales_c3.transform(
    (lambda x: (x + 0.0) / 153918 * 100), axis=1
)
porcentaje_calidad_materiales_c3
# %%
calidad_serv_c3 = comuna3_vivienda.groupby(['INCALSERV']).count()
calidad_serv_c3
# %%
porcentaje_calidad_serv_c3 = calidad_serv_c3.transform(
    (lambda x: (x + 0.0) / 153918 * 100), axis=1
)
porcentaje_calidad_serv_c3
# %%
calidad_cons_c3 = comuna3_vivienda.groupby(['INCALCONS']).count()
calidad_cons_c3
# %%
porcentaje_calidad_cons_c3 = calidad_cons_c3.transform(
    (lambda x: (x + 0.0) / 153918 * 100), axis=1
)
porcentaje_calidad_cons_c3
# %%
#HOGAR COMUNA 3
comuna3_hogar = comuna3[["COMUNA", "H05", "H06", "H07", "H08", "H09", "H10", "H13", "H16", "H19A", "H19B", "H19C", "PROP", "INDHAC"]].copy()
comuna3_hogar
# %%
hogar_agua_c3 = comuna3_hogar.groupby(['H08']).count()
hogar_agua_c3
# %%
porcentaje_agua_c3 = hogar_agua_c3.transform(
    (lambda x: (x + 0.0) / 153918 * 100), axis=1
)
porcentaje_agua_c3
# %%
hogar_bagno_c3 = comuna3_hogar.groupby(['H10']).count()
hogar_bagno_c3
# %%
porcentaje_bagno_c3 = hogar_bagno_c3.transform(
    (lambda x: (x + 0.0) / 153918 * 100), axis=1
)
porcentaje_bagno_c3
# %%
hogar_bagno_ex_c3 = comuna3_hogar.groupby(['H13']).count()
hogar_bagno_ex_c3
# %%
porcentaje_bagno_ex_c3 = hogar_bagno_ex_c3.transform(
    (lambda x: (x + 0.0) / 153918 * 100), axis=1
)
porcentaje_bagno_ex_c3
# %%
hogar_prop_c3 = comuna3_hogar.groupby(['PROP']).count()
hogar_prop_c3
# %%
porcentaje_hogar_prop_c3 = hogar_prop_c3.transform(
    (lambda x: (x + 0.0) / 153918 * 100), axis=1
)
porcentaje_hogar_prop_c3
# %%
hogar_hac_c3 = comuna3_hogar.groupby(['INDHAC']).count()
hogar_hac_c3
# %%
porcentaje_hogar_hac_c3 = hogar_hac_c3.transform(
    (lambda x: (x + 0.0) / 153918 * 100), axis=1
)
porcentaje_hogar_hac_c3
# %%
