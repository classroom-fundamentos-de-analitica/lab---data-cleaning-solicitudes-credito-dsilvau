import pandas as pd
from datetime import datetime
import re

def clean_data():
    data = pd.read_csv("solicitudes_credito.csv", sep=";")

    data.sexo = data.sexo.str.lower()

    data.tipo_de_emprendimiento = data.tipo_de_emprendimiento.str.lower()

    data.idea_negocio = data.idea_negocio.str.lower()
    data.idea_negocio = data.idea_negocio.apply(lambda x : x.replace('-',' '))
    data.idea_negocio = data.idea_negocio.apply(lambda x : x.replace('_',' '))

    data.barrio = data.barrio.astype(str)
    data.barrio = data.barrio.str.lower()
    data.barrio = data.barrio.apply(lambda x : x.replace('-', ''))
    data.barrio = data.barrio.apply(lambda x : x.replace('_', ''))
    data.barrio = data.barrio.apply(lambda x : x.replace(' ', ''))
    data.barrio = data.barrio.apply(lambda x : x.replace('.', ''))

    data.estrato = data.estrato.astype(int)

    data.comuna_ciudadano = data.comuna_ciudadano.astype(int)

    data.monto_del_credito = data.monto_del_credito.apply(lambda x : x.replace('$',''))
    data.monto_del_credito = data.monto_del_credito.apply(lambda x : x.replace(',',''))
    data.monto_del_credito = data.monto_del_credito.apply(lambda x : x.replace('.00',''))
    data.monto_del_credito = data.monto_del_credito.astype(int)

    data.fecha_de_beneficio = data.fecha_de_beneficio.apply(lambda x : x.replace('/', '-'))
    data.fecha_de_beneficio = pd.to_datetime(data.fecha_de_beneficio,
                                       infer_datetime_format=True)

    data.línea_credito = data.línea_credito.str.lower()
    data.línea_credito = data.línea_credito.apply(lambda x : x.replace('_', ''))
    data.línea_credito = data.línea_credito.apply(lambda x : x.replace('-', ''))
    data.línea_credito = data.línea_credito.apply(lambda x : x.replace(' ', ''))
    data.línea_credito = data.línea_credito.apply(lambda x : x.replace('.', ''))

    # Final setup

    data = data[data.barrio != "nan"]

    data = data[data["barrio"].str.contains("¿") == False]
    data.drop(columns=["Unnamed: 0"], inplace=True)

    data.dropna(inplace=True)
    data.drop_duplicates(inplace=True)

    #print(data.sexo.value_counts().to_list())
    #print(data.tipo_de_emprendimiento.value_counts().to_list())
    #print(data.línea_credito.value_counts().to_list())
    # data = data[data.barrio == "guayabal"]
    # print(data.línea_credito.value_counts())

    data = pd.read_csv("solicitudes_credito.csv", sep=";", index_col=0)
    
    data.dropna(axis=0, inplace=True)
    data.drop_duplicates(inplace=True)

    for columna in ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'línea_credito', 'barrio']:
        data[columna] = data[columna].str.lower()
        data[columna] = data[columna].apply(lambda x: x.replace('_', ' '))
        data[columna] = data[columna].apply(lambda x: x.replace('-', ' '))

    data['monto_del_credito'] = data['monto_del_credito'].str.replace("\$[\s*]", "")
    data['monto_del_credito'] = data['monto_del_credito'].str.replace(",", "")
    data['monto_del_credito'] = data['monto_del_credito'].str.replace("\.00", "")
    data['monto_del_credito'] = data['monto_del_credito'].astype(int)
    
    data['comuna_ciudadano'] = data['comuna_ciudadano'].astype(float)

    data['fecha_de_beneficio'] = data['fecha_de_beneficio'].apply(lambda x: datetime.strptime(x, "%Y/%m/%d") if (len(re.findall("^\d+/", x)[0]) - 1) == 4 else datetime.strptime(x, "%d/%m/%Y"))

    data.drop_duplicates(inplace=True)
    return data
