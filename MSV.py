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
df_ms5 = df_ms.loc[df_ms.MetaSanitaria == 'MSV']
df_ms5 = df_ms5.merge(df_est, on='IdEstablecimiento', how='left')
#%%
# Preparar los datos
df_ms5 = df_ms5.dropna(subset=['Ano', 'Mes'])
df_ms5['Ano'] = df_ms5['Ano'].astype(int)
df_ms5['Mes'] = df_ms5['Mes'].astype(int)
df_ms5['Porcentaje'] = df_ms5['Numerador']/df_ms5['Denominador']
df_ms5['IdEstablecimiento'] = df_ms5['IdEstablecimiento'].astype(str)
df_ms5['nombre_establecimiento'] = df_ms5['nombre_establecimiento'].astype(str)
df_ms5['codigo_nombre']=df_ms5['IdEstablecimiento']+' - '+df_ms5['nombre_establecimiento']
#%%

# Título del dashboard
st.title('Meta V: Cobertura de tratamiento en personas con HTA')

st.subheader("Filtros")
all_servicios = ['Todos los Servicio de Salud', 'Servicio de Salud Metropolitano Norte',
                 'Servicio de Salud Metropolitano Occidente', 'Servicio de Salud Metropolitano Central',
                 'Servicio de Salud Metropolitano Sur', 'Servicio de Salud Metropolitano Oriente',
                 'Servicio de Salud Metropolitano Sur Oriente']
selected_servicios = st.selectbox('Seleccione Servicios de Salud', all_servicios, index=0)

# Filtrar el DataFrame según el Servicio de Salud seleccionado
if 'Todos los Servicio de Salud' in selected_servicios:
    df_ms5_filtered = df_ms5
else:
    df_ms5_filtered = df_ms5[df_ms5['servicio_salud'] == selected_servicios]

# Actualizar la lista de comunas basándose en el filtro de servicios de salud
all_comunas = ['Todas'] + sorted(list(df_ms5_filtered['comuna'].unique()))
selected_comunas = st.multiselect('Seleccione Comunas', all_comunas, default='Todas')

# Filtrar el DataFrame según las Comunas seleccionadas
if 'Todas' not in selected_comunas:
    df_ms5_filtered = df_ms5_filtered[df_ms5_filtered['comuna'].isin(selected_comunas)]

# Actualizar la lista de establecimientos basándose en los filtros anteriores
all_establecimientos = ['Todos'] + sorted(list(df_ms5_filtered['codigo_nombre'].unique()))
selected_establecimientos = st.multiselect('Seleccione Establecimientos', all_establecimientos, default='Todos')

# Filtrar el DataFrame según los Establecimientos seleccionados
if 'Todos' not in selected_establecimientos:
    df_ms5_filtered = df_ms5_filtered[df_ms5_filtered['codigo_nombre'].isin(selected_establecimientos)]

# Meses de corte
all_meses = sorted(list(df_ms5_filtered['Mes'].unique()))
selected_meses = st.selectbox('Seleccione el mes de corte', all_meses, index=len(all_meses)-1)
df_ms5_filtered = df_ms5_filtered[df_ms5_filtered['Mes']==selected_meses]
#%%
# Mostrar datos filtrados
st.write("## Datos para la Meta Sanitaria")

st.write("Fecha de corte de datos: _Septiembre del 2024_")
# Información de resumen
num_services = df_ms5_filtered['servicio_salud'].nunique()
num_communes = df_ms5_filtered['comuna'].nunique()
num_establishments = df_ms5_filtered['codigo_nombre'].nunique()

# Dividir las métricas en 3 columnas
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label='N° Servicios de Salud', value=num_services)
with col2:
    st.metric(label='N° de comunas', value=num_communes)
with col3:
    st.metric(label='N° de establecimientos', value=num_establishments)
#%%
# Mostrar dataframe
col_ms4b=['Ano', 'Mes','codigo_nombre','servicio_salud',  'Numerador', 'Denominador','Porcentaje']
rename_ms4b={
    'Ano':'Año', 
    'Mes':'Mes',
    'codigo_nombre':'Nombre del establecimeinto',
    'servicio_salud':'Servicio de Salud',  
    'Numerador':'Numerador', 
    'Denominador':'Denominador',
    'Porcentaje':'Cumplimiento de la MS'
}
st.write(df_ms5_filtered[col_ms4b].rename(columns=rename_ms4b))

col_ms4b = ['IdEstablecimiento', 'nombre_establecimiento', 'servicio_salud', 'comuna', 'Numerador', 'Denominador', 'Porcentaje']


#%%
# DATOS CUMPLIMIENTO y GRAFICO GAUGE
st.subheader("Cumplimiento de la Meta Sanitaria")

# Calcular el porcentaje de cumplimiento total
total_numerador = df_ms5_filtered['Numerador'].sum()
total_denominador = df_ms5_filtered['Denominador'].sum()
total_porcentaje = (total_numerador / total_denominador)
meta_nacional = 0.45

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
                {'range': [0, 45], 'color': "gray"},
                {'range': [45, 100], 'color': "lightgray"}
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
df_cumplimiento = df_ms5_filtered.groupby('comuna').agg(
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