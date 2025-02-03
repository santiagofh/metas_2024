#%% Importaciones
import os
import pandas as pd
import json
#%% Lectura de datos de FONASA
fonasa1 = pd.read_excel('FONASA/Copia de T6603_Inscritos.xlsx', sheet_name='Respuesta M', skiprows=4)
fonasa2 = pd.read_excel('FONASA/Copia de T6603_Inscritos.xlsx', sheet_name='Respuesta S', skiprows=4)
fonasa = pd.concat([fonasa1, fonasa2])
ss_rm = ['Metropolitano Central', 'Metropolitano Norte', 'Metropolitano Occidente', 'Metropolitano Oriente', 'Metropolitano Sur', 'Metropolitano Sur Oriente']
fonasa_rm = fonasa.loc[fonasa['Servicio de Salud'].isin(ss_rm)]

# %%
columnas=[
    'Servicio de Salud',
 	'Código Comuna',
    'Comuna',
    'Dependencia Adm.',	
    'Código Centro',	
    'Centro']
fonasa_rm=fonasa_rm[columnas]
# %%
fonasa_rm=fonasa_rm.drop_duplicates(subset=columnas)
# %%
rename_col={'Código Centro':'IdEstablecimiento'}
fonasa_rm.rename(columns=rename_col,inplace=True)
# %%

#%% Crear diccionario
establecimientos_dict = fonasa_rm.set_index('IdEstablecimiento').to_dict(orient='index')

#%% Exportar a archivo JSON
output_file = 'establecimientos.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(establecimientos_dict, f, ensure_ascii=False, indent=4)

print(f"Diccionario exportado a {output_file}")
# %%
