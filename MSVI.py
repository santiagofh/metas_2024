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
df_ms6 = df_ms.loc[df_ms.MetaSanitaria == 'MSVI']
df_ms6 = df_ms6.merge(df_est, on='IdEstablecimiento', how='left')
#%%
# Preparar los datos
df_ms6 = df_ms6.dropna(subset=['Ano', 'Mes'])
df_ms6['Ano'] = df_ms6['Ano'].fillna(0).astype(int)
df_ms6['Mes'] = df_ms6['Mes'].fillna(0).astype(int)
df_ms6['Numerador'] = df_ms6['Numerador'].fillna(0).astype(int)
df_ms6['Denominador'] = df_ms6['Denominador'].fillna(0).astype(int)
df_ms6['IdEstablecimiento'] = df_ms6['IdEstablecimiento'].astype(str)
df_ms6["comuna"] = df_ms6["comuna"].fillna("No especificado").astype(str)
df_ms6['nombre_establecimiento'] = df_ms6['nombre_establecimiento'].astype(str)
df_ms6 = df_ms6.dropna(subset=["servicio_salud", "comuna"])
df_ms6["servicio_salud"] = df_ms6["servicio_salud"].fillna("No especificado").astype(str)
df_ms6['codigo_nombre']=df_ms6['IdEstablecimiento']+' - '+df_ms6['nombre_establecimiento']
df_ms6 = df_ms6.groupby('IdEstablecimiento').agg({
    'Ano':'max',
    'Mes':'max',
    'Numerador':'sum',
    'Denominador':'sum',
    'codigo_nombre':'first',
    'comuna':'first',
    'Dependencia Administrativa':'first',
    'Nivel de Atención':'first',
    'servicio_salud':'first',
    }).reset_index()
df_ms6['Porcentaje'] = df_ms6['Numerador']/df_ms6['Denominador']
#%%

# Título del dashboard
st.title('Meta VI: Prevalencia de Lactancia Materna Exclusiva (LME) en menores de 6 meses de vida')

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
all_servicios = ["Todos"] + sorted(df_ms6["servicio_salud"].unique())
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
df_ms6_filtered = (
    df_ms6
    if selected_servicios == "Todos"
    else df_ms6[df_ms6["servicio_salud"] == selected_servicios]
)


# -----------------------------------------------------
# 4) FILTRO 2: Comuna
# -----------------------------------------------------
# Construimos las comunas disponibles dentro del subset ya filtrado
all_comunas = sorted(df_ms6_filtered["comuna"].unique())
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
    df_ms6_filtered = df_ms6_filtered[df_ms6_filtered["comuna"].isin(selected_comunas)]


# -----------------------------------------------------
# 5) FILTRO 3: Dependencia Administrativa
# -----------------------------------------------------
all_dependencias = sorted(df_ms6_filtered["Dependencia Administrativa"].dropna().unique())
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
    df_ms6_filtered = df_ms6_filtered[df_ms6_filtered["Dependencia Administrativa"].isin(selected_dependencias)]


# -----------------------------------------------------
# 6) FILTRO 4: Nivel de Atención
# -----------------------------------------------------
all_niveles = sorted(df_ms6_filtered["Nivel de Atención"].dropna().unique())
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
    df_ms6_filtered = df_ms6_filtered[df_ms6_filtered["Nivel de Atención"].isin(selected_niveles)]


# -----------------------------------------------------
# 7) FILTRO 5: Establecimientos
# -----------------------------------------------------
all_establecimientos = sorted(df_ms6_filtered["codigo_nombre"].dropna().unique())
selected_establecimientos = st.multiselect(
    "Seleccione Establecimientos",
    ["Todos"] + all_establecimientos,
    default=st.session_state["selected_establecimientos"]
)

st.session_state["selected_establecimientos"] = selected_establecimientos

if "Todos" not in selected_establecimientos:
    df_ms6_filtered = df_ms6_filtered[df_ms6_filtered["codigo_nombre"].isin(selected_establecimientos)]

#%%
# Mostrar datos filtrados
st.write(f"## Datos para la Meta Sanitaria")
st.write("Fecha de corte de datos: _Enero del 2025_")

# Información de resumen
num_services = df_ms6_filtered['servicio_salud'].nunique()
num_communes = df_ms6_filtered['comuna'].nunique()
num_establishments = df_ms6_filtered['codigo_nombre'].nunique()

# Dividir las métricas en 3 columnas
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label='N° Servicios de Salud', value=num_services)
with col2:
    st.metric(label='N° de comunas', value=num_communes)
with col3:
    st.metric(label='N° de establecimientos', value=num_establishments)
#%%
# Mostrar datagrame
col_ms6=['Ano', 'Mes','codigo_nombre','servicio_salud',  'Numerador', 'Denominador','Porcentaje']
rename_ms6={
    'Ano':'Año', 
    'Mes':'Mes',
    'codigo_nombre':'Nombre del establecimeinto',
    'servicio_salud':'Servicio de Salud',  
    'Numerador':'Numerador', 
    'Denominador':'Denominador',
    'Porcentaje':'Cumplimiento de la MS'
}
st.write(f"## Tabla de establecimientos")
st.write('A continuación se muestra la tabla de los establecimientos, su numerador, denominador y cumplimiento de la meta sanitaria')
st.write(df_ms6_filtered[col_ms6].rename(columns=rename_ms6))
#%%
# Calcular el total del numerador y denominador
total_numerador = df_ms6_filtered['Numerador'].sum()
total_denominador = df_ms6_filtered['Denominador'].sum()
total_porcentaje = (total_numerador / total_denominador) * 100 if total_denominador > 0 else 0
meta_nacional = 0.6
#%%
# Mostrar datos de Numerador, Denominador y Porcentaje de cumplimiento
st.write("## Cumplimiento de la Meta Sanitaria")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label='Numerador', value=total_numerador)
with col2:
    st.metric(label='Denominador', value=total_denominador)
with col3:
    st.metric(label='Porcentaje de cumplimiento', value=total_porcentaje)
with col4:
    st.metric(label='Meta Nacional', value=meta_nacional)
#%%
# Grafico Gauge
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=total_porcentaje,
    title={'text': 'INDICADOR'},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "blue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 60], 'color': "gray"},
            {'range': [60, 100], 'color': "lightgray"}
        ],
        'threshold': {
            'line': {'color': "black", 'width': 4},
            'thickness': 0.75,
            'value': total_porcentaje
        },
        'shape': "angular"
    }
))
st.plotly_chart(fig)

# #%%
# # Grafico de metas por mes
# grouped_data = df_ms6_filtered.groupby(['Ano', 'Mes'])[['Denominador', 'Numerador']].sum().reset_index()

# grouped_data['Denominador Acumulado'] = grouped_data.groupby('Ano')['Denominador'].cumsum()
# grouped_data['Numerador Acumulado'] = grouped_data.groupby('Ano')['Numerador'].cumsum()

# grouped_data['Cumplimiento'] = (grouped_data['Numerador Acumulado'] / grouped_data['Denominador Acumulado']) * 100

# fig = go.Figure()

# # Añadir trazas para el numerador acumulado, denominador acumulado y cumplimiento
# for year in grouped_data['Ano'].unique():
#     year_data = grouped_data[grouped_data['Ano'] == year]
#     fig.add_trace(go.Scatter(
#         x=year_data['Mes'],
#         y=year_data['Numerador Acumulado'],
#         mode='lines',
#         name=f'Numerador Acumulado {year}',
#         line=dict(color='red'),
#         yaxis='y1'
#     ))

#     fig.add_trace(go.Scatter(
#         x=year_data['Mes'],
#         y=year_data['Denominador Acumulado'],
#         mode='lines',
#         name=f'Denominador Acumulado {year}',
#         line=dict(color='blue'),
#         yaxis='y1'
#     ))

#     fig.add_trace(go.Scatter(
#         x=year_data['Mes'],
#         y=year_data['Cumplimiento'],
#         mode='lines',
#         name=f'Cumplimiento {year}',
#         line=dict(color='green'),
#         yaxis='y2'
#     ))

# # Configurar el layout del gráfico
# fig.update_layout(
#     title='Denominador, Numerador y Cumplimiento por Mes (MSVI)',
#     xaxis_title='Mes',
#     yaxis=dict(
#         title='Cantidad',
#         # titlefont=dict(color='black'),
#         # tickfont=dict(color='black')
#     ),
#     yaxis2=dict(
#         title='Cumplimiento (%)',
#         # titlefont=dict(color='black'),
#         # tickfont=dict(color='black'),
#         overlaying='y',
#         side='right',
#         range=[0, 100]
#     ),
#     legend_title='Tipo',
#     legend=dict(x=0, y=1, traceorder='normal')
# )

# # Mostrar el gráfico en Streamlit
# st.write("## Denominador, Numerador y Cumplimiento por Mes (MSVI)")
# st.plotly_chart(fig)

#%%
# GRAFICO POR COMUNAS
## Crear un DataFrame con el nombre de la comuna, denominador, numerador y porcentaje de cumplimiento
df_cumplimiento = df_ms6_filtered.groupby('comuna').agg(
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
    y0=60,
    x1=len(df_cumplimiento['comuna']) - 1,
    y1=60,
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

