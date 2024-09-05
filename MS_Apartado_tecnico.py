import streamlit as st

st.title("Apartado Técnico")

# Meta 1
st.header("Meta 1")
st.markdown("""
| **Numerador**   | **REM-A03**                                      | **SECCIÓN A.2**                                                               | **Celdas**                                            | **Código Prestación** | **Columnas**                   |
| --------------- | ------------------------------------------------ | ----------------------------------------------------------------------------- | ----------------------------------------------------- | --------------------- | ------------------------------ |
|                 | APLICACIÓN Y RESULTADOS DE ESCALAS DE EVALUACIÓN | RESULTADOS DE LA APLICACIÓN DE ESCALA DE EVALUACIÓN DEL DESARROLLO PSICOMOTOR | J25+, K25+, L25+, M25+, J27+, K27+, L27+, M27+        | 02010420, 03500366    | col08+, col09+, col10+, col11+ |
| **Denominador** | **REM-A03**                                      | **SECCIÓN A.2**                                                               | **Celdas**                                            | **Código Prestación** | **Columnas**                   |
|                 | APLICACIÓN Y RESULTADOS DE ESCALAS DE EVALUACIÓN | RESULTADOS DE LA APLICACIÓN DE ESCALA DE EVALUACIÓN DEL DESARROLLO PSICOMOTOR | J22+, K22+, L22+, M22+ (menos) J39+, K39+, L39+, M39+ | 02010321, 03500334    | col08+, col09+, col10+, col11+ |
""")

# Meta 2
st.header("Meta 2")
st.markdown("""
| **Numerador**   | **REM-P12**                                                    | **SECCIÓN A**                                                                                                              | **Celdas**                                     | **Código Prestación**                            | **Columnas** |
| --------------- | -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- | ------------------------------------------------ | ------------ |
|                 |                                                                | PROGRAMA DE CÁNCER DE CUELLO UTERINO: POBLACIÓN CON TAMIZAJE VIGENTE PARA LA DETECCIÓN PRECOZ DEL CÁNCER DE CUELLO UTERINO | B11+, B12+, B13+, B14+, B15+, B16+, B17+, B18+ | P1206020, P1206030, P1206050, P1206070, P1206080 | col01        |
| **Denominador** | **Población FONASA**                                           |                                                                                                                            |                                                |                                                  |              |
|                 | Inscrita y validada comprometida:<br>*Mujeres de 25 a 65 años* |                                                                                                                            |                                                |                                                  |              |
""")

# Meta 3A
st.header("Meta 3A")
st.markdown("""
| Numerador       | REM-A03                                          | SECCIÓN D.7                                                                              | Celdas                                                                                                                                                                                                                                                                                 | Código Prestación  | Columnas                                                                                                                                                       |
| --------------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|                 | APLICACIÓN Y RESULTADOS DE ESCALAS DE EVALUACIÓN | APLICACIÓN Y RESULTADOS DE PAUTA DE EVALUACIÓN CON ENFOQUE DE RIESGO ODONTOLÓGICO (CERO) | F204+, G204+, H204+, I204+, J204+, K204+, L204+, M204+, N204+, O204+, P204+, Q204+, R204+, S204+, T204+, U204+, V204+, W204+, X204+, Y204+, F205+, G205+, H205+, I205+, J205+, K205+, L205+, M205+, N205+, O205+, P205+, Q205+, R205+, S205+, T205+, U205+, V205+, W205+, X205+, Y205+ | 03500364, 03500365 | col04+, col05+, col06+, col07+, col08+, col09+, col10+, col11+, col12+, col13+, col14+, col15+, col16+, col17+, col18+, col19+, col20+, col21+, col22+, col23+ |
| **Denominador** | **Población FONASA**                             |                                                                                          |                                                                                                                                                                                                                                                                                        |                    |                                                                                                                                                                |
|                 | Inscrita y validada, de 0 a 9 años               |                                                                                          |                                                                                                                                                                                                                                                                                        |                    |                                                                                                                                                                |
""")

# Meta 3B
st.header("Meta 3B")
st.markdown("""
| Numerador       | REM-A09                                       | SECCIÓN C                 | Celdas     | Código Prestación | Columnas       |
| --------------- | --------------------------------------------- | ------------------------- | ---------- | ----------------- | -------------- |
|                 | ATENCIÓN DE SALUD BUCAL EN LA RED ASISTENCIAL | INGRESOS Y EGRESOS EN APS | S48+, T48+ | 09220100          | col16+, col17+ |
| **Denominador** | **Población FONASA**                          |                           |            |                   |                |
|                 | Inscrita y validada, de 6 años                |                           |            |                   |                |
""")

# Meta 4A
st.header("Meta 4A")
st.markdown("""
| Numerador       | REM P4                                                                                                                                                       | SECCIÓN B             | Celdas     | Código Prestación  | Columnas |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------- | ---------- | ------------------ | -------- |
|                 | POBLACIÓN EN CONTROL PROGRAMA DE SALUD CARDIOVASCULAR (PSCV)                                                                                                 | METAS DE COMPENSACIÓN | C36+, C37+ | P4180300, P4200200 | col01    |
| **Denominador** | **Población FONASA**                                                                                                                                         |                       |            |                    |          |
|                 | Inscrita y validada según prevalencia:<br>(de 15 a 24 años x 1,80%) + (de 25 a 44 años x 6,30%) + (de 45 a 64 años x 18,30%) + (de 65 años y más x 30,60%) + |                       |            |                    |          |
""")

# Meta 4B
st.header("Meta 4B")
st.markdown("""
| Numerador       | REM P4                                                       | SECCIÓN C                                  | Celdas                 | Código Prestación                      | Columnas     |
| --------------- | ------------------------------------------------------------ | ------------------------------------------ | ---------------------- | -------------------------------------- | ------------ |
|                 | POBLACIÓN EN CONTROL PROGRAMA DE SALUD CARDIOVASCULAR (PSCV) | VARIABLES DE SEGUIMIENTO DEL PSCV AL CORTE | C61+, C62+, C63+, C64+ | P4190809, P4170300, P4190500, P4190600 | col01        |
| **Denominador** | **REM P4**                                                   | **SECCIÓN A**                              | **Celdas**             | **Código Prestación**                  | **Columnas** |
|                 | POBLACIÓN EN CONTROL PROGRAMA DE SALUD CARDIOVASCULAR (PSCV) | PROGRAMA SALUD CARDIOVASCULAR (PSCV)       | C17                    | P4150602                               | col01        |
""")

# Meta 5
st.header("Meta 5")
st.markdown("""
| Numerador   | REM P4                                                                                                                                             | SECCIÓN B             | Celdas     | Código Prestación  | Columnas |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- | ---------- | ------------------ | -------- |
|             | POBLACIÓN EN CONTROL PROGRAMA DE SALUD CARDIOVASCULAR (PSCV)                                                                                       | METAS DE COMPENSACIÓN | C34+, C35+ | P4180200, P4200100 | col01    |
| Denominador | Población FONASA                                                                                                                                   |                       |            |                    |          |
|             | Inscrita y validada según prevalencia:<br>(de 15 a 24 años x 0,70%)+(de 25 a 44 años x 10,6%)+(de 45 a 64 años x 45,1%)+(de 65 años y más x 73,3%) |                       |            |                    |          |
""")

# Meta 6
st.header("Meta 6")
st.markdown("""
| Numerador       | REM-A03                                          | SECCIÓN A.5                            | Celdas     | Código Prestación     | Columnas     |
| --------------- | ------------------------------------------------ | -------------------------------------- | ---------- | --------------------- | ------------ |
|                 | APLICACIÓN Y RESULTADOS DE ESCALAS DE EVALUACIÓN | LACTANCIA EN NIÑOS Y NIÑAS CONTROLADOS | G60        | A0200002              | col06        |
| **Denominador** | **REM-A03**                                      | **SECCIÓN A.5**                        | **Celdas** | **Código Prestación** | **Columnas** |
|                 | APLICACIÓN Y RESULTADOS DE ESCALAS DE EVALUACIÓN | LACTANCIA EN NIÑOS Y NIÑAS CONTROLADOS | G66        | A0200001              | col06        |
""")

# Meta 7
st.header("Meta 7")
st.markdown("""
| Numerador       | REM P3.                                                                                     | SECCIÓN D                                          | Celdas                                                                                                                                                                                                       | Código Prestación              | Columnas                                                                                                                                                                                                                                                                              |
| --------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|                 | POBLACIÓN EN CONTROL OTROS PROGRAMAS                                                        | NIVEL DE CONTROL DE POBLACIÓN RESPIRATORIA CRÓNICA | Asma: H59+, I59+, J59+, K59+, L59+, M59+, N59+, O59+, P59+, Q59+, S59+, T59+, U59+, V59+, W59+, X59+, Y59+, Z59+, AA59+, AB59+, AD59+, AE59+, AF59+, AG59+, AH59+, AI59+, AJ59+, AL59+, AM59+ <br> EPOC: C63 | Asma: P3161041, EPOC: P3161043 | Asma: col06+, col07+, col08+, col09+, col10+, col11+, col12+, col13+, col14+, col15+, col16+, col17+, col18+, col19+, col20+, col21+, col22+, col23+, col24+, col25+, col26+, col27+, col28+, col29+, col30+, col31+, col32+, col33+, col34+, col35+, col36+, col37+ <br> EPOC: col01 |
| **Denominador** | **Población FONASA**                                                                        |                                                    |                                                                                                                                                                                                              |                                |                                                                                                                                                                                                                                                                                       |
|                 | Inscrita y validada según prevalencia: (de 40 y más años x 11,7%)+(de 5 y más años x 10,0%) |                                                    |                                                                                                                                                                                                              |                                |                                                                                                                                                                                                                                                                                       |
""")


# Sección para mostrar el enlace del PDF
st.header("Orientaciones tecnicas Metas Sanitarias 2024 de la ley 19.813")

# Ruta del archivo PDF
pdf_path = "DOC/OOTT Metas Sanitarias 2024 APS.pdf"

# Cargar el PDF y crear un enlace de descarga
with open(pdf_path, "rb") as file:
    pdf_data = file.read()
    # Crear el enlace para descargar el PDF
    st.download_button(label="Descargar o ver el PDF", data=pdf_data, file_name="Metas_Sanitarias_2024_APS.pdf", mime="application/pdf")