#%%
import pandas as pd
#%%
# Lectura FONASA
fonasa1 = pd.read_excel('FONASA/Copia de T6603_Inscritos.xlsx', sheet_name='Respuesta M', skiprows=4)
fonasa2 = pd.read_excel('FONASA/Copia de T6603_Inscritos.xlsx', sheet_name='Respuesta S', skiprows=4)
fonasa = pd.concat([fonasa1, fonasa2], ignore_index=True)
ss_rm = [
    'Metropolitano Central', 'Metropolitano Norte', 'Metropolitano Occidente', 
    'Metropolitano Oriente', 'Metropolitano Sur', 'Metropolitano Sur Oriente','Metropolitano Central'
]
fonasa_rm = fonasa.loc[fonasa['Servicio de Salud'].isin(ss_rm)].copy()
#%%
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
#%%
# META I
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
#%%
# META II
"""
Denominador (FONASA):
    Mujeres de 25 a 64 años (25..65), sin prevalencia
"""

ms2=sumar_denominador_fonasa(
        fonasa_rm=fonasa_rm,
        edades=[range(25,65)],
        sexo=["Mujeres"]
    )
# %%
# META IIIa
"""
Denominador (FONASA):
    Niños/as 0-9 años (0..10), sin prevalencias (ejemplo base).
    (En el prototipo original se usaba: "edad": [list(range(0,10))])
"""
ms3a = sumar_denominador_fonasa(
    fonasa_rm=fonasa_rm,
    edades=[range(0,10)],
    sexo=None,
    prevalencias=None
)
# %%
# META IIIb
"""
Denominador (FONASA):
    Edad 6 años (ejemplo range(6,7) o [6]).
"""
ms3b = sumar_denominador_fonasa(
    fonasa_rm=fonasa_rm,
    edades=[range(6,7)],
    sexo=None,
    prevalencias=None
)
#%%
# META IVA
"""
Denominador (FONASA):
        15-24 (0.018), 25-44 (0.063), 45-64 (0.183), >=65 (0.306)
"""
ms4a = sumar_denominador_fonasa(
    fonasa_rm=fonasa_rm,
    edades=[range(15,25), range(25,45), range(45,65), range(65,200)],
    sexo=None,
    prevalencias=[0.018, 0.063, 0.183, 0.306]
)
#%%
# META V
"""
Denominador (FONASA):
    - 15-24 (0.007), 25-44 (0.106), 45-64 (0.451), >=65 (0.733)
"""
ms5 = sumar_denominador_fonasa(
    fonasa_rm=fonasa_rm,
    edades= [range(15,25), range(25,45), range(45,65), range(65,200)],
    sexo=None,
    prevalencias=[0.007, 0.106, 0.451, 0.733]
)
#%%
# META VII

"""
Denominador (FONASA) con prevalencia en dos rangos:
    - 40+ (0.117)
    - 5-39 (0.10)
    (basado en el prototipo original: "edad": [list(range(40,120)), list(range(5,40))], "prevalencia": [0.117, 0.10])
"""

ms7 = sumar_denominador_fonasa(
    fonasa_rm=fonasa_rm,
    edades=[range(40,120), range(5,40)],
    sexo=None,
    prevalencias=[0.117, 0.10]
)
# %%
# Lista de todos los DataFrames de MS y sus etiquetas
lista_ms = [
    (ms2, "II"),
    (ms3a, "IIIa"),
    (ms3b, "IIIb"),
    (ms4a, "IVa"),
    (ms5, "V"),
    (ms7, "VII")
]

# Agregar columna 'MS' y unir
df_final = pd.concat(
    [df.assign(MS=etiqueta) for df, etiqueta in lista_ms],
    ignore_index=True
)[["IdEstablecimiento", "MS", "Inscritos_suma_fonasa"]]
#%%
df_final.to_csv("data/ms_fonasa.csv")
# %%
