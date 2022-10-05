## %

import numpy as np
import pandas as pd

df1 = pd.read_csv(
    "emisiones2016.csv",     # file path
    delimiter=';',       # delimitador ',',';','|','\t'
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
    #encoding=None,      # archivos con tilde y ñ por lo general utilizan "utf-8" etc 
)
#print(df1)

df2 = pd.read_csv(
    "emisiones2017.csv",     # file path
    delimiter=';',       # delimitador ',',';','|','\t'
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
    #encoding=None,      # archivos con tilde y ñ por lo general utilizan "utf-8" etc 
)
#print(df2)

df3 = pd.read_csv(
    "emisiones2018.csv",     # file path
    delimiter=';',       # delimitador ',',';','|','\t'
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
    #encoding=None,      # archivos con tilde y ñ por lo general utilizan "utf-8" etc 
)
#print(df3)

df4 = pd.read_csv(
    "emisiones2019.csv",     # file path
    delimiter=';',       # delimitador ',',';','|','\t'
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
    #encoding=None,      # archivos con tilde y ñ por lo general utilizan "utf-8" etc 
)
#print(df4)


emisiones = pd.concat([df1, df2, df3,df4])
#print(emisiones)

#columnas = ["ESTACION", "MAGNITUD", "ANO", "MES"]
#print(emisiones[columnas])

emisiones = emisiones.melt(id_vars=["ESTACION", "MAGNITUD", "ANO", "MES", "MUNICIPIO", "PUNTO_MUESTREO"], var_name="DIA", value_name="VALOR")
#print(emisiones)

emisiones["DIA"] = emisiones.DIA.str.strip("D")
emisiones['FECHA'] = emisiones.ANO.apply(str) + '/' + emisiones.MES.apply(str) + '/' + emisiones.DIA.apply(str)
emisiones['FECHA'] = pd.to_datetime(emisiones.FECHA, format='%Y/%m/%d', infer_datetime_format=True, errors='coerce')
#print(emisiones)
emisiones = emisiones.drop(emisiones[np.isnat(emisiones.FECHA)].index)
emisiones.sort_values(['ESTACION', 'MAGNITUD', 'FECHA'])
#print(emisiones)
#print('Estaciones:', emisiones.ESTACION.unique())
#print('Contaminantes:', emisiones.MAGNITUD.unique())

import datetime as dt
from datetime import date, time, datetime 


#def evolucion(estacion, contaminante, desde, hasta):
#    return emisiones[(emisiones.ESTACION == estacion) & (emisiones.MAGNITUD == contaminante) & (emisiones.FECHA >= desde) & (emisiones.FECHA <= hasta)].sort_values('FECHA').VALOR
#print(evolucion(56, 8, dt.datetime.strptime('2018/10/25', '%Y/%m/%d'), dt.datetime.strptime('2019/02/12', '%Y/%m/%d')))

#contaminantes = emisiones.groupby("MAGNITUD").agg(["min","max","mean","std"])
#print(contaminantes)

#contaminantes1 = emisiones.groupby('MAGNITUD').VALOR.describe()
#print(contaminantes1)

#contaminante_distrito = emisiones.groupby(['ESTACION', 'MAGNITUD']).VALOR.describe()
#print(contaminante_distrito)

# Función que devuelve un resumen descriptivo de la emisiones en un contaminante dado en un estación dada
#def resumen(estacion, contaminante):
#    return emisiones[(emisiones.ESTACION == estacion) & (emisiones.MAGNITUD == contaminante)].VALOR.describe()
# Resumen de Dióxido de Nitrógeno en Plaza Elíptica
#print('Resumen Dióxido de Nitrógeno en Plaza Elíptica:\n', resumen(56, 8),'\n', sep='')
# Resumen de Dióxido de Nitrógeno en Plaza del Carmen
#print('Resumen Dióxido de Nitrógeno en Plaza del Carmen:\n', resumen(35, 8), sep='')

# Función que devuelve una serie con las emisiones medias mensuales de un contaminante y un mes año para todos las estaciones
#def evolucion_mensual(contaminante, año):
#    return emisiones[(emisiones.MAGNITUD == contaminante) & (emisiones.ANO == año)].groupby(['ESTACION', 'MES']).VALOR.mean().unstack('MES')
# Evolución del dióxido de nitrógeno en 2019
#print(evolucion_mensual(8, 2019))

