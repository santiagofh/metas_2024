#%%
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
#%%
# Ordenar dataframe
df_ms = pd.read_csv('MS2024.csv')
col_est=['Código Vigente','Nombre Oficial','Nombre Dependencia Jerárquica (SEREMI / Servicio de Salud)','Nombre Comuna']
col_rename={
    'Código Vigente':'IdEstablecimiento',
    'Nombre Oficial':'nombre_establecimiento',
    'Nombre Dependencia Jerárquica (SEREMI / Servicio de Salud)':'servicio_salud',
    'Nombre Comuna':'comuna'
}
df_est = pd.read_excel('Establecimientos DEIS MINSAL 28-05-2024 (1).xlsx', skiprows=1, usecols=col_est)
df_est = df_est.rename(columns=col_rename)
df_ms2 = df_ms.loc[df_ms.MetaSanitaria == 'MSII']
df_ms2 = df_ms2.merge(df_est, on='IdEstablecimiento', how='left')
#%%
# Preparar los datos
df_ms2 = df_ms2.dropna(subset=['Ano', 'Mes'])
df_ms2['Ano'] = df_ms2['Ano'].astype(int)
df_ms2['Mes'] = df_ms2['Mes'].astype(int)
df_ms2['Porcentaje'] = df_ms2['Numerador']/df_ms2['Denominador']
df_ms2['IdEstablecimiento'] = df_ms2['IdEstablecimiento'].astype(str)
df_ms2['nombre_establecimiento'] = df_ms2['nombre_establecimiento'].astype(str)
df_ms2 = df_ms2.dropna(subset=["servicio_salud", "comuna"])
df_ms2["servicio_salud"] = df_ms2["servicio_salud"].fillna("No especificado").astype(str)
df_ms2['codigo_nombre']=df_ms2['IdEstablecimiento']+' - '+df_ms2['nombre_establecimiento']
#%%

# Título del dashboard
st.title('Meta II: Detección precoz del cáncer de cuello uterino')
st.write('PAPANICOLAOU (PAP) O TEST DE VPH VIGENTE EN PERSONAS DE 25 A 64 AÑOS')


st.subheader("Filtros en Cascada")

# -----------------------------------------------------
# 1) DEFINICIÓN DE FUNCIONES PARA RESETEAR FILTROS
# -----------------------------------------------------
def reset_comunas_hacia_abajo():
    """
    Si el usuario cambia el Servicio de Salud, se resetean
    todos los filtros inferiores (comuna, dependencia, nivel, establecimiento).
    """
    st.session_state["selected_comunas"] = ["Todas"]
    st.session_state["selected_dependencias"] = ["Todas"]
    st.session_state["selected_niveles"] = ["Todos"]
    st.session_state["selected_establecimientos"] = ["Todos"]

def reset_dependencia_hacia_abajo():
    """
    Si cambia la comuna, se resetean los filtros: dependencia, nivel, establecimiento.
    """
    st.session_state["selected_dependencias"] = ["Todas"]
    st.session_state["selected_niveles"] = ["Todos"]
    st.session_state["selected_establecimientos"] = ["Todos"]

def reset_nivel_hacia_abajo():
    """
    Si cambia la dependencia, se resetean los filtros: nivel, establecimiento.
    """
    st.session_state["selected_niveles"] = ["Todos"]
    st.session_state["selected_establecimientos"] = ["Todos"]

def reset_establecimientos():
    """
    Si cambia el nivel, se resetea solamente el filtro de establecimientos.
    """
    st.session_state["selected_establecimientos"] = ["Todos"]


# -----------------------------------------------------
# 2) CREACIÓN DE VALORES POR DEFECTO EN SESSION_STATE
#    (solo la primera vez que corre la app)
# -----------------------------------------------------
if "selected_servicios" not in st.session_state:
    st.session_state["selected_servicios"] = "Todos"
if "selected_comunas" not in st.session_state:
    st.session_state["selected_comunas"] = ["Todas"]
if "selected_dependencias" not in st.session_state:
    st.session_state["selected_dependencias"] = ["Todas"]
if "selected_niveles" not in st.session_state:
    st.session_state["selected_niveles"] = ["Todos"]
if "selected_establecimientos" not in st.session_state:
    st.session_state["selected_establecimientos"] = ["Todos"]

# Guardamos también los valores anteriores para detectar cambios
if "prev_servicios" not in st.session_state:
    st.session_state["prev_servicios"] = "Todos"
if "prev_comunas" not in st.session_state:
    st.session_state["prev_comunas"] = ["Todas"]
if "prev_dependencias" not in st.session_state:
    st.session_state["prev_dependencias"] = ["Todas"]
if "prev_niveles" not in st.session_state:
    st.session_state["prev_niveles"] = ["Todos"]


# -----------------------------------------------------
# 3) FILTRO 1: Servicio de Salud
# -----------------------------------------------------
all_servicios = ["Todos"] + sorted(df_ms2["servicio_salud"].unique())
selected_servicios = st.selectbox(
    "Seleccione Servicios de Salud",
    all_servicios,
    index=all_servicios.index(st.session_state["selected_servicios"])  # reiniciar a lo que teníamos
)

# Si el valor ha cambiado respecto al anterior => resetea todo hacia abajo
if selected_servicios != st.session_state["prev_servicios"]:
    reset_comunas_hacia_abajo()

# Tras posibles reseteos, guardamos la selección actual
st.session_state["selected_servicios"] = selected_servicios
st.session_state["prev_servicios"] = selected_servicios

# ---- Aplicar este primer filtro ----
df_ms2_filtered = (
    df_ms2
    if selected_servicios == "Todos"
    else df_ms2[df_ms2["servicio_salud"] == selected_servicios]
)


# -----------------------------------------------------
# 4) FILTRO 2: Comuna
# -----------------------------------------------------
# Construimos las comunas disponibles dentro del subset ya filtrado
all_comunas = sorted(df_ms2_filtered["comuna"].unique())
selected_comunas = st.multiselect(
    "Seleccione Comunas",
    ["Todas"] + all_comunas,
    default=st.session_state["selected_comunas"]
)

# Si cambió la selección de comuna de forma que no coincide con la previa, reseteamos dependencias en adelante
if selected_comunas != st.session_state["prev_comunas"]:
    reset_dependencia_hacia_abajo()

# Guardamos la selección (y la previa)
st.session_state["selected_comunas"] = selected_comunas
st.session_state["prev_comunas"] = selected_comunas

# Aplicar el filtro de comuna
if "Todas" not in selected_comunas:
    df_ms2_filtered = df_ms2_filtered[df_ms2_filtered["comuna"].isin(selected_comunas)]


# -----------------------------------------------------
# 5) FILTRO 3: Dependencia Administrativa
# -----------------------------------------------------
all_dependencias = sorted(df_ms2_filtered["Dependencia Administrativa"].dropna().unique())
selected_dependencias = st.multiselect(
    "Seleccione Dependencia Administrativa",
    ["Todas"] + all_dependencias,
    default=st.session_state["selected_dependencias"]
)

# Si cambió, resetea filtro de nivel y establecimiento
if selected_dependencias != st.session_state["prev_dependencias"]:
    reset_nivel_hacia_abajo()

st.session_state["selected_dependencias"] = selected_dependencias
st.session_state["prev_dependencias"] = selected_dependencias

if "Todas" not in selected_dependencias:
    df_ms2_filtered = df_ms2_filtered[df_ms2_filtered["Dependencia Administrativa"].isin(selected_dependencias)]


# -----------------------------------------------------
# 6) FILTRO 4: Nivel de Atención
# -----------------------------------------------------
all_niveles = sorted(df_ms2_filtered["Nivel de Atención"].dropna().unique())
selected_niveles = st.multiselect(
    "Seleccione Nivel de Atención",
    ["Todos"] + all_niveles,
    default=st.session_state["selected_niveles"]
)

if selected_niveles != st.session_state["prev_niveles"]:
    reset_establecimientos()

st.session_state["selected_niveles"] = selected_niveles
st.session_state["prev_niveles"] = selected_niveles

if "Todos" not in selected_niveles:
    df_ms2_filtered = df_ms2_filtered[df_ms2_filtered["Nivel de Atención"].isin(selected_niveles)]


# -----------------------------------------------------
# 7) FILTRO 5: Establecimientos
# -----------------------------------------------------
all_establecimientos = sorted(df_ms2_filtered["codigo_nombre"].dropna().unique())
selected_establecimientos = st.multiselect(
    "Seleccione Establecimientos",
    ["Todos"] + all_establecimientos,
    default=st.session_state["selected_establecimientos"]
)

st.session_state["selected_establecimientos"] = selected_establecimientos

if "Todos" not in selected_establecimientos:
    df_ms2_filtered = df_ms2_filtered[df_ms2_filtered["codigo_nombre"].isin(selected_establecimientos)]


# -----------------------------------------------------
# 8) FILTRO de Mes (ejemplo)
# -----------------------------------------------------
all_meses = sorted(df_ms2_filtered['Mes'].unique())
selected_meses = st.selectbox('Seleccione mes de corte', all_meses, index=len(all_meses)-1)
df_ms2_filtered = df_ms2_filtered[df_ms2_filtered['Mes'] == selected_meses]


#%%
# Mostrar datos filtrados
st.write("## Datos para la Meta Sanitaria")
st.write("Fecha de corte de datos: _Enero del 2025_")

num_services = df_ms2_filtered['servicio_salud'].nunique()
num_communes = df_ms2_filtered['comuna'].nunique()
num_establishments = df_ms2_filtered['codigo_nombre'].nunique()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label='N° Servicios de Salud', value=num_services)
with col2:
    st.metric(label='N° de comunas', value=num_communes)
with col3:
    st.metric(label='N° de establecimientos', value=num_establishments)
#%%
# Mostrar DataFrame
col_ms2=['Ano', 'Mes','codigo_nombre','servicio_salud',  'Numerador', 'Denominador','Porcentaje']
rename_ms2={
    'Ano':'Año', 
    'Mes':'Mes',
    'codigo_nombre':'Nombre del establecimeinto',
    'servicio_salud':'Servicio de Salud',  
    'Numerador':'Numerador', 
    'Denominador':'Denominador',
    'Porcentaje':'Cumplimiento de la MS'
}
st.write('## Tabla de establecimientos')
st.write('A continuación se muestra la tabla de los establecimientos, su numerador, denominador y cumplimiento de la meta sanitaria')
st.write(df_ms2_filtered[col_ms2].rename(columns=rename_ms2))
#%%
#%% Descargar Excel con la tabla de establecimientos
import io

# Filtrar columnas y renombrar para el archivo
df_export = df_ms2_filtered[col_ms2].rename(columns=rename_ms2)

# Crear un buffer en memoria
output = io.BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df_export.to_excel(writer, index=False, sheet_name='Tabla_Establecimientos')

# Botón de descarga
st.download_button(
    label="📥 Descargar tabla de establecimientos (Excel)",
    data=output.getvalue(),
    file_name="tabla_establecimientos.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

#%%
# Calcular el total del numerador y denominador
total_numerador = df_ms2_filtered['Numerador'].sum()
total_denominador = df_ms2_filtered['Denominador'].sum()
total_porcentaje = (total_numerador / total_denominador) if total_denominador > 0 else 0
meta_nacional = 0.8
st.subheader("Cumplimiento de la Meta Sanitaria")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label='Numerador', value=total_numerador)
with col2:
    st.metric(label='Denominador', value=total_denominador)
with col3:
    st.metric(label='Porcentaje de cumplimiento', value=total_porcentaje)
with col4:
    st.metric(label='Meta Nacional', value=meta_nacional)

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=total_porcentaje * 100,  # Convertir a porcentaje
    title={'text': 'Cumplimiento'},
    gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "blue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 80], 'color': "gray"},
                {'range': [80, 100], 'color': "lightgray"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': total_porcentaje* 100
            },
            'shape': "angular"}
))
st.plotly_chart(fig)

#%%
# Crear un DataFrame con el nombre de la comuna, denominador, numerador y porcentaje de cumplimiento
df_cumplimiento = df_ms2_filtered.groupby('comuna').agg(
    total_numerador=('Numerador', 'sum'),
    total_denominador=('Denominador', 'sum')
).reset_index()

df_cumplimiento['porcentaje_cumplimiento'] = (df_cumplimiento['total_numerador'] / df_cumplimiento['total_denominador']) * 100

rename_cumplimiento={
    'porcentaje_cumplimiento':'Porcentaje de cumplimiento',
    'total_numerador':'Numerador',
    'total_denominador':'Denominador',
    'comuna':'Comuna'
}

# %%
df_cumplimiento = df_ms2_filtered.groupby('comuna').agg(
    total_numerador=('Numerador', 'sum'),
    total_denominador=('Denominador', 'sum')
).reset_index()

df_cumplimiento['porcentaje_cumplimiento'] = (df_cumplimiento['total_numerador'] / df_cumplimiento['total_denominador']) * 100

rename_cumplimiento = {
    'porcentaje_cumplimiento': 'Porcentaje de cumplimiento',
    'total_numerador': 'Numerador',
    'total_denominador': 'Denominador',
    'comuna': 'Comuna'
}

# Ordenar el DataFrame por porcentaje de cumplimiento de mayor a menor
df_cumplimiento = df_cumplimiento.sort_values(by='porcentaje_cumplimiento', ascending=False)

# Mostrar el DataFrame resultante
st.write("## Tabla de cumplimiento por comuna")
st.write(df_cumplimiento.rename(columns=rename_cumplimiento))

# Crear el gráfico de barras
fig = px.bar(
    df_cumplimiento,
    x='comuna',
    y='porcentaje_cumplimiento',
    title='Porcentaje de Cumplimiento por Comuna',
    labels={'comuna': 'Comuna', 'porcentaje_cumplimiento': 'Porcentaje de Cumplimiento'},
    text='porcentaje_cumplimiento'
)

# Agregar la línea horizontal para la meta nacional del 90%
fig.add_shape(
    type="line",
    x0=0,
    y0=80,
    x1=len(df_cumplimiento['comuna']) - 1,
    y1=80,
    line=dict(color="red", width=2, dash="dash"),
)

# Ajustar el diseño del gráfico
fig.update_layout(
    xaxis_title='Comuna',
    yaxis_title='Porcentaje de Cumplimiento',
    yaxis=dict(range=[0, 100])
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)