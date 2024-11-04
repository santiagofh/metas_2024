import streamlit as st

import streamlit as st

# Título de la pantalla de bienvenida
def home():
    st.title('Bienvenidos al Dashboard de Metas Sanitarias')

    # Subtítulo
    st.subheader('Sistema integral para el seguimiento y control de las metas sanitarias')

    # Descripción
    st.write("""
    Este dashboard está diseñado para proporcionar una visión completa y detallada de las metas sanitarias en las diversas áreas de salud pública.

    - Consultar el cumplimiento de las metas sanitarias por Servicio de salud, Comuna y Establecimiento de salud.
    - Ver gráficos y tablas detalladas que muestran el progreso y los indicadores de las metas sanitarias.
    """)
    # Descripción adicional
    st.write(""" comprometidos a proporcionar información precisa y actualizada para apoyar la toma de decisiones en el ámbito de la salud pública.""")

pages = {
"Menu principal":[
    st.Page(home, default=True, title="Pagina de inicio", icon=":material/home:")
],
"Metas Sanitarias" : [
    st.Page("MSI.py", title="Meta I: Recuperación del Desarrollo Psicomotor", icon=":material/public:"),
    st.Page('MSII.py', title="Meta II: Detección precoz del cáncer de cuello uterino", icon=":material/public:"),
    st.Page('MSIIIa.py', title="Meta III.A: Control con Enfoque de Riesgo odontológico en población de 0 a 9 años", icon=":material/public:"),
    st.Page('MSIIIb.py', title="Meta III.B: Niños y niñas de 6 años libres de caries", icon=":material/public:"),
    st.Page('MSIVa.py', title="Meta IV.A: Cobertura efectiva de tratamiento de DM2 en personas de 15 y más años", icon=":material/public:"),
    st.Page('MSIVb.py', title="Meta IV.B: Evaluación anual del pie diabético en personas de 15 años y más", icon=":material/public:"),
    st.Page('MSV.py', title="Meta V: Cobertura de tratamiento en personas con HTA", icon=":material/public:"),
    st.Page('MSVI.py', title="Meta VI: Prevalencia de Lactancia Materna Exclusiva (LME) en menores de 6 meses de vida", icon=":material/public:"),
    st.Page('MSVII.py', title="Meta VII: Cobertura efectiva de tratamiento en enfermedades respiratorias crónicas (asma y EPOC) en personas de 5 años y más", icon=":material/public:")

],
"Recursos" : [
    st.Page("MS_Apartado_tecnico.py", title="Apartado Tecnico", icon=":material/description:")
]
}
pg = st.navigation(pages)
pg.run()