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
            "edad": [[6]]
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
            "cod": ["P3161041"],
            "col": [
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
                    "Col37",
                    ],
            "cod2":["P3161045"],
            "col2":["Col01"]
        },
        "denominador": {
            "edad": [list(range(40, 120)), 
                     list(range(5, 40))],
            "prevalencia": [0.117, 
                            0.10]
        }
    }
}

#%% Recopilación de todos los códigos
all_codes = []
for meta in metas_sanitarias.values():
    all_codes.extend(meta['numerador']['cod'])
    if 'cod2' in meta['numerador']:
        all_codes.extend(meta['numerador']['cod2'])
    if 'cod' in meta['denominador']:
        all_codes.extend(meta['denominador']['cod'])
    if 'cod2' in meta['denominador']:
        all_codes.extend(meta['denominador']['cod2'])

print(all_codes)


#%% Lectura y filtrado de datos
directory_2024 = r"C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\REM\REM 2024\archivos_extraidos"
directory_2023 = r"C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\REM\REM 2023\archivos_extraidos"

filtered_data_2024 = []
filtered_data_2023 = []
# Recorrer carpetas y subcarpetas
for root, dirs, files in os.walk(directory_2024):
    for filename in files:
        if filename.endswith(".csv") or filename.endswith(".txt"):
            filepath = os.path.join(root, filename)
            for chunk in pd.read_csv(filepath, sep=";", chunksize=1000):
                filtered_chunk = chunk[chunk['CodigoPrestacion'].isin(all_codes)]
                filtered_data_2024.append(filtered_chunk)
# Recorrer carpetas y subcarpetas
for root, dirs, files in os.walk(directory_2023):
    for filename in files:
        if filename.endswith(".csv") or filename.endswith(".txt"):
            filepath = os.path.join(root, filename)
            for chunk in pd.read_csv(filepath, sep=";", chunksize=1000):
                filtered_chunk = chunk[chunk['CodigoPrestacion'].isin(all_codes)]
                filtered_data_2023.append(filtered_chunk)
# Concatenar todos los datos filtrados
df_rem_2024 = pd.concat(filtered_data_2024, ignore_index=True)
df_rem_2023 = pd.concat(filtered_data_2023, ignore_index=True) # META 1 = Octubre 2023 a Septiembre 2024

print(df_rem_2024)
#%%
# Datos DEIS
path_deis=r"C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\GIE\DEIS\Listado de establecimientos\Establecimientos DEIS MINSAL 07-01-2025 (2).xlsx"
df_deis=pd.read_excel(path_deis)
#%% Lectura de datos de FONASA
fonasa1 = pd.read_excel('FONASA/Copia de T6603_Inscritos.xlsx', sheet_name='Respuesta M', skiprows=4)
fonasa2 = pd.read_excel('FONASA/Copia de T6603_Inscritos.xlsx', sheet_name='Respuesta S', skiprows=4)
fonasa = pd.concat([fonasa1, fonasa2])
ss_rm = ['Metropolitano Central', 'Metropolitano Norte', 'Metropolitano Occidente', 'Metropolitano Oriente', 'Metropolitano Sur', 'Metropolitano Sur Oriente','Metropolitano Central']
fonasa_rm = fonasa.loc[fonasa['Servicio de Salud'].isin(ss_rm)]
#%%
# Trabajar
df_deis_concat = df_deis.rename(columns={
    'Código Vigente': 'IdEstablecimiento',
    'Código Dependencia Jerárquica (SEREMI / Servicio de Salud)': 'IdServicio',
    'Código Región': 'IdRegion',
    'IdComuna':'Código Comuna'
})
df_deis_concat['Año'] = 2024
df_deis_concat = df_deis_concat[['IdEstablecimiento', 'IdServicio', 'IdRegion', 'Año']]
df_unique = df_deis_concat.drop_duplicates(subset=['IdEstablecimiento', 'IdServicio', 'IdRegion'])
df_codes = pd.DataFrame({'CodigoPrestacion': all_codes})
df_deis_concat2 = df_unique.merge(df_codes, how='cross')
df_months = pd.DataFrame({'Mes': range(1, 13)})
df_deis_concat2 = df_deis_concat2.merge(df_months, how='cross')
df_deis_concat2_rm = df_deis_concat2[df_deis_concat2['IdRegion'] == 13]
#%%
# df_rem_2024=pd.concat([df_rem_2024,df_deis_concat2_rm])
# Mes	IdServicio	Ano	IdEstablecimiento	CodigoPrestacion	IdRegion

#%% Definición de funciones
def calcular_numerador(metas_sanitarias, df_rem_2024, key, region_id, cols_df, cols_grup):
    """
    Calcula el numerador de la meta `key` (en metas_sanitarias),
    para la región `region_id`, agrupando por las columnas en `cols_grup`.
    Considera por separado el conjunto de códigos 'cod' y sus columnas 'col',
    y el conjunto 'cod2' con sus columnas 'col2', para luego sumar ambos resultados.
    """

    # --- Paso 1: Crear DataFrame parcial para cod, col ---
    if "cod" in metas_sanitarias[key]["numerador"] and "col" in metas_sanitarias[key]["numerador"]:
        cod1 = metas_sanitarias[key]["numerador"]["cod"]
        col1 = metas_sanitarias[key]["numerador"]["col"]

        # Filtro por códigos cod1 y región
        df_cod1 = df_rem_2024.loc[
            (df_rem_2024.CodigoPrestacion.isin(cod1)) &
            (df_rem_2024.IdRegion == region_id)
        ].copy()

        # Nos quedamos con las columnas de identificación + col1
        df_cod1 = df_cod1[cols_df + col1]
        df_cod1.fillna(0, inplace=True)

        # Agrupamos y sumamos
        df_cod1 = df_cod1.groupby(by=cols_grup).sum().reset_index()
        df_cod1['temp_sum_cod1'] = df_cod1[col1].sum(axis=1)
        
        # Nos quedamos con cols de agrupación + columna parcial
        df_cod1 = df_cod1[cols_grup + ['temp_sum_cod1']]
    else:
        # Si no existen 'cod'/'col', dejamos un DF vacío con las columnas necesarias
        df_cod1 = pd.DataFrame(columns=cols_grup + ['temp_sum_cod1'])

    # --- Paso 2: Crear DataFrame parcial para cod2, col2 ---
    if "cod2" in metas_sanitarias[key]["numerador"] and "col2" in metas_sanitarias[key]["numerador"]:
        cod2 = metas_sanitarias[key]["numerador"]["cod2"]
        col2 = metas_sanitarias[key]["numerador"]["col2"]

        # Filtro por códigos cod2 y región
        df_cod2 = df_rem_2024.loc[
            (df_rem_2024.CodigoPrestacion.isin(cod2)) &
            (df_rem_2024.IdRegion == region_id)
        ].copy()

        # Nos quedamos con las columnas de identificación + col2
        df_cod2 = df_cod2[cols_df + col2]
        df_cod2.fillna(0, inplace=True)

        # Agrupamos y sumamos
        df_cod2 = df_cod2.groupby(by=cols_grup).sum().reset_index()
        df_cod2['temp_sum_cod2'] = df_cod2[col2].sum(axis=1)

        # Nos quedamos con cols de agrupación + columna parcial
        df_cod2 = df_cod2[cols_grup + ['temp_sum_cod2']]
    else:
        df_cod2 = pd.DataFrame(columns=cols_grup + ['temp_sum_cod2'])

    # --- Paso 3: Unir (merge) los resultados parciales ---
    #    Usamos 'outer' para no perder filas si existen en uno y no en otro.
    df_numerador_est = pd.merge(df_cod1, df_cod2, on=cols_grup, how='outer')

    # Llenar NaN con 0 (en caso de filas que existan en un DF y no en el otro)
    df_numerador_est[['temp_sum_cod1','temp_sum_cod2']] = df_numerador_est[['temp_sum_cod1','temp_sum_cod2']].fillna(0)

    # --- Paso 4: Sumar los subtotales para el numerador final ---
    df_numerador_est[f'Numerador_{key}'] = df_numerador_est['temp_sum_cod1'] + df_numerador_est['temp_sum_cod2']

    # --- Paso 5: Quedarnos sólo con las columnas finales ---
    df_numerador_est = df_numerador_est[cols_grup + [f'Numerador_{key}']]

    return df_numerador_est


def calcular_denominador(metas_sanitarias, df_rem_2024, key, region_id, cols_df, cols_grup):
    df_denominador = df_rem_2024.loc[df_rem_2024.CodigoPrestacion.isin(metas_sanitarias[key]["denominador"]["cod"])]
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
    df_group_denominador = df_group_denominador[['Código Centro','Dependencia Adm.' ,'Inscritos']]
    df_group_denominador = df_group_denominador.rename(columns={'Código Centro': 'IdEstablecimiento'})
    df_group_denominador = df_group_denominador.rename(columns={'Inscritos': f'Denominador_{key}'})
    return df_group_denominador

#%% Definición de parámetros y procesamiento
cols_df = [  'IdEstablecimiento', 'Ano', 'Mes', 'IdRegion']
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
    df_numerador_est1 = calcular_numerador(metas_sanitarias, df_rem_2024, key, region_id, cols_df, cols_grup)
    df_denominador_est1 = calcular_denominador(metas_sanitarias, df_rem_2024, key, region_id, cols_df, cols_grup)
    df_resultado1=df_numerador_est1.merge(df_denominador_est1, on=cols_merge, how='outer')
    resultado[key]=df_resultado1
#%% Calcular denominadores FONASA y actualizar resultados para metas sanitarias con 'sexo' y 'edad'
denominadores_fonasa = {}
for key in ms_denominador_fonasa:
    print(key)
    df_numerador_est2 = calcular_numerador(metas_sanitarias, df_rem_2024, key, region_id, cols_df, cols_grup)
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
#%%
# Agregar 'Dependencia Administrativa' y 'Nivel de Atención' para hacer filtros
df_final = pd.concat(resultados_list, ignore_index=True)

# Agregar establecimientos que no reportan REM20
# fonasa_rm_merge=fonasa_rm.rename(columns={
# 'Código Centro':'',
# 'Código Comuna':'IdComuna',
# })
# df_final=pd.concat([fonasa_rm_merge[['IdEstablecimiento','IdComuna']],df_final])

df_final = df_final.merge(df_deis[['Código Vigente','Dependencia Administrativa','Nivel de Atención']],left_on='IdEstablecimiento', right_on='Código Vigente')

df_final.to_csv('MS2024.csv', index=False, encoding='utf-8')
print("Archivo CSV guardado exitosamente.")
# %%