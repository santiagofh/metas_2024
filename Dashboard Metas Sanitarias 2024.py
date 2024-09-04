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
    st.Page("MSI.py", title="Meta I: Recuperación del desarrollo psicomotor", icon=":material/public:"),
    st.Page('MSII.py', title="Meta II: Detección precoz del cáncer de cuello uterino", icon=":material/public:"),
    st.Page('MSIIIa.py', title="Meta III-a: Protección de la salud bucal en población infatil - Control con enfoque de riesgo odontológico en población de 0 a 9 años", icon=":material/public:"),
    st.Page('MSIIIb.py', title="Meta III-b: Niños y niñas de 6 años libres de caries", icon=":material/public:"),
    st.Page('MSIVa.py', title="Meta IV-a: Cobertura efectiva de diabetes tipo 2 (DM2) en personas de 15 años y más", icon=":material/public:"),
    st.Page('MSIVb.py', title="Meta IV-b: Niños y niñas de 6 años libres de caries", icon=":material/public:"),
    st.Page('MSV.py', title="Meta V: Cobertura de tratamiento en personas de 15 años y más con hipertensión", icon=":material/public:"),
    st.Page('MSVI.py', title="Meta VI: Lactancia materna exclusiva (LME) en niños y niñas al sexto mes de vida", icon=":material/public:"),
    st.Page('MSVII.py', title="Meta VII: Cobertura de tratamiento en personas con asma y EPOC", icon=":material/public:")

],
"Recursos" : [
    st.Page("MS_Apartado_tecnico.py", title="Fuentes y archivos", icon=":material/description:")
]
}
pg = st.navigation(pages)
pg.run()