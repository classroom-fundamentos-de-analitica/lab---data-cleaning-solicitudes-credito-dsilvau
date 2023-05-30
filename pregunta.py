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
    df = pd.read_csv("solicitudes_credito.csv", sep=";", index_col=0)

    df.dropna(axis=0, inplace=True)
    df.drop_duplicates(inplace=True)

    columns_to_lower = ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'línea_credito', 'barrio']
    columns_to_replace = ['idea_negocio', 'barrio']

    for column in columns_to_lower:
        df[column] = df[column].str.lower()
        df[column] = df[column].apply(lambda x: x.replace('_', ' '))
        df[column] = df[column].apply(lambda x: x.replace('-', ' '))

    for column in columns_to_replace:
        df[column] = df[column].str.replace('-', '').str.replace('_', '').str.replace(' ', '').str.replace('.', '')

    df['monto_del_credito'] = df['monto_del_credito'].str.replace(r'\$|,|\..*$', '').astype(int)
    df['comuna_ciudadano'] = df['comuna_ciudadano'].astype(float)

    date_format = "%Y/%m/%d" if len(re.findall("^\d+/", df['fecha_de_beneficio'].iloc[0])[0]) - 1 == 4 else "%d/%m/%Y"
    df['fecha_de_beneficio'] = pd.to_datetime(df['fecha_de_beneficio'], format=date_format)

    df.drop_duplicates(inplace=True)
    return df

