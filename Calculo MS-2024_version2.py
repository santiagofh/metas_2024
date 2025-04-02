
#%% Importaciones
import os
import pandas as pd
import json

#%% Lectura de datos y filtrado de archivos REM en carpeta 2024 y 2023
directory_2024 = r"C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\DATA\REM\REM_2024"
directory_2023 = r"C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\DATA\REM\REM_2023"

all_codes = [
    "02010420", 
    "03500366",
    "02010321", 
    "03500334",
    "P1206010", 
    "P1206020", 
    "P1206030", 
    "P1206040", 
    "P1206050", 
    "P1206060", 
    "P1206070", 
    "P1206080",
    "03500364", 
    "03500365",
    "09220100", 
    "P4180300", 
    "P4200200",
    "P4190809", 
    "P4170300", 
    "P4190500", 
    "P4190600", 
    "P4150602",
    "P4180200", 
    "P4200100",
    "A0200002", 
    "A0200001",
    "P3161041", 
    "P3161045"
]


def leer_y_filtrar_archivos(directorio, all_codes, sep=";", chunksize=1000):
    datos_filtrados = []

    for root, dirs, files in os.walk(directorio):
        for filename in files:
            if filename.endswith(".csv") or filename.endswith(".txt"):
                filepath = os.path.join(root, filename)
                for chunk in pd.read_csv(filepath, sep=sep, chunksize=chunksize):
                    filtered_chunk = chunk[chunk['CodigoPrestacion'].isin(all_codes)]
                    datos_filtrados.append(filtered_chunk)

    if datos_filtrados:
        return pd.concat(datos_filtrados, ignore_index=True)
    else:
        return pd.DataFrame()

leer=True
if leer:
    df_rem_2024 = leer_y_filtrar_archivos(directory_2024, all_codes)
    df_rem_2023 = leer_y_filtrar_archivos(directory_2023, all_codes)
#%% -----------------------------------------------------------------------------------------
# Ajustar la información de región y año si es necesario, 
# en caso de que no existan columnas 'Ano', 'IdRegion' o haya que crearlas.

# Ejemplo: Si no existe, podríamos asignar:
# df_rem_2024['Ano'] = 2024
# df_rem_2024['IdRegion'] = # Colocar la región que corresponda o proveniente del archivo
# ...
# Dependiendo de la fuente real de datos

#%% -----------------------------------------------------------------------------------------
# Lectura de DEIS (para cruzar datos de establecimientos: Dependencia Admin, Nivel, etc.)
path_deis = r"C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\GIE\DEIS\Listado de establecimientos\Establecimientos DEIS MINSAL 07-01-2025 (2).xlsx"
df_deis = pd.read_excel(path_deis)

# Renombrar columnas relevantes
df_deis = df_deis.rename(columns={
    'Código Vigente': 'IdEstablecimiento',
    'Código Dependencia Jerárquica (SEREMI / Servicio de Salud)': 'IdServicio',
    'Código Región': 'IdRegion',
    'IdComuna': 'Código Comuna'
})

#%% -----------------------------------------------------------------------------------------
# Lectura FONASA
fonasa1 = pd.read_excel('FONASA/Copia de T6603_Inscritos.xlsx', sheet_name='Respuesta M', skiprows=4)
fonasa2 = pd.read_excel('FONASA/Copia de T6603_Inscritos.xlsx', sheet_name='Respuesta S', skiprows=4)
fonasa = pd.concat([fonasa1, fonasa2], ignore_index=True)

ss_rm = [
    'Metropolitano Central', 'Metropolitano Norte', 'Metropolitano Occidente', 
    'Metropolitano Oriente', 'Metropolitano Sur', 'Metropolitano Sur Oriente','Metropolitano Central'
]
fonasa_rm = fonasa.loc[fonasa['Servicio de Salud'].isin(ss_rm)].copy()

# IMPORTANTE: Ajustar este ID de región para filtrar, si se desea trabajar solo en la RM
region_id = 13

#%% -----------------------------------------------------------------------------------------
# Funciones auxiliares (para sumar columnas, etc.)

def sumar_columnas_por_establecimiento(df, codigos, columnas_sumar, region_id):
    """
    Filtra df según 'CodigoPrestacion' en 'codigos' y 'IdRegion' == region_id,
    agrupa por IdEstablecimiento, Ano, Mes, y retorna un DataFrame
    con la suma de las columnas especificadas en 'columnas_sumar'.
    
    El DataFrame resultante contiene:
    [IdEstablecimiento, Ano, Mes, 'suma']
    """
    # Ajustar nombres de columnas de agrupación según existan en df
    cols_grup = ['IdEstablecimiento', 'Ano', 'Mes']
    df_filt = df.loc[
        (df['CodigoPrestacion'].isin(codigos)) &
        (df['IdRegion'] == region_id)
    ].copy()
    
    # Nos aseguramos de que las columnas a sumar existan, y si no, las creamos en 0
    for col in columnas_sumar:
        if col not in df_filt.columns:
            df_filt[col] = 0

    # Llenamos NaN con 0
    df_filt[columnas_sumar] = df_filt[columnas_sumar].fillna(0)

    # Agrupamos
    df_grouped = df_filt.groupby(cols_grup)[columnas_sumar].sum().reset_index()

    # Creamos la columna 'suma' con la suma en cada fila
    df_grouped['suma'] = df_grouped[columnas_sumar].sum(axis=1)

    # Devolvemos solo las columnas de interés
    return df_grouped[cols_grup + ['suma']]

def sumar_denominador_fonasa(
    fonasa_rm, 
    edades=None, 
    sexo=None, 
    prevalencias=None
):
    """
    Calcula la suma (o ponderación por prevalencias) de 'Inscritos' según sexo y rango(s) de edad,
    en la información de FONASA.
    - edades: lista de listas con rangos, ej. [range(25,65)] o [range(15,25), range(25,45), ...]
    - sexo: lista, ej. ["Mujeres"] o ["Hombres","Mujeres"], etc.
    - prevalencias: si existe, debe ser un array del mismo largo que 'edades',
      para multiplicar los inscritos por esa prevalencia.

    Retorna un DataFrame con columnas:
    ['IdEstablecimiento', 'Inscritos_suma_fonasa']
    donde 'Inscritos_suma_fonasa' es la suma (o la suma de la multiplicación por prevalencia).
    """
    df_final_list = []

    # Copiamos para no afectar el original
    df_fon = fonasa_rm.copy()

    if sexo is not None:
        df_fon = df_fon[df_fon['Sexo'].isin(sexo)]

    if edades is not None:
        # Caso con prevalencias
        if prevalencias is not None and len(prevalencias) == len(edades):
            for i, rango_edad in enumerate(edades):
                tmp = df_fon[df_fon['Edad'].isin(rango_edad)].copy()
                tmp['Inscritos'] = tmp['Inscritos'] * prevalencias[i]
                df_final_list.append(tmp)
            df_concat = pd.concat(df_final_list, ignore_index=True)
        else:
            # Sin prevalencias
            df_concat = df_fon[df_fon['Edad'].isin(edades[0])]  # asumiendo una sola lista
    else:
        # Sin filtro de edades, ni prevalencias
        df_concat = df_fon

    # Agrupamos por establecimiento
    df_group = df_concat.groupby('Código Centro')['Inscritos'].sum().reset_index()

    df_group = df_group.rename(columns={
        'Código Centro': 'IdEstablecimiento',
        'Inscritos': 'Inscritos_suma_fonasa'
    })

    return df_group

#%% -----------------------------------------------------------------------------------------
# Definición de funciones ESPECÍFICAS para cada meta
# Cada función retorna un DataFrame con columnas:
# [IdEstablecimiento, Ano, Mes, Numerador_{META}, Denominador_{META}]

# ------------------------------------------------------------------------------
# META I (MSI)
def calcular_MSI(df_rem_2023, df_rem_2024, region_id):
    """
    Cálculo de la Meta Sanitaria I (MSI) tomando información 
    desde Octubre de 2023 (df_rem_2023) hasta Septiembre de 2024 (df_rem_2024).

    Numerador: 
      Códigos: ["02010420", "03500366"]
      Columnas a sumar: ["Col08", "Col09", "Col10", "Col11"]

    Denominador: 
      Códigos: ["02010321", "03500334"]
      Columnas a sumar: ["Col08", "Col09", "Col10", "Col11"]

    Ambas sumatorias se filtran por 'IdRegion' == region_id 
    y se agrupan por [IdEstablecimiento, Ano, Mes].
    """
    # 1) Filtramos df_rem_2023 sólo para meses >= 10 (Oct, Nov, Dic)
    df_2023_oct_to_dec = df_rem_2023.loc[df_rem_2023['Mes'] >= 10].copy()
    
    # 2) Filtramos df_rem_2024 sólo para meses <= 9 (Ene hasta Sep)
    df_2024_jan_to_sep = df_rem_2024.loc[df_rem_2024['Mes'] <= 9].copy()
    
    # 3) Concatenamos ambos
    df_combined = pd.concat([df_2023_oct_to_dec, df_2024_jan_to_sep], ignore_index=True)
    
    df_rem_2024

    # 4) Calculamos el Numerador (usando tu función auxiliar para sumar columnas)
    df_num = sumar_columnas_por_establecimiento(
        df=df_rem_2024,
        codigos=["02010420", "03500366"],
        columnas_sumar=["Col08", "Col09", "Col10", "Col11"],
        region_id=region_id
    )
    df_num = df_num.rename(columns={'suma': 'Numerador_MSI'})
    
    # 5) Calculamos el Denominador
    df_den = sumar_columnas_por_establecimiento(
        df=df_combined,
        codigos=["02010321", "03500334"],
        columnas_sumar=["Col08", "Col09", "Col10", "Col11"],
        region_id=region_id
    )
    df_den = df_den.rename(columns={'suma': 'Denominador_MSI'})
    
    # 6) Unimos ambos en un solo DataFrame
    df_merge = pd.merge(
        df_num, 
        df_den, 
        on=['IdEstablecimiento', 'Ano', 'Mes'], 
        how='outer'
    )
    
    return df_merge

# ------------------------------------------------------------------------------
# META II (MSII)
def calcular_MSII(df_rem, fonasa_rm, region_id):
    """
    Numerador (REM):
        Códigos: "P1206010", ..., "P1206080"
        Columnas: ["Col01","Col02"]
    Denominador (FONASA):
        Mujeres de 25 a 64 años (25..65), sin prevalencia
    """
    # Numerador
    df_num = sumar_columnas_por_establecimiento(
        df=df_rem,
        codigos=[
            "P1206010","P1206020","P1206030","P1206040","P1206050",
            "P1206060","P1206070","P1206080"
        ],
        columnas_sumar=["Col01", "Col02"],
        region_id=region_id
    )
    df_num = df_num.rename(columns={'suma':'Numerador_MSII'})

    # Denominador (FONASA): Mujeres 25-64
    df_den_fona = sumar_denominador_fonasa(
        fonasa_rm=fonasa_rm,
        edades=[range(25,65)],
        sexo=["Mujeres"]
    )
    df_den_fona = df_den_fona.rename(columns={'Inscritos_suma_fonasa':'Denominador_MSII'})

    # Unir
    df_merge = pd.merge(df_num, df_den_fona, 
                        on='IdEstablecimiento', 
                        how='outer')
    return df_merge

# ------------------------------------------------------------------------------
# META IIIa (MSIIIa)
def calcular_MSIIIa(df_rem, fonasa_rm, region_id):
    """
    Numerador (REM):
        Códigos: ["03500364", "03500365"]
        Columnas: "Col04".."Col23"
    Denominador (FONASA):
        Niños/as 0-9 años (0..10), sin prevalencias (ejemplo base).
        (En el prototipo original se usaba: "edad": [list(range(0,10))])
    """
    # Numerador
    cols_numerador = [
        "Col04","Col05","Col06","Col07","Col08","Col09","Col10","Col11",
        "Col12","Col13","Col14","Col15","Col16","Col17","Col18","Col19",
        "Col20","Col21","Col22","Col23"
    ]
    df_num = sumar_columnas_por_establecimiento(
        df=df_rem,
        codigos=["03500364","03500365"],
        columnas_sumar=cols_numerador,
        region_id=region_id
    )
    df_num = df_num.rename(columns={'suma':'Numerador_MSIIIa'})

    # Denominador (FONASA): 0-9 años
    df_den_fona = sumar_denominador_fonasa(
        fonasa_rm=fonasa_rm,
        edades=[range(0,10)],  # Ajustar si se requiere
        sexo=None,
        prevalencias=None
    )
    df_den_fona = df_den_fona.rename(columns={'Inscritos_suma_fonasa':'Denominador_MSIIIa'})

    # Unir
    df_merge = pd.merge(df_num, df_den_fona, 
                        on='IdEstablecimiento', 
                        how='outer')
    return df_merge

# ------------------------------------------------------------------------------
# META IIIb (MSIIIb)
def calcular_MSIIIb(df_rem, fonasa_rm, region_id):
    """
    Numerador (REM):
      Código: ["09220100"]
      Columnas: ["Col16", "Col17"]
    Denominador (FONASA):
      Edad 6 años (ejemplo range(6,7) o [6]).
    """
    # Numerador
    df_num = sumar_columnas_por_establecimiento(
        df=df_rem,
        codigos=["09220100"],
        columnas_sumar=["Col16","Col17"],
        region_id=region_id
    )
    df_num = df_num.rename(columns={'suma':'Numerador_MSIIIb'})

    # Denominador (FONASA): 6 años
    df_den_fona = fonasa_rm.copy()
    # Filtrar 6 años
    df_den_fona = df_den_fona[df_den_fona['Edad'] == 6]
    df_den_fona_group = df_den_fona.groupby('Código Centro')['Inscritos'].sum().reset_index()
    df_den_fona_group = df_den_fona_group.rename(columns={
        'Código Centro': 'IdEstablecimiento',
        'Inscritos': 'Denominador_MSIIIb'
    })

    # Unir
    df_merge = pd.merge(df_num, df_den_fona_group, 
                        on='IdEstablecimiento', 
                        how='outer')
    return df_merge

# ------------------------------------------------------------------------------
# META IVa (MSIVa)
def calcular_MSIVa(df_rem, fonasa_rm, region_id):
    """
    Numerador (REM):
      Códigos: ["P4180300","P4200200"]
      Columnas: ["Col01"]
    Denominador (FONASA):
      Cuatro rangos de edad con cuatro prevalencias:
         15-24 (0.018), 25-44 (0.063), 45-64 (0.183), >=65 (0.306)
    """
    # Numerador
    df_num = sumar_columnas_por_establecimiento(
        df=df_rem,
        codigos=["P4180300","P4200200"],
        columnas_sumar=["Col01"],
        region_id=region_id
    )
    df_num = df_num.rename(columns={'suma':'Numerador_MSIVa'})

    # Denominador (FONASA) con prevalencias
    edades_list = [range(15,25), range(25,45), range(45,65), range(65,200)]
    prevalencias_list = [0.018, 0.063, 0.183, 0.306]
    df_den_fona = sumar_denominador_fonasa(
        fonasa_rm=fonasa_rm,
        edades=edades_list,
        sexo=None,
        prevalencias=prevalencias_list
    )
    df_den_fona = df_den_fona.rename(columns={'Inscritos_suma_fonasa':'Denominador_MSIVa'})

    # Unir
    df_merge = pd.merge(df_num, df_den_fona, 
                        on='IdEstablecimiento', 
                        how='outer')
    return df_merge

# ------------------------------------------------------------------------------
# META IVb (MSIVb)
def calcular_MSIVb(df_rem, region_id):
    """
    Numerador (REM):
      Códigos: ["P4190809","P4170300","P4190500","P4190600"]
      Columnas: ["Col01"]
    Denominador (REM):
      Códigos: ["P4150602"]
      Columnas: ["Col01"]
    """
    # Numerador
    df_num = sumar_columnas_por_establecimiento(
        df=df_rem,
        codigos=["P4190809","P4170300","P4190500","P4190600"],
        columnas_sumar=["Col01"],
        region_id=region_id
    )
    df_num = df_num.rename(columns={'suma':'Numerador_MSIVb'})

    # Denominador
    df_den = sumar_columnas_por_establecimiento(
        df=df_rem,
        codigos=["P4150602"],
        columnas_sumar=["Col01"],
        region_id=region_id
    )
    df_den = df_den.rename(columns={'suma':'Denominador_MSIVb'})

    # Unir
    df_merge = pd.merge(df_num, df_den, 
                        on=['IdEstablecimiento', 'Ano', 'Mes'], 
                        how='outer')
    return df_merge

# ------------------------------------------------------------------------------
# META V (MSV)
def calcular_MSV(df_rem, fonasa_rm, region_id):
    """
    Numerador (REM):
      Códigos: ["P4180200","P4200100"]
      Columnas: ["Col01"]
    Denominador (FONASA):
      Igual que en MSIVa, 4 rangos de edad con prevalencias:
        - 15-24 (0.007), 25-44 (0.106), 45-64 (0.451), >=65 (0.733)
    """
    # Numerador
    df_num = sumar_columnas_por_establecimiento(
        df=df_rem,
        codigos=["P4180200","P4200100"],
        columnas_sumar=["Col01"],
        region_id=region_id
    )
    df_num = df_num.rename(columns={'suma':'Numerador_MSV'})

    # Denominador con prevalencias
    edades_list = [range(15,25), range(25,45), range(45,65), range(65,200)]
    prevalencias_list = [0.007, 0.106, 0.451, 0.733]
    df_den_fona = sumar_denominador_fonasa(
        fonasa_rm=fonasa_rm,
        edades=edades_list,
        sexo=None,
        prevalencias=prevalencias_list
    )
    df_den_fona = df_den_fona.rename(columns={'Inscritos_suma_fonasa':'Denominador_MSV'})

    # Unir
    df_merge = pd.merge(df_num, df_den_fona, 
                        on='IdEstablecimiento', 
                        how='outer')
    return df_merge

# ------------------------------------------------------------------------------
# META VI (MSVI)
def calcular_MSVI(df_rem, region_id):
    """
    Numerador (REM):
      Código: ["A0200002"]
      Columnas: ["Col06"]
    Denominador (REM):
      Código: ["A0200001"]
      Columnas: ["Col06"]
    """
    df_num = sumar_columnas_por_establecimiento(
        df=df_rem,
        codigos=["A0200002"],
        columnas_sumar=["Col06"],
        region_id=region_id
    )
    df_num = df_num.rename(columns={'suma':'Numerador_MSVI'})

    df_den = sumar_columnas_por_establecimiento(
        df=df_rem,
        codigos=["A0200001"],
        columnas_sumar=["Col06"],
        region_id=region_id
    )
    df_den = df_den.rename(columns={'suma':'Denominador_MSVI'})

    df_merge = pd.merge(df_num, df_den, 
                        on=['IdEstablecimiento','Ano','Mes'], 
                        how='outer')
    return df_merge

# ------------------------------------------------------------------------------
# META VII (MSVII)
def calcular_MSVII(df_rem, fonasa_rm, region_id):
    """
    Numerador (REM):
      1) cod=["P3161041"], col=["Col06".."Col37"]
      2) cod2=["P3161045"], col2=["Col01"] 
      Sumar ambos resultados.

    Denominador (FONASA) con prevalencia en dos rangos:
      - 40+ (0.117)
      - 5+ (0.10)
      (basado en el prototipo original: "edad": [list(range(40,120)), list(range(5,40))], "prevalencia": [0.117, 0.10])
    """
    # Numerador 1
    cols_1 = [f"Col{str(i).zfill(2)}" for i in range(6,38)]  # Col06..Col37
    df_num1 = sumar_columnas_por_establecimiento(
        df=df_rem,
        codigos=["P3161041"],
        columnas_sumar=cols_1,
        region_id=region_id
    )
    df_num1 = df_num1.rename(columns={'suma':'temp1'})

    # Numerador 2
    df_num2 = sumar_columnas_por_establecimiento(
        df=df_rem,
        codigos=["P3161045"],
        columnas_sumar=["Col01"],
        region_id=region_id
    )
    df_num2 = df_num2.rename(columns={'suma':'temp2'})

    df_numerador = pd.merge(df_num1, df_num2, 
                            on=['IdEstablecimiento','Ano','Mes'], 
                            how='outer')
    df_numerador[['temp1','temp2']] = df_numerador[['temp1','temp2']].fillna(0)
    df_numerador['Numerador_MSVII'] = df_numerador['temp1'] + df_numerador['temp2']
    df_numerador = df_numerador.drop(columns=['temp1','temp2'])

    # Denominador (FONASA): 
    # Rango1: 40-120 => prevalencia=0.117
    # Rango2: 5-120   => prevalencia=0.10
    edades_list = [range(40, 200), range(5, 200)]
    prevalencias_list = [0.117, 0.10]
    df_den_fona = sumar_denominador_fonasa(
        fonasa_rm=fonasa_rm,
        edades=edades_list,
        sexo=None,
        prevalencias=prevalencias_list
    )
    df_den_fona = df_den_fona.rename(columns={'Inscritos_suma_fonasa':'Denominador_MSVII'})

    # Unir
    df_merge = pd.merge(df_numerador, df_den_fona, 
                        on='IdEstablecimiento', 
                        how='outer')
        # Asegurar que cada establecimiento tenga datos en el mes 12
    registros_extra = []
    for establecimiento in df_merge['IdEstablecimiento'].unique():
        if not ((df_merge['IdEstablecimiento'] == establecimiento) & (df_merge['Mes'] == 12)).any():
            denominador = df_merge.loc[df_merge['IdEstablecimiento'] == establecimiento, 'Denominador_MSVII'].values[0]
            ano = df_merge.loc[df_merge['IdEstablecimiento'] == establecimiento, 'Ano'].values[0]

            registros_extra.append({
                'IdEstablecimiento': establecimiento,
                'Ano': ano,
                'Mes': 12,
                'Numerador_MSVII': 0,  # No hay datos de numerador
                'Denominador_MSVII': denominador
            })

    df_extra = pd.DataFrame(registros_extra)
    df_final = pd.concat([df_merge, df_extra], ignore_index=True)
    return df_final

#%% -----------------------------------------------------------------------------------------
# Cálculo de cada Meta por separado
df_MSI = calcular_MSI(df_rem_2023, df_rem_2024, region_id)
df_MSII  = calcular_MSII(df_rem_2024, fonasa_rm, region_id)
df_MSIIIa= calcular_MSIIIa(df_rem_2024, fonasa_rm, region_id)
df_MSIIIb= calcular_MSIIIb(df_rem_2024, fonasa_rm, region_id)
df_MSIVa = calcular_MSIVa(df_rem_2024, fonasa_rm, region_id)
df_MSIVb = calcular_MSIVb(df_rem_2024, region_id)
df_MSV   = calcular_MSV(df_rem_2024, fonasa_rm, region_id)
df_MSVI  = calcular_MSVI(df_rem_2024, region_id)
df_MSVII = calcular_MSVII(df_rem_2024, fonasa_rm, region_id)

#%% -----------------------------------------------------------------------------------------
# Unir todos los resultados en un formato "largo" (row by meta)
# Cada uno tendrá:
#   [IdEstablecimiento, Ano, Mes, Numerador_XXX, Denominador_XXX]

# Para facilitar la unión final en un solo DataFrame "largo", 
# transformamos cada DataFrame para tener las columnas [IdEstablecimiento, Ano, Mes, Numerador, Denominador, MetaSanitaria]

def preparar_df_final(df_in, meta_name, num_col, den_col):
    df_out = df_in.copy()
    df_out['MetaSanitaria'] = meta_name
    df_out = df_out.rename(columns={
        num_col: 'Numerador',
        den_col: 'Denominador'
    })
    # Nos aseguramos de que existan las columnas de agrupación
    for c in ['Ano','Mes','IdEstablecimiento']:
        if c not in df_out.columns:
            df_out[c] = None
    df_out = df_out[['IdEstablecimiento','Ano','Mes','Numerador','Denominador','MetaSanitaria']]
    return df_out

dfs_finales = []

dfs_finales.append(preparar_df_final(df_MSI,   'MSI',   'Numerador_MSI',   'Denominador_MSI'))
dfs_finales.append(preparar_df_final(df_MSII,  'MSII',  'Numerador_MSII',  'Denominador_MSII'))
dfs_finales.append(preparar_df_final(df_MSIIIa,'MSIIIa','Numerador_MSIIIa','Denominador_MSIIIa'))
dfs_finales.append(preparar_df_final(df_MSIIIb,'MSIIIb','Numerador_MSIIIb','Denominador_MSIIIb'))
dfs_finales.append(preparar_df_final(df_MSIVa, 'MSIVa', 'Numerador_MSIVa', 'Denominador_MSIVa'))
dfs_finales.append(preparar_df_final(df_MSIVb, 'MSIVb', 'Numerador_MSIVb', 'Denominador_MSIVb'))
dfs_finales.append(preparar_df_final(df_MSV,   'MSV',   'Numerador_MSV',   'Denominador_MSV'))
dfs_finales.append(preparar_df_final(df_MSVI,  'MSVI',  'Numerador_MSVI',  'Denominador_MSVI'))
dfs_finales.append(preparar_df_final(df_MSVII, 'MSVII', 'Numerador_MSVII','Denominador_MSVII'))

df_final = pd.concat(dfs_finales, ignore_index=True)

#%% -----------------------------------------------------------------------------------------
# Agregar información de Dependencia y Nivel de Atención (u otros) desde df_deis
# Asumimos que df_deis tiene 'IdEstablecimiento' como key

if 'Dependencia Administrativa' in df_deis.columns:
    dep_col = 'Dependencia Administrativa'
else:
    dep_col = 'DependenciaAdm'  # Ajustar si difiere

if 'Nivel de Atención' in df_deis.columns:
    nivel_col = 'Nivel de Atención'
else:
    nivel_col = 'NivelAtencion'  # Ajustar si difiere

cols_merge_deis = ['IdEstablecimiento', dep_col, nivel_col]
df_deis_merge = df_deis.drop_duplicates(subset=['IdEstablecimiento'])

df_final2 = pd.merge(df_final, 
                     df_deis_merge[cols_merge_deis], 
                     on='IdEstablecimiento', 
                     how='left')

#%% -----------------------------------------------------------------------------------------
# Exportar a CSV (formato unificado)
df_final2.to_csv('MS2024_v2.csv', index=False, encoding='utf-8')
print("Archivo CSV guardado exitosamente: 'MS2024_v2.csv'")
#%% -----------------------------------------------------------------------------------------
