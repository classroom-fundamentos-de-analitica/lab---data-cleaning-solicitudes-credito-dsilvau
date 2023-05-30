"""
Limpieza de datos usando Pandas
-----------------------------------------------------------------------------------------

Realice la limpieza del dataframe. Los tests evaluan si la limpieza fue realizada 
correctamente. Tenga en cuenta datos faltantes y duplicados.

"""
import pandas as pd
from datetime import datetime
import re

def clean_data():
    df = pd.read_csv("solicitudes_credito.csv", sep=";")

    df.sexo = df.sexo.str.lower()

    df.tipo_de_emprendimiento = df.tipo_de_emprendimiento.str.lower()

    df.idea_negocio = df.idea_negocio.str.lower()
    df.idea_negocio = df.idea_negocio.apply(lambda x : x.replace('-',' '))
    df.idea_negocio = df.idea_negocio.apply(lambda x : x.replace('_',' '))

    df.barrio = df.barrio.astype(str)
    df.barrio = df.barrio.str.lower()
    df.barrio = df.barrio.apply(lambda x : x.replace('-', ''))
    df.barrio = df.barrio.apply(lambda x : x.replace('_', ''))
    df.barrio = df.barrio.apply(lambda x : x.replace(' ', ''))
    df.barrio = df.barrio.apply(lambda x : x.replace('.', ''))

    df.estrato = df.estrato.astype(int)

    df.comuna_ciudadano = df.comuna_ciudadano.astype(int)

    df.monto_del_credito = df.monto_del_credito.apply(lambda x : x.replace('$',''))
    df.monto_del_credito = df.monto_del_credito.apply(lambda x : x.replace(',',''))
    df.monto_del_credito = df.monto_del_credito.apply(lambda x : x.replace('.00',''))
    df.monto_del_credito = df.monto_del_credito.astype(int)

    df.fecha_de_beneficio = df.fecha_de_beneficio.apply(lambda x : x.replace('/', '-'))
    df.fecha_de_beneficio = pd.to_datetime(df.fecha_de_beneficio,
                                       infer_datetime_format=True)

    df.línea_credito = df.línea_credito.str.lower()
    df.línea_credito = df.línea_credito.apply(lambda x : x.replace('_', ''))
    df.línea_credito = df.línea_credito.apply(lambda x : x.replace('-', ''))
    df.línea_credito = df.línea_credito.apply(lambda x : x.replace(' ', ''))
    df.línea_credito = df.línea_credito.apply(lambda x : x.replace('.', ''))

    # Final setup

    df = df[df.barrio != "nan"]

    df = df[df["barrio"].str.contains("¿") == False]
    df.drop(columns=["Unnamed: 0"], inplace=True)

    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    df = pd.read_csv("solicitudes_credito.csv", sep=";", index_col = 0)
    
    df.dropna(axis = 0, inplace = True)
    df.drop_duplicates(inplace = True)

    for columna in ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'línea_credito', 'barrio']:
        df[columna] = df[columna].str.lower()
        df[columna] = df[columna].apply(lambda x: x.replace('_', ' '))
        df[columna] = df[columna].apply(lambda x: x.replace('-', ' '))

    df['monto_del_credito'] = df['monto_del_credito'].str.replace("\$[\s*]", "")
    df['monto_del_credito'] = df['monto_del_credito'].str.replace(",", "")
    df['monto_del_credito'] = df['monto_del_credito'].str.replace("\.00", "")
    df['monto_del_credito'] = df['monto_del_credito'].astype(int)
    
    df['comuna_ciudadano'] = df['comuna_ciudadano'].astype(float)

    df['fecha_de_beneficio'] = df['fecha_de_beneficio'].apply(lambda x: datetime.strptime(x, "%Y/%m/%d") if (len(re.findall("^\d+/", x)[0]) - 1) == 4 else datetime.strptime(x, "%d/%m/%Y"))

    df.drop_duplicates(inplace = True)
    return df
