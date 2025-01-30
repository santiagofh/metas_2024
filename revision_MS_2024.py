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
                    "Col37",
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
directory = r"C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\DATA\REM\archivos_extraidos_2024"

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
# %%

establecimientos_maipu_municipal=[
111378,
111379,
111380,
111382,
111383,
111783,
111784,
200643,
201129
]

df_rem_maipu=df_rem.loc[df_rem['IdEstablecimiento'].isin(establecimientos_maipu_municipal)]
df_rem_maipu.to_excel("data/df_rem_2024_maipu_municipal.xlsx")
# %%
