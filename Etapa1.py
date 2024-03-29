# %%
from itertools import count
from statistics import geometric_mean
import pandas as pd
import numpy as np
import geopandas as gpd

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
votos_x_circuito_comuna = tabla_final.groupby(["COMUNA", "circuito"]).sum()
votos_x_circuito_comuna
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
    tabla_final[["COMUNA", "circuito","pp1", "pp2", "pp3", "pp4", "nv", "BARRIO"]]
    .groupby(["COMUNA", "circuito"])
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
#COMUNA 4
is_comuna4 = votantes.loc[:,"COMUNA"] == 4
comuna4 = votantes[is_comuna4]
comuna4
# %%
#POBLACION COMUNA 4
comuna4_poblacion = comuna4[["COMUNA", "P03", "P05", "P07", "P08", "P09", "CONDACT"]].copy()
comuna4_poblacion
# %%
edad_c4 = comuna4_poblacion["P03"].describe()
edad_c4
# %%
moda_educacion_c4 = comuna4_poblacion["P09"].mode()
moda_educacion_c4
# %%
educacion_c4 = comuna4_poblacion.groupby(['P09']).count()
educacion_c4
# %%
porcentaje_educacion_c4 = educacion_c4.transform(
    (lambda x: (x + 0.0) / 163460 * 100), axis=1
)
porcentaje_educacion_c4
# %%
poblacion_actividad_c4 = comuna4_poblacion.groupby(['CONDACT']).count()
poblacion_actividad_c4
# %%
porcentaje_actividad_c4 = poblacion_actividad_c4.transform(
    (lambda x: (x + 0.0) / 163460 * 100), axis=1
)
porcentaje_actividad_c4
# %%
comuna4_vivienda = comuna4[["COMUNA", "TIPVV", "V01", "INMAT", "INCALSERV", "INCALCONS"]].copy()
comuna4_vivienda
# %%
#VIVIENDA COMUNA 4
cant_tipo_vivienda_c4 = comuna4_vivienda.groupby(['V01']).count()
cant_tipo_vivienda_c4
# %%
porcentaje_tipo_vivienda_c4 = cant_tipo_vivienda_c4.transform(
    (lambda x: (x + 0.0) / 163460 * 100), axis=1
)
porcentaje_tipo_vivienda_c4
# %%
calidad_materiales_c4 = comuna4_vivienda.groupby(['INMAT']).count()
calidad_materiales_c4
# %%
porcentaje_calidad_materiales_c4 = calidad_materiales_c4.transform(
    (lambda x: (x + 0.0) / 163460 * 100), axis=1
)
porcentaje_calidad_materiales_c4
# %%
calidad_serv_c4 = comuna4_vivienda.groupby(['INCALSERV']).count()
calidad_serv_c4
# %%
porcentaje_calidad_serv_c4 = calidad_serv_c4.transform(
    (lambda x: (x + 0.0) / 163460 * 100), axis=1
)
porcentaje_calidad_serv_c4
# %%
calidad_cons_c4 = comuna4_vivienda.groupby(['INCALCONS']).count()
calidad_cons_c4
# %%
porcentaje_calidad_cons_c4 = calidad_cons_c4.transform(
    (lambda x: (x + 0.0) / 163460 * 100), axis=1
)
porcentaje_calidad_cons_c4
# %%
#HOGAR COMUNA 4
comuna4_hogar = comuna4[["COMUNA", "H05", "H06", "H07", "H08", "H09", "H10", "H13", "H16", "H19A", "H19B", "H19C", "PROP", "INDHAC"]].copy()
comuna4_hogar
# %%
hogar_agua_c4 = comuna4_hogar.groupby(['H08']).count()
hogar_agua_c4
# %%
porcentaje_agua_c4 = hogar_agua_c4.transform(
    (lambda x: (x + 0.0) / 163460 * 100), axis=1
)
porcentaje_agua_c4
# %%
hogar_bagno_c4 = comuna4_hogar.groupby(['H10']).count()
hogar_bagno_c4
# %%
porcentaje_bagno_c4 = hogar_bagno_c4.transform(
    (lambda x: (x + 0.0) / 163460 * 100), axis=1
)
porcentaje_bagno_c4
# %%
hogar_bagno_ex_c4 = comuna4_hogar.groupby(['H13']).count()
hogar_bagno_ex_c4
# %%
porcentaje_bagno_ex_c4 = hogar_bagno_ex_c4.transform(
    (lambda x: (x + 0.0) / 163460 * 100), axis=1
)
porcentaje_bagno_ex_c4
# %%
hogar_prop_c4 = comuna4_hogar.groupby(['PROP']).count()
hogar_prop_c4
# %%
porcentaje_hogar_prop_c4 = hogar_prop_c4.transform(
    (lambda x: (x + 0.0) / 163460 * 100), axis=1
)
porcentaje_hogar_prop_c4
# %%
hogar_hac_c4 = comuna4_hogar.groupby(['INDHAC']).count()
hogar_hac_c4
# %%
porcentaje_hogar_hac_c4 = hogar_hac_c4.transform(
    (lambda x: (x + 0.0) / 163460 * 100), axis=1
)
porcentaje_hogar_hac_c4
# %%
#COMUNA 5
is_comuna5 = votantes.loc[:,"COMUNA"] == 5
comuna5 = votantes[is_comuna5]
comuna5
# %%
#POBLACION COMUNA 5
comuna5_poblacion = comuna5[["COMUNA", "P03", "P05", "P07", "P08", "P09", "CONDACT"]].copy()
comuna5_poblacion
# %%
edad_c5 = comuna5_poblacion["P03"].describe()
edad_c5
# %%
moda_educacion_c5 = comuna5_poblacion["P09"].mode()
moda_educacion_c5
# %%
educacion_c5 = comuna5_poblacion.groupby(['P09']).count()
educacion_c5
# %%
porcentaje_educacion_c5 = educacion_c5.transform(
    (lambda x: (x + 0.0) / 147885 * 100), axis=1
)
porcentaje_educacion_c5
# %%
poblacion_actividad_c5 = comuna5_poblacion.groupby(['CONDACT']).count()
poblacion_actividad_c5
# %%
porcentaje_actividad_c5 = poblacion_actividad_c5.transform(
    (lambda x: (x + 0.0) / 147885 * 100), axis=1
)
porcentaje_actividad_c5
# %%
#VIVIENDA COMUNA 5
comuna5_vivienda = comuna5[["COMUNA", "TIPVV", "V01", "INMAT", "INCALSERV", "INCALCONS"]].copy()
comuna5_vivienda
# %%
cant_tipo_vivienda_c5 = comuna5_vivienda.groupby(['V01']).count()
cant_tipo_vivienda_c5
# %%
porcentaje_tipo_vivienda_c5 = cant_tipo_vivienda_c5.transform(
    (lambda x: (x + 0.0) / 147885 * 100), axis=1
)
porcentaje_tipo_vivienda_c5
# %%
calidad_materiales_c5 = comuna5_vivienda.groupby(['INMAT']).count()
calidad_materiales_c5
# %%
porcentaje_calidad_materiales_c5 = calidad_materiales_c5.transform(
    (lambda x: (x + 0.0) / 147885 * 100), axis=1
)
porcentaje_calidad_materiales_c5
# %%
calidad_serv_c5 = comuna5_vivienda.groupby(['INCALSERV']).count()
calidad_serv_c5
# %%
porcentaje_calidad_serv_c5 = calidad_serv_c5.transform(
    (lambda x: (x + 0.0) / 147885 * 100), axis=1
)
porcentaje_calidad_serv_c5
# %%
calidad_cons_c5 = comuna5_vivienda.groupby(['INCALCONS']).count()
calidad_cons_c5
# %%
porcentaje_calidad_cons_c5 = calidad_cons_c5.transform(
    (lambda x: (x + 0.0) / 147885 * 100), axis=1
)
porcentaje_calidad_cons_c5
# %%
#HOGAR COMUNA 5
comuna5_hogar = comuna5[["COMUNA", "H05", "H06", "H07", "H08", "H09", "H10", "H13", "H16", "H19A", "H19B", "H19C", "PROP", "INDHAC"]].copy()
comuna5_hogar
# %%
hogar_agua_c5 = comuna5_hogar.groupby(['H08']).count()
hogar_agua_c5
# %%
porcentaje_agua_c5 = hogar_agua_c5.transform(
    (lambda x: (x + 0.0) / 147885 * 100), axis=1
)
porcentaje_agua_c5
# %%
hogar_bagno_c5 = comuna5_hogar.groupby(['H10']).count()
hogar_bagno_c5
# %%
porcentaje_bagno_c5 = hogar_bagno_c5.transform(
    (lambda x: (x + 0.0) / 147885 * 100), axis=1
)
porcentaje_bagno_c5
# %%
hogar_bagno_ex_c5 = comuna5_hogar.groupby(['H13']).count()
hogar_bagno_ex_c5
# %%
porcentaje_bagno_ex_c5 = hogar_bagno_ex_c5.transform(
    (lambda x: (x + 0.0) / 147885 * 100), axis=1
)
porcentaje_bagno_ex_c5
# %%
hogar_prop_c5 = comuna5_hogar.groupby(['PROP']).count()
hogar_prop_c5
# %%
porcentaje_hogar_prop_c5 = hogar_prop_c5.transform(
    (lambda x: (x + 0.0) / 147885 * 100), axis=1
)
porcentaje_hogar_prop_c5
# %%
hogar_hac_c5 = comuna5_hogar.groupby(['INDHAC']).count()
hogar_hac_c5
# %%
porcentaje_hogar_hac_c5 = hogar_hac_c5.transform(
    (lambda x: (x + 0.0) / 147885 * 100), axis=1
)
porcentaje_hogar_hac_c5
# %%
#COMUNA 6
is_comuna6 = votantes.loc[:,"COMUNA"] == 6
comuna6 = votantes[is_comuna6]
comuna6
# %%
#POBLACION COMUNA 6
comuna6_poblacion = comuna6[["COMUNA", "P03", "P05", "P07", "P08", "P09", "CONDACT"]].copy()
comuna6_poblacion
# %%
edad_c6 = comuna6_poblacion["P03"].describe()
edad_c6
# %%
moda_educacion_c6 = comuna6_poblacion["P09"].mode()
moda_educacion_c6
# %%
educacion_c6 = comuna6_poblacion.groupby(['P09']).count()
educacion_c6
# %%
porcentaje_educacion_c6 = educacion_c6.transform(
    (lambda x: (x + 0.0) / 146155  * 100), axis=1
)
porcentaje_educacion_c6
# %%
poblacion_actividad_c6 = comuna6_poblacion.groupby(['CONDACT']).count()
poblacion_actividad_c6
# %%
porcentaje_actividad_c6 = poblacion_actividad_c6.transform(
    (lambda x: (x + 0.0) / 146155 * 100), axis=1
)
porcentaje_actividad_c6
# %%
#VIVIENDA COMUNA 6
comuna6_vivienda = comuna6[["COMUNA", "TIPVV", "V01", "INMAT", "INCALSERV", "INCALCONS"]].copy()
comuna6_vivienda
# %%
cant_tipo_vivienda_c6 = comuna6_vivienda.groupby(['V01']).count()
cant_tipo_vivienda_c6
# %%
porcentaje_tipo_vivienda_c6 = cant_tipo_vivienda_c6.transform(
    (lambda x: (x + 0.0) / 146155 * 100), axis=1
)
porcentaje_tipo_vivienda_c6
# %%
calidad_materiales_c6 = comuna6_vivienda.groupby(['INMAT']).count()
calidad_materiales_c6
# %%
porcentaje_calidad_materiales_c6 = calidad_materiales_c6.transform(
    (lambda x: (x + 0.0) / 146155 * 100), axis=1
)
porcentaje_calidad_materiales_c6
# %%
calidad_serv_c6 = comuna6_vivienda.groupby(['INCALSERV']).count()
calidad_serv_c6
# %%
porcentaje_calidad_serv_c6 = calidad_serv_c6.transform(
    (lambda x: (x + 0.0) / 146155 * 100), axis=1
)
porcentaje_calidad_serv_c6
# %%
calidad_cons_c6 = comuna6_vivienda.groupby(['INCALCONS']).count()
calidad_cons_c6
# %%
porcentaje_calidad_cons_c6 = calidad_cons_c6.transform(
    (lambda x: (x + 0.0) / 146155 * 100), axis=1
)
porcentaje_calidad_cons_c6
# %%
#HOGAR COMUNA 6
comuna6_hogar = comuna6[["COMUNA", "H05", "H06", "H07", "H08", "H09", "H10", "H13", "H16", "H19A", "H19B", "H19C", "PROP", "INDHAC"]].copy()
comuna6_hogar
# %%
hogar_agua_c6 = comuna6_hogar.groupby(['H08']).count()
hogar_agua_c6
# %%
porcentaje_agua_c6 = hogar_agua_c5.transform(
    (lambda x: (x + 0.0) / 146155 * 100), axis=1
)
porcentaje_agua_c6
# %%
hogar_bagno_c6 = comuna6_hogar.groupby(['H10']).count()
hogar_bagno_c6
# %%
porcentaje_bagno_c6 = hogar_bagno_c6.transform(
    (lambda x: (x + 0.0) / 146155 * 100), axis=1
)
porcentaje_bagno_c6
# %%
hogar_bagno_ex_c6 = comuna6_hogar.groupby(['H13']).count()
hogar_bagno_ex_c6

# %%

porcentaje_bagno_ex_c6 = hogar_bagno_ex_c6.transform(
    (lambda x: (x + 0.0) / 146155 * 100), axis=1
)
porcentaje_bagno_ex_c6
# %%
hogar_prop_c6 = comuna6_hogar.groupby(['PROP']).count()
hogar_prop_c6
# %%
porcentaje_hogar_prop_c6 = hogar_prop_c6.transform(
    (lambda x: (x + 0.0) / 146155 * 100), axis=1
)
porcentaje_hogar_prop_c6
# %%
hogar_hac_c6 = comuna6_hogar.groupby(['INDHAC']).count()
hogar_hac_c6
# %%
porcentaje_hogar_hac_c6 = hogar_hac_c6.transform(
    (lambda x: (x + 0.0) / 146155 * 100), axis=1
)
porcentaje_hogar_hac_c6

# %%
#COMUNA 7
is_comuna7 = votantes.loc[:,"COMUNA"] == 7
comuna7 = votantes[is_comuna7]
comuna7


# %%
#POBLACION COMUNA 7
comuna7_poblacion = comuna7[["COMUNA", "P03", "P05", "P07", "P08", "P09", "CONDACT"]].copy()
comuna7_poblacion
# %%
edad_c7 = comuna7_poblacion["P03"].describe()
edad_c7
# %%
moda_educacion_c7 = comuna7_poblacion["P09"].mode()
moda_educacion_c7
# %%
educacion_c7 = comuna7_poblacion.groupby(['P09']).count()
educacion_c7
# %%
porcentaje_educacion_c7 = educacion_c7.transform(
    (lambda x: (x + 0.0) / 171435  * 100), axis=1
)
porcentaje_educacion_c7
#=======
#>>>>>>> 3a673cef7eebaa4096e50edb4fe0473f5689813f
# %%
#GEOPANDAS
censo = gpd.read_file("/Users/camilaherrero/Desktop/Candidato 3",
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
print(censo)
# %%
import matplotlib.pyplot as plt
# %%
porcentaje_votos_x_comunas.reset_index(inplace = True)
#%%

censo["circuito"]=censo["circuito"].apply(int)
censo

# %%
censovotos= pd.merge(censo,porcentaje_votos_x_comunas, on="circuito", how="inner")
censovotos=censovotos.sort_values("circuito")
censovotos.reset_index(inplace=True)
censovotos
# %%
censovotos= pd.merge(censo,porcentaje_votos_x_comunas, on="circuito", how="inner")
censovotos=censovotos.sort_values("circuito")
censovotos.reset_index(inplace=True)
censovotos
# %%
censovotos.plot(column='pp3', scheme= "quantiles", figsize=(10, 10)) 
# %%
fig, ax = plt.subplots(figsize=(10, 10))
 
# Control del título y los ejes
ax.set_title('Porcentaje de votos del partido 3 por circuito electoral', 
             pad = 20, 
             fontdict={'fontsize':20, 'color': '#4873ab'})
ax.set_xlabel('Longitud')
ax.set_ylabel('Latitud')
 
# Mostrar el mapa finalizado
censovotos.plot(column='pp3', cmap='viridis',scheme='quantiles', ax=ax, zorder=5)
# %%
radios_shp = gpd.read_file("/Users/camilaherrero/Desktop/Candidato 3/CABA_radios.shx",
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
radios_shp
# %%
radios_shp.rename({"DPTO" : "COMUNA"}, axis = 1, inplace = True) #cambie el nombre de la columna dpto por comuna para poder hacer un merge con el df que veniamos trabajando
radios_shp

# %%
radios_shp["COMUNA"] = radios_shp.COMUNA.str.strip("Comuna") #para sacarle la leyenda "Comuna" a la fila de comunas y que quede solo el numero
radios_shp

# %%
radios_shp["COMUNA"] = radios_shp["COMUNA"].apply(int)
radios_shp

# %%
votantes["PROV"] = 2
votantes
# %%
votantes["COMUNA"] = votantes["COMUNA"].apply(str)
votantes["COMUNA"]
# %%
votantes["IDFRAC"] = votantes["IDFRAC"].apply(str)
# %%
votantes["IDRADIO"] = votantes["IDRADIO"].apply(str)

# %%
votantes["PROV"] = votantes["PROV"].apply(str)
# %%
votantes["COMUNA"] = votantes["COMUNA"].str.pad(3, side = "left", fillchar ='0')
votantes["COMUNA"]
# %%
votantes["IDFRAC"] = votantes["IDFRAC"].str.pad(2, side = "left", fillchar ='0')
votantes["IDFRAC"]
# %%
votantes["IDRADIO"] = votantes["IDRADIO"].str.pad(2, side = "left", fillchar ='0')
votantes["IDRADIO"]

# %%
votantes["PROV"] = votantes["PROV"].str.pad(2, side = "left", fillchar ='0')
votantes["PROV"]
# %%
votantes["RADIO"] = votantes.PROV.str.cat(votantes.COMUNA)
votantes
# %%
votantes["RADIO"] = votantes.RADIO.str.cat(votantes.IDFRAC)
votantes
# %%
votantes["RADIO"] = votantes.RADIO.str.cat(votantes.IDRADIO)
votantes
# %%
votantes_radio_agrup = votantes.groupby(["RADIO"]).sum()
votantes_radio_agrup
# %%
votantes_radio_agrup.reset_index(inplace= True)
votantes_radio_agrup

# %%
votantes_radio_shp = pd.merge(radios_shp,votantes_radio_agrup, on="RADIO", how="inner")
votantes_radio_shp
# %%
