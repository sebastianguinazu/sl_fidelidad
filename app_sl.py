from vega_datasets import data
import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import pickle
import plotly.express as px


# seteo la barra del costado

st.sidebar.header('Elija el monitor')
page = st.sidebar.selectbox('Distribucion de los puntajes', ["Homepage", "General", "Tipo de socio", \
    "Grupo etario", "Genero", "Socio cancha", "Descargar csv"])

st.sidebar.header('Elija puntajes')
patrimonial = st.sidebar.slider("Patrimonial pts:", 0, 2000, 2000, 100, '%d')
refundador = st.sidebar.slider("Refundador pts", 0, 2000, 1500, 100, '%d')
debito = st.sidebar.slider("Debito pts", 0, 2000, 1000, 100, '%d')
ant_simple = st.sidebar.slider("Antiguedad Simple pts", 0, 1000, 250, 50, '%d')
ant_pleno = st.sidebar.slider("Antiguedad Pleno pts", 0, 1000, 350, 50, '%d')
ant_interior = st.sidebar.slider("Antiguedad Interior pts", 0, 1000, 350, 50, '%d')
ant_exterior = st.sidebar.slider("Antiguedad Exterior pts", 0, 1000, 500, 50, '%d')
ant_vitalic = st.sidebar.slider("Antiguedad Vitalicio pts", 0, 1000, 350, 50, '%d')
abo_bidegain = st.sidebar.slider("Abono Bidegain pts", 0, 2000, 1000, 100, '%d')
abo_polideportivo = st.sidebar.slider("Abono Polideportivo pts", 0, 2000, 500, 100, '%d')
# vita_abonando = st.sidebar.slider("Vitalicio cuota pts", 0, 2000, 25, 100, '%d')
# cuota_dia_aspo = st.sidebar.slider("Cuota al dia ASPO pts", 0, 2000, 1000, 100, '%d')
eve_bid_amba = st.sidebar.slider("Bidegain Ingreso AMBA pts", 0, 500, 50, 25, '%d')
eve_bid_inte = st.sidebar.slider("Bidegain Ingreso Interior pts", 0, 500, 75, 25, '%d')
# eve_pol_amba = st.sidebar.slider("Polideportivo Ingreso AMBA pts", 0, 500, 50, 25, '%d')
# eve_pol_inte = st.sidebar.slider("Polideportivo Ingreso Interior pts", 0, 500, 75, 25, '%d')


# setel el contenido de las paginas

def main():

    df = load_datasets()

    if st.sidebar.button('Calcular'):
        df = calc_puntos(df)

    # if st.sidebar.button('Entrenar'):
    
    if page == "Homepage":
    	st.image('helpers/sl_cabecera.PNG')
    	st.title("Simulador de puntos de Fidelidad")
    	st.markdown("> Por Sebastian Guinazu (Socio Nro 29873)")
    	st.markdown("Esta app se construyo con el objetivo de poder simular el puntaje de fidelidad de \
            los socios San Lorenzo. En la barra de la izquierda se pueden elegir los puntajes de los \
            distintos items. Tambien se pueden seleccionar diferentes monitores para analizar la distribucion\
            de los puntajes en distintas categorias")
    	st.markdown("")
    	st.markdown("## **Para usar la app siga los siguientes pasos:**")
    	st.markdown("")
    	st.markdown("### 🎯 Primero defina los **puntajes** para cada item en la barra de la izquierda")
    	st.markdown("### ⏩ Luego precione el boton **Calcular** abajo de todo")
    	st.markdown("### 📊 En el menu de la izquierda puede seleccionar los **Monitores** disponibles")

    elif page == "General":
        st.title("Puntos de fidelidad")
        st.markdown("")
        st.markdown("### Estadisticos de la distribucion de los puntos")
        st.markdown("")
        st.write(f"- El promedio de los puntos es {round(df['puntos'].mean())}")
        st.write(f"- El valor de la mediana (donde se acumula el 50%) es de \
            {round(df.puntos.describe()[5])}")
        st.write(f"- El valor maximo es de \
            {round(df.puntos.describe()[7])}")

        st.markdown("### Grafico de la distribucion")
        if st.button('Mostrar'):
            fig = px.histogram(df, x="puntos", nbins=20, labels={"puntos":'Puntos de fidelidad', 'count':'# Socios'}).update_layout(yaxis_title="# Socios")
            st.plotly_chart(fig, use_container_width=True)

    elif page == "Tipo de socio":
        st.title("Puntos de fidelidad por Tipo de Socio")
        st.markdown("")
        st.markdown("En este monitor se pueden analizar la distribucion de los puntos por categoria de socios. ")
        st.markdown("### Estadisticos de la distribucion de los puntos por tipo de socio")
        st.write(f"- Los socios **vitalicios** son el {round(df[df['tipo_socio']=='VITALICIO'].shape[0]/df.shape[0]*100)}%. \
            Su promedio de pts de fidelidad queda en  {round(df.loc[df['tipo_socio']=='VITALICIO', 'puntos'].mean())}\
            y la mediana  {round(df.loc[df['tipo_socio']=='VITALICIO', 'puntos'].describe()[5])}")
        st.write(f"- Los socios **simples** son el {round(df[df['tipo_socio']=='SIMPLE'].shape[0]/df.shape[0]*100)}%. \
            Su promedio de pts de fidelidad queda en {round(df.loc[df['tipo_socio']=='SIMPLE', 'puntos'].mean())}\
            y la mediana {round(df.loc[df['tipo_socio']=='SIMPLE', 'puntos'].describe()[5])}")
        st.write(f"- Los socios **plenos** son el {round(df[df['tipo_socio']=='PLENO'].shape[0]/df.shape[0]*100)}%. \
            Su promedio de pts de fidelidad queda en {round(df.loc[df['tipo_socio']=='PLENO', 'puntos'].mean())}\
            y la mediana {round(df.loc[df['tipo_socio']=='PLENO', 'puntos'].describe()[5])}")
        st.write(f"- Los socios del **interior** son el {round(df[df['tipo_socio']=='INTERIOR'].shape[0]/df.shape[0]*100)}%. \
            Su promedio de pts de fidelidad queda en {round(df.loc[df['tipo_socio']=='INTERIOR', 'puntos'].mean())}\
            y la mediana es {round(df.loc[df['tipo_socio']=='INTERIOR', 'puntos'].describe()[5])}")
        # st.write(f"- El promedio de los socios del **exterior** es {round(df.loc[df['tipo_socio']=='EXTERIOR', 'puntos'].mean())}\
        #     la mediana es {round(df.loc[df['tipo_socio']=='EXTERIOR', 'puntos'].describe()[5])}")

        st.markdown("### Grafico de la distribucion")
        if st.button('Mostrar'):
            fig = px.box(df, x="tipo_socio", y="puntos", color="tipo_socio", color_discrete_sequence=["blue", "red", "blue", "red", "blue", "red"], \
                labels={"puntos":'Puntos de fidelidad', 'tipo_socio':'Tipo de socio'})
            st.plotly_chart(fig, use_container_width=True)

    elif page == "Grupo etario":
        st.title("Puntos de fidelidad por Grupo Etario")
        st.markdown("")
        st.markdown("En este monitor se pueden analizar la distribucion de los puntos por el grupo etario de los socios. ")
        st.markdown("### Estadisticos de la distribucion de los puntos por grupo etario")
        st.write(f"- Los socios **mayores a 60** son el {round(df[df['grupo_etario']=='Mayor a 60'].shape[0]/df.shape[0]*100)}%. \
            Su promedio de pts de fidelidad queda en  {round(df.loc[df['grupo_etario']=='Mayor a 60', 'puntos'].mean())}\
            y la mediana  {round(df.loc[df['grupo_etario']=='Mayor a 60', 'puntos'].describe()[5])}")
        st.write(f"- Los socios **entre 45 y 59** son el {round(df[df['grupo_etario']=='Entre 45 y 59'].shape[0]/df.shape[0]*100)}%. \
            Su promedio de pts de fidelidad queda en {round(df.loc[df['grupo_etario']=='Entre 45 y 59', 'puntos'].mean())}\
            y la mediana {round(df.loc[df['grupo_etario']=='Entre 45 y 59', 'puntos'].describe()[5])}")
        st.write(f"- Los socios **entre 30 y 44** son el {round(df[df['grupo_etario']=='Entre 30 y 44'].shape[0]/df.shape[0]*100)}%. \
            Su promedio de pts de fidelidad queda en {round(df.loc[df['grupo_etario']=='Entre 30 y 44', 'puntos'].mean())}\
            y la mediana {round(df.loc[df['grupo_etario']=='Entre 30 y 44', 'puntos'].describe()[5])}")
        st.write(f"- Los socios **entre 18 y 29** son el {round(df[df['grupo_etario']=='Entre 18 y 29'].shape[0]/df.shape[0]*100)}%. \
            Su promedio de pts de fidelidad queda en {round(df.loc[df['grupo_etario']=='Entre 18 y 29', 'puntos'].mean())}\
            y la mediana es {round(df.loc[df['grupo_etario']=='Entre 18 y 29', 'puntos'].describe()[5])}")
        st.write(f"- Los socios **menores a 18** son el {round(df[df['grupo_etario']=='Menores a 18'].shape[0]/df.shape[0]*100)}%. \
            Su promedio de pts de fidelidad queda en {round(df.loc[df['grupo_etario']=='Menores a 18', 'puntos'].mean())}\
            y la mediana es {round(df.loc[df['grupo_etario']=='Menores a 18', 'puntos'].describe()[5])}")

        st.markdown("### Grafico de la distribucion")
        if st.button('Mostrar'):
            fig = px.box(df[~df['edad'].isna()], x="grupo_etario", y="puntos", color="grupo_etario", color_discrete_sequence=["blue", "red", "blue", "red", "blue"], \
                labels={"puntos":'Puntos de fidelidad', 'grupo_etario':'Grupo etario'})
            st.plotly_chart(fig, use_container_width=True)

    elif page == "Genero":
        st.title("Puntos de fidelidad por Genero")
        st.markdown("")
        st.markdown("En este monitor se pueden analizar la distribucion de los puntos por genero.")
        st.markdown("### Estadisticos de la distribucion de los puntos por genero")
        st.write(f"- Las **socias** son el {round(df[df['sexo']=='F'].shape[0]/df.shape[0]*100)}%. \
            Su promedio de pts de fidelidad queda en  {round(df.loc[df['sexo']=='F', 'puntos'].mean())}\
            y la mediana  {round(df.loc[df['sexo']=='F', 'puntos'].describe()[5])}")
        st.write(f"- Los **socios** son el {round(df[df['sexo']=='M'].shape[0]/df.shape[0]*100)}%. \
            Su promedio de pts de fidelidad queda en  {round(df.loc[df['sexo']=='M', 'puntos'].mean())}\
            y la mediana  {round(df.loc[df['sexo']=='M', 'puntos'].describe()[5])}")

        if st.button('Mostrar'):
            fig = px.box(df[~df['edad'].isna()], x="sexo", y="puntos", color="sexo", color_discrete_sequence=["blue", "red"], \
                labels={"puntos":'Puntos de fidelidad', 'sexo':'Genero'})
            st.plotly_chart(fig)

    elif page == "Socio cancha":
        st.title("Detalle de los socios que van a la cancha")
        st.markdown("")
        st.markdown("En este monitor se pueden analizar la distribucion de los puntos por asistencia a partidos. ")
        st.markdown("### Estadisticos de la distribucion de los puntos por asistencia a partidos")
        st.write(f"- Los socios que no asistieron a **ningun partido** son el {round(df[df['partidos']=='Ninguno'].shape[0]/df.shape[0]*100)}%. \
            Su promedio de pts de fidelidad queda en  {round(df.loc[df['partidos']=='Ninguno', 'puntos'].mean())}\
            y la mediana  {round(df.loc[df['partidos']=='Ninguno', 'puntos'].describe()[5])}")
        st.write(f"- Los socios que asistieron **entre 1 y 4 partidos** son el {round(df[df['partidos']=='Entre 1 y 4'].shape[0]/df.shape[0]*100)}%. \
            Su promedio de pts de fidelidad queda en {round(df.loc[df['partidos']=='Entre 1 y 4', 'puntos'].mean())}\
            y la mediana {round(df.loc[df['partidos']=='Entre 1 y 4', 'puntos'].describe()[5])}")
        st.write(f"- Los socios que asistieron **entre 5 y 9 partidos** son el {round(df[df['partidos']=='Entre 5 y 9'].shape[0]/df.shape[0]*100)}%. \
            Su promedio de pts de fidelidad queda en {round(df.loc[df['partidos']=='Entre 5 y 9', 'puntos'].mean())}\
            y la mediana {round(df.loc[df['partidos']=='Entre 5 y 9', 'puntos'].describe()[5])}")
        st.write(f"- Los socios que asistieron a **mas de 10 partidos ** son el {round(df[df['partidos']=='Mas de 10'].shape[0]/df.shape[0]*100)}%. \
            Su promedio de pts de fidelidad queda en {round(df.loc[df['partidos']=='Mas de 10', 'puntos'].mean())}\
            y la mediana es {round(df.loc[df['partidos']=='Mas de 10', 'puntos'].describe()[5])}")

        st.markdown("### Grafico de la distribucion")
        if st.button('Mostrar'):
            fig = px.box(df, x="partidos", y="puntos", color="partidos", color_discrete_sequence=["blue", "red", "blue", "red", "blue", "red"], \
                labels={"puntos":'Puntos de fidelidad', 'partidos':'Partidos'},
                category_orders={"partidos": ["Ninguno", "Entre 1 y 4", "Entre 5 y 9", "Mas de 10"]})
            st.plotly_chart(fig, use_container_width=True)

    elif page == "Descargar csv":
        st.title("Descargar csv filtrado")
        st.markdown("")
        st.markdown("En este monitor se pueden fijar ciertos filtros para descargar el csv con la info de los socios. \
            Una vez que estan definidos, tocar le boton 'aplicar filtros', luego, ir abajo y tocar 'Descargar csv file'.")
        filtros=st.button('Aplicar filtros')

        filtro_edad_min = st.number_input('Edad min', min_value=0, max_value=100, value=18)
        filtro_edad_max = st.number_input('Edad max', min_value=0, max_value=100, value=70)
        filtro_tiposocio = st.selectbox('Tipo de socio', (['TODOS'] + list(df['tipo_socio'].unique())))
        filtro_sexo = st.selectbox('Sexo', (['TODOS'] + list(df['sexo'].unique())))
        filtro_partidos = st.selectbox('Partidos asistidos', (['TODOS'] + list(df['partidos'].unique())))
        filtro_debito = st.selectbox('Forma de pago', (['TODOS'] + list(df['forma_pago'].unique())))
        filtro_antig_min = st.number_input('Antiguedad min', min_value=0, max_value=50, value=0)
        filtro_antig_max = st.number_input('Antiguedad max', min_value=0, max_value=50, value=50)
        # refundador
        # abonos

        if filtros:
            'Se aplicaron los filtros'
            import base64
            df_download = df
            df_download = df_download[df_download.edad >= filtro_edad_min]
            df_download = df_download[df_download.edad <= filtro_edad_max]
            if filtro_tiposocio != 'TODOS':
                df_download = df_download[df_download['tipo_socio'] == filtro_tiposocio]
            if filtro_sexo != 'TODOS':
                df_download = df_download[df_download['sexo'] == filtro_sexo]
            if filtro_partidos != 'TODOS':
                df_download = df_download[df_download['partidos'] == filtro_partidos]
            if filtro_debito != 'TODOS':
                df_download = df_download[df_download['forma_pago'] == filtro_debito]
            df_download = df_download[df_download.antig >= filtro_antig_min]
            df_download = df_download[df_download.antig <= filtro_antig_max]

            csv = df_download.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # some strings
            linko= f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'
            st.markdown(linko, unsafe_allow_html=True)


# funciones

@st.cache(show_spinner=False, allow_output_mutation=True)
def load_datasets():
    df = pickle.load( open( "data/df_fide.p", "rb" ) )

    df['puntos'] = 0
    return df

def calc_puntos(df):
    df['puntos'] = 0

    df.loc[df['tipo_socio']=='PATRIMONIAL', 'puntos'] += patrimonial
    df.loc[df['refunda']==1, 'puntos'] += refundador
    df.loc[df['forma_pago']=='DEBITO', 'puntos'] += debito

    df.loc[df['tipo_socio']=='SIMPLE', 'puntos'] += df.loc[df['tipo_socio']=='SIMPLE', 'antig'] * ant_simple
    df.loc[df['tipo_socio']=='PLENO', 'puntos'] += df.loc[df['tipo_socio']=='PLENO', 'antig'] * ant_pleno
    df.loc[df['tipo_socio']=='INTERIOR', 'puntos'] += df.loc[df['tipo_socio']=='INTERIOR', 'antig'] * ant_interior
    df.loc[df['tipo_socio']=='EXTERIOR', 'puntos'] += df.loc[df['tipo_socio']=='EXTERIOR', 'antig'] * ant_exterior
    df.loc[df['tipo_socio']=='VITALICIO', 'puntos'] += df.loc[df['tipo_socio']=='VITALICIO', 'antig'] * ant_vitalic

    df['puntos'] += df['abo_bid_2020'] * abo_bidegain
    df['puntos'] += df['abo_bid_2021'] * abo_bidegain
    df['puntos'] += df['abo_pol_2020'] * abo_polideportivo
    df['puntos'] += df['abo_pol_2021'] * abo_polideportivo

    intext = (df['tipo_socio']=='INTERIOR') | (df['tipo_socio']=='EXTERIOR')
    df.loc[~intext, 'puntos'] += df.loc[~intext, 'eve_2018'] * eve_bid_amba
    df.loc[~intext, 'puntos'] += df.loc[~intext, 'eve_2019'] * eve_bid_amba
    df.loc[~intext, 'puntos'] += df.loc[~intext, 'eve_2020'] * eve_bid_amba
    df.loc[intext, 'puntos'] += df.loc[intext, 'eve_2018'] * eve_bid_inte
    df.loc[intext, 'puntos'] += df.loc[intext, 'eve_2019'] * eve_bid_inte
    df.loc[intext, 'puntos'] += df.loc[intext, 'eve_2020'] * eve_bid_inte

    return df


# formato

COLOR = "black"
BACKGROUND_COLOR = "#fff"

max_width = 1350
padding_top = 0
padding_bottom = 1
padding_right = 1
padding_left = 1

st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: {max_width}px;
        padding-top: {padding_top}rem;
        padding-right: {padding_right}rem;
        padding-left: {padding_left}rem;
        padding-bottom: {padding_bottom}rem;
    }}
    .reportview-container .main {{
        color: {COLOR};
        background-color: {BACKGROUND_COLOR};
    }}
</style>
""",
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()