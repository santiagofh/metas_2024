#%% Importaciones
import os
import pandas as pd
import json

#%% Definiciones de datos y denominadores
metas_sanitarias = {
    "MSI": {
        "numerador": {
            "cod": ["02010420", "03500366"],
            "col": ["Col08", "Col09", "Col10", "Col11"]
        },
        "denominador": {
            "cod": ["02010321", "03500334"],
            "col": ["Col08", "Col09", "Col10", "Col11"]
        }
    },
    "MSII": {
        "numerador": {
            "cod": [
                "P1206010", "P1206020", "P1206030", "P1206040", "P1206050", "P1206060",
                "P1206070", "P1206080", 
                # "P1240010", "P1240011", "P1240012", "P1240013","P1240014", "P1240015", "P1240016"
            ],
            "col": ["Col01", 
                    "Col02" #"Trans Masculino con Tamizaje Vigente para la Detección Precoz de Cáncer de Cuello Uterino"
                    ]
        },
        "denominador": {
            "sexo": ["Mujeres"],
            "edad": [list(range(25, 65))]
        }
    },
    "MSIIIa": {
        "numerador": {
            "cod": ["03500364", "03500365"],
            "col": [
                "Col04", "Col05", "Col06", "Col07", "Col08", "Col09", "Col10", "Col11",
                "Col12", "Col13", "Col14", "Col15", "Col16", "Col17", "Col18", "Col19",
                "Col20", "Col21", "Col22", "Col23"
            ]
        },
        "denominador": {
            "edad": [list(range(0, 10))]
        }
    },
    "MSIIIb": {
        "numerador": {
            "cod": ["09220100"],
            "col": ["Col16", "Col17"]
        },
        "denominador": {
            "edad": [list(range(0, 7))]
        }
    },
    "MSIVa": {
        "numerador": {
            "cod": ["P4180300", "P4200200"],
            "col": ["Col01"]
        },
        "denominador": {
            "edad": [
                list(range(15, 25)), list(range(25, 45)),
                list(range(45, 65)), list(range(65, 200))
            ],
            "prevalencia": [0.018, 0.063, 0.183, 0.306]
        }
    },

    "MSIVb": {
        "numerador": {
            "cod": ["P4190809", "P4170300", "P4190500", "P4190600"],
            "col": ["Col01"]
        },
        "denominador": {
            "cod": ["P4150602"],
            "col": ["Col01"]
        }
    },

    "MSV": {
        "numerador": {
            "cod": ["P4180200", "P4200100"],
            "col": ["Col01"]
        },
        "denominador": {
            "edad": [
                list(range(15, 25)), list(range(25, 45)),
                list(range(45, 65)), list(range(65, 200))
            ],
            "prevalencia": [
                0.007,
                0.106,
                0.451,
                0.733
            ]
        }
    },
    "MSVI": {
        "numerador": {
            "cod": ["A0200002"],
            "col": ["Col06"]
        },
        "denominador": {
            "cod": ["A0200001"],
            "col": ["Col06"]
        }
    },
    "MSVII": {
        "numerador": {
            "cod": ["P3161041","P3161045"],
            "col": ["Col01",
                    "Col06",
                    "Col07",
                    "Col08",
                    "Col09",
                    "Col10",
                    "Col11",
                    "Col12",
                    "Col13",
                    "Col14",
                    "Col15",
                    "Col16",
                    "Col17",
                    "Col18",
                    "Col19",
                    "Col20",
                    "Col21",
                    "Col22",
                    "Col23",
                    "Col24",
                    "Col25",
                    "Col26",
                    "Col27",
                    "Col28",
                    "Col29",
                    "Col30",
                    "Col31",
                    "Col32",
                    "Col33",
                    "Col34",
                    "Col35",
                    "Col36",
                    ]
        },
        "denominador": {
            "edad": [list(range(40, 120)), list(range(5, 40))],
            "prevalencia": [0.117, 
                            0.10]
        }
    }
}

#%% Recopilación de todos los códigos
all_codes = []
for meta in metas_sanitarias.values():
    all_codes.extend(meta['numerador']['cod'])
    if 'cod' in meta['denominador']:
        all_codes.extend(meta['denominador']['cod'])

print(all_codes)

#%% Lectura y filtrado de datos
directory = r"C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\Salud Pública\REM\REM_2024"
filtered_data = []

# Recorrer carpetas y subcarpetas
for root, dirs, files in os.walk(directory):
    for filename in files:
        if filename.endswith(".csv") or filename.endswith(".txt"):
            filepath = os.path.join(root, filename)
            for chunk in pd.read_csv(filepath, sep=";", chunksize=1000):
                filtered_chunk = chunk[chunk['CodigoPrestacion'].isin(all_codes)]
                filtered_data.append(filtered_chunk)

# Concatenar todos los datos filtrados
df_rem = pd.concat(filtered_data, ignore_index=True)
print(df_rem)

#%% Lectura de datos de FONASA
fonasa1 = pd.read_excel('FONASA/Copia de T6603_Inscritos.xlsx', sheet_name='Respuesta M', skiprows=4)
fonasa2 = pd.read_excel('FONASA/Copia de T6603_Inscritos.xlsx', sheet_name='Respuesta S', skiprows=4)
fonasa = pd.concat([fonasa1, fonasa2])
ss_rm = ['Metropolitano Central', 'Metropolitano Norte', 'Metropolitano Occidente', 'Metropolitano Oriente', 'Metropolitano Sur', 'Metropolitano Sur Oriente']
fonasa_rm = fonasa.loc[fonasa['Servicio de Salud'].isin(ss_rm)]

#%% Definición de funciones
def calcular_numerador(metas_sanitarias, df_rem, key, region_id, cols_df, cols_grup):
    df_numerador = df_rem.loc[df_rem.CodigoPrestacion.isin(metas_sanitarias[key]["numerador"]["cod"])]
    df_numerador_rm = df_numerador.loc[df_numerador.IdRegion == region_id]
    df_numerador_rm_cols = df_numerador_rm[cols_df + list(metas_sanitarias[key]["numerador"]["col"])].copy()
    df_numerador_rm_cols.fillna(0, inplace=True)
    df_numerador_est = df_numerador_rm_cols.groupby(by=cols_grup).sum().reset_index()
    df_numerador_est[f'Numerador_{key}'] = df_numerador_est[list(metas_sanitarias[key]["numerador"]["col"])].sum(axis=1)
    df_numerador_est = df_numerador_est[cols_grup + [f'Numerador_{key}']]
    return df_numerador_est

def calcular_denominador(metas_sanitarias, df_rem, key, region_id, cols_df, cols_grup):
    df_denominador = df_rem.loc[df_rem.CodigoPrestacion.isin(metas_sanitarias[key]["denominador"]["cod"])]
    df_denominador_rm = df_denominador.loc[df_denominador.IdRegion == region_id]
    df_denominador_rm_cols = df_denominador_rm[cols_df + list(metas_sanitarias[key]["denominador"]["col"])].copy()
    df_denominador_rm_cols.fillna(0, inplace=True)
    df_denominador_est = df_denominador_rm_cols.groupby(by=cols_grup).sum().reset_index()
    df_denominador_est[f'Denominador_{key}'] = df_denominador_est[list(metas_sanitarias[key]["denominador"]["col"])].sum(axis=1)
    df_denominador_est = df_denominador_est[cols_grup + [f'Denominador_{key}']]
    return df_denominador_est

def calcular_denominador_fonasa(fonasa_rm, metas_sanitarias, key):
    if "prevalencia" in metas_sanitarias[key]["denominador"]:
        df_filt_list = []
        for i in range(len(metas_sanitarias[key]["denominador"]["edad"])):
            df_filt = fonasa_rm.loc[fonasa_rm.Edad.isin(metas_sanitarias[key]["denominador"]["edad"][i])].copy()
            df_filt['Inscritos'] = df_filt['Inscritos'].multiply(metas_sanitarias[key]["denominador"]["prevalencia"][i]).copy()
            df_filt_list.append(df_filt)
        df_denominador = pd.concat(df_filt_list)
    else:
        df_denominador = fonasa_rm.loc[fonasa_rm.Edad.isin(metas_sanitarias[key]["denominador"]["edad"][0])].copy()
        if "sexo" in metas_sanitarias[key]["denominador"]:
            df_denominador = df_denominador.loc[fonasa_rm.Sexo.isin(metas_sanitarias[key]["denominador"]["sexo"])].copy()
    df_denominador=df_denominador.dropna(subset=['Inscritos'])
    df_group_denominador = df_denominador.groupby('Código Centro').sum().reset_index()
    df_group_denominador = df_group_denominador[['Código Centro', 'Inscritos']]
    df_group_denominador = df_group_denominador.rename(columns={'Código Centro': 'IdEstablecimiento'})
    df_group_denominador = df_group_denominador.rename(columns={'Inscritos': f'Denominador_{key}'})
    return df_group_denominador

#%% Definición de parámetros y procesamiento
cols_df = [  'IdEstablecimiento', 'Ano', 'Mes', 'CodigoPrestacion', 'IdRegion']
cols_grup = ['IdEstablecimiento', 'Ano', 'Mes']
cols_merge = ['IdEstablecimiento', 'Ano', 'Mes']
region_id = 13  # ID de la región para filtrar

resultado={}

#%% Definición de listas de MS
ms_denominador_rem = ['MSI', 'MSIVb', 'MSVI']
ms_denominador_fonasa= ['MSII', 'MSIIIb', 'MSIIIa', 'MSIVa', 'MSV', 'MSVII']

#%% Procesar metas sanitarias con 'cod' y 'col'
for key in ms_denominador_rem:
    print(key)
    df_numerador_est1 = calcular_numerador(metas_sanitarias, df_rem, key, region_id, cols_df, cols_grup)
    df_denominador_est1 = calcular_denominador(metas_sanitarias, df_rem, key, region_id, cols_df, cols_grup)
    df_resultado1=df_numerador_est1.merge(df_denominador_est1, on=cols_merge, how='outer')
    resultado[key]=df_resultado1
#%% Calcular denominadores FONASA y actualizar resultados para metas sanitarias con 'sexo' y 'edad'
denominadores_fonasa = {}
for key in ms_denominador_fonasa:
    print(key)
    df_numerador_est2 = calcular_numerador(metas_sanitarias, df_rem, key, region_id, cols_df, cols_grup)
    df_denominador_est2 = calcular_denominador_fonasa(fonasa_rm, metas_sanitarias, key)
    df_resultado2=df_numerador_est2.merge(df_denominador_est2, on='IdEstablecimiento', how='outer')
    resultado[key]=df_resultado2
#%%
#%% Convertir resultados a diccionario y guardar en JSON
resultados_dict = {}
for key, df in resultado.items():
    resultados_dict[key] = df[['IdEstablecimiento', 'Ano', 'Mes', f'Numerador_{key}', f'Denominador_{key}']].rename(
        columns={
            f'Numerador_{key}': 'Numerador',
            f'Denominador_{key}': 'Denominador'
        }
    ).to_dict(orient='records')

# Guardar en JSON
with open('MS2024.json', 'w', encoding='utf-8') as f:
    json.dump(resultados_dict, f, ensure_ascii=False, indent=4)

print("JSON guardado exitosamente.")
# %%

#%% Convertir resultados a un solo DataFrame y guardar en CSV
resultados_list = []
for key, df in resultado.items():
    df['MetaSanitaria'] = key
    df = df[['IdEstablecimiento', 'Ano', 'Mes', f'Numerador_{key}', f'Denominador_{key}', 'MetaSanitaria']].rename(
        columns={
            f'Numerador_{key}': 'Numerador',
            f'Denominador_{key}': 'Denominador'
        }
    )
    resultados_list.append(df)

df_final = pd.concat(resultados_list, ignore_index=True)
df_final.to_csv('MS2024.csv', index=False, encoding='utf-8')

print("Archivo CSV guardado exitosamente.")
# %%