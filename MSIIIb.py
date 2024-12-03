# %%
# %%
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Leer los datos
df_ms = pd.read_csv('MS2024.csv')
col_est = ['Código Vigente', 'Nombre Oficial', 'Nombre Dependencia Jerárquica (SEREMI / Servicio de Salud)', 'Nombre Comuna']
col_rename = {
    'Código Vigente': 'IdEstablecimiento',
    'Nombre Oficial': 'nombre_establecimiento',
    'Nombre Dependencia Jerárquica (SEREMI / Servicio de Salud)': 'servicio_salud',
    'Nombre Comuna': 'comuna'
}
df_est = pd.read_excel('Establecimientos DEIS MINSAL 28-05-2024 (1).xlsx', skiprows=1, usecols=col_est)
df_est = df_est.rename(columns=col_rename)
df_ms3b = df_ms.loc[df_ms.MetaSanitaria == 'MSIIIb']
df_ms3b = df_ms3b.merge(df_est, on='IdEstablecimiento', how='left')

# Preparar los datos
df_ms3b = df_ms3b.dropna(subset=['Ano', 'Mes'])
df_ms3b['Ano'] = df_ms3b['Ano'].astype(int)
df_ms3b['Mes'] = df_ms3b['Mes'].astype(int)
df_ms3b['Porcentaje'] = df_ms3b['Numerador'] / df_ms3b['Denominador']
df_ms3b['IdEstablecimiento'] = df_ms3b['IdEstablecimiento'].astype(str)
df_ms3b['nombre_establecimiento'] = df_ms3b['nombre_establecimiento'].astype(str)
df_ms3b['codigo_nombre'] = df_ms3b['IdEstablecimiento'] + ' - ' + df_ms3b['nombre_establecimiento']

# Agrupar por IdEstablecimiento, sumar Numerador y calcular promedio de Denominador
df_grouped = df_ms3b.groupby('IdEstablecimiento').agg({
    'Numerador': 'sum',
    'Denominador': 'mean',
    'servicio_salud': 'first',
    'nombre_establecimiento': 'first',
    'comuna': 'first'
}).reset_index()

# Recalcular el porcentaje
df_grouped['Porcentaje'] = df_grouped['Numerador'] / df_grouped['Denominador']
df_grouped['codigo_nombre'] = df_grouped['IdEstablecimiento'] + ' - ' + df_grouped['nombre_establecimiento']

# Título del dashboard
st.title('Meta III.B: Niños y niñas de 6 años libres de caries')

st.subheader("Filtros")
all_servicios = ['Todos los Servicio de Salud', 'Servicio de Salud Metropolitano Norte',
                 'Servicio de Salud Metropolitano Occidente', 'Servicio de Salud Metropolitano Central',
                 'Servicio de Salud Metropolitano Sur', 'Servicio de Salud Metropolitano Oriente',
                 'Servicio de Salud Metropolitano Sur Oriente']
selected_servicios = st.selectbox('Seleccione Servicios de Salud', all_servicios, index=0)

# Filtrar el DataFrame según el Servicio de Salud seleccionado
if 'Todos los Servicio de Salud' in selected_servicios:
    df_filtered = df_grouped
else:
    df_filtered = df_grouped[df_grouped['servicio_salud'] == selected_servicios]

# Actualizar la lista de comunas basándose en el filtro de servicios de salud
all_comunas = ['Todas'] + sorted(list(df_filtered['comuna'].unique()))
selected_comunas = st.multiselect('Seleccione Comunas', all_comunas, default='Todas')

# Filtrar el DataFrame según las Comunas seleccionadas
if 'Todas' not in selected_comunas:
    df_filtered = df_filtered[df_filtered['comuna'].isin(selected_comunas)]

# Actualizar la lista de establecimientos basándose en los filtros anteriores
all_establecimientos = ['Todos'] + sorted(list(df_filtered['codigo_nombre'].unique()))
selected_establecimientos = st.multiselect('Seleccione Establecimientos', all_establecimientos, default='Todos')

# Filtrar el DataFrame según los Establecimientos seleccionados
if 'Todos' not in selected_establecimientos:
    df_filtered = df_filtered[df_filtered['codigo_nombre'].isin(selected_establecimientos)]

#%%
# Mostrar datos filtrados
st.write("## Datos para la Meta Sanitaria")
st.write("Fecha de corte de datos: _Octubre del 2024_")

# Información de resumen
num_services = df_filtered['servicio_salud'].nunique()
num_communes = df_filtered['comuna'].nunique()
num_establishments = df_filtered['codigo_nombre'].nunique()

# Dividir las métricas en 3 columnas
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label='N° Servicios de Salud', value=num_services)
with col2:
    st.metric(label='N° de comunas', value=num_communes)
with col3:
    st.metric(label='N° de establecimientos', value=num_establishments)

# Mostrar dataframe
col_ms3b = ['IdEstablecimiento', 'nombre_establecimiento', 'servicio_salud', 'comuna', 'Numerador', 'Denominador', 'Porcentaje']
rename_ms3b = {
    'IdEstablecimiento': 'ID Establecimiento',
    'nombre_establecimiento': 'Nombre del establecimiento',
    'servicio_salud': 'Servicio de Salud',
    'comuna': 'Comuna',
    'Numerador': 'Numerador',
    'Denominador': 'Denominador',
    'Porcentaje': 'Cumplimiento de la MS'
}
st.write(df_filtered[col_ms3b].rename(columns=rename_ms3b))


#%%
# DATOS CUMPLIMIENTO y GRAFICO GAUGE
st.subheader("Cumplimiento de la Meta Sanitaria")

# Calcular el porcentaje de cumplimiento total
total_numerador = df_filtered['Numerador'].sum()
total_denominador = df_filtered['Denominador'].sum()
total_porcentaje = total_numerador / total_denominador
meta_nacional = 0.16
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
    title={'text': 'Cumplimiento Total General'},
    gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "blue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 16], 'color': "gray"},
                {'range': [16, 100], 'color': "lightgray"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': total_porcentaje * 100
            },
            'shape': "angular"}
))
st.plotly_chart(fig)

#%%
# GRAFICO POR COMUNAS
## Crear un DataFrame con el nombre de la comuna, denominador, numerador y porcentaje de cumplimiento
df_cumplimiento = df_filtered.groupby('comuna').agg(
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
    y0=15,
    x1=len(df_cumplimiento['comuna']) - 1,
    y1=15,
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