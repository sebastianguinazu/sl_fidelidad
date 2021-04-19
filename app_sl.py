from vega_datasets import data
import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
from datetime import datetime
import pickle
import plotly.express as px


# seteo la barra del costado

st.sidebar.header('Elija el monitor')
page = st.sidebar.selectbox('Distribucion de los puntajes', ["Homepage", "General", "Tipo de socio", \
    "Grupo etario", "Genero", "Valores altos"])

st.sidebar.header('Elija puntajes')
patrimonial = st.sidebar.slider("Patrimonial pts:", 0, 2000, 2000, 100, '%d')
refundador = st.sidebar.slider("Refundador pts", 0, 2000, 1500, 100, '%d')
debito = st.sidebar.slider("Debito pts", 0, 500, 25, 25, '%d')
ant_simple = st.sidebar.slider("Antiguedad Simple pts", 0, 1000, 250, 50, '%d')
ant_pleno = st.sidebar.slider("Antiguedad Pleno pts", 0, 1000, 350, 50, '%d')
ant_interior = st.sidebar.slider("Antiguedad Interior pts", 0, 1000, 350, 50, '%d')
ant_exterior = st.sidebar.slider("Antiguedad Exterior pts", 0, 1000, 500, 50, '%d')
ant_vitalic = st.sidebar.slider("Antiguedad Vitalicio pts", 0, 1000, 350, 50, '%d')
abo_bidegain = st.sidebar.slider("Abono Bidegain pts", 0, 2000, 1000, 100, '%d')
abo_polideportivo = st.sidebar.slider("Abono Polideportivo pts", 0, 2000, 500, 100, '%d')
# vita_abonando = st.sidebar.slider("Vitalicio cuota pts", 0, 2000, 25, 100, '%d')
# cuota_dia_aspo = st.sidebar.slider("Cuota al dia ASPO pts", 0, 2000, 1000, 100, '%d')
eve_bid_amba = st.sidebar.slider("Bidegain Ingreso AMBA pts", 0, 500, 50, 1, '%d')
eve_bid_inte = st.sidebar.slider("Bidegain Ingreso Interior pts", 0, 500, 75, 25, '%d')
eve_pol_amba = st.sidebar.slider("Polideportivo Ingreso AMBA pts", 0, 500, 50, 25, '%d')
eve_pol_inte = st.sidebar.slider("Polideportivo Ingreso Interior pts", 0, 500, 75, 25, '%d')


# setel el contenido de las paginas

def main():

    df_fide = load_datasets()

    if st.sidebar.button('Calcular'):
        df_fide = calc_puntos(df_fide)

    # if st.sidebar.button('Entrenar'):
    
    if page == "Homepage":
    	st.image('helpers/sl_cabecera.PNG')
    	st.title("Simulador de puntos de Fidelidad")
    	st.markdown("> Esta app se construyo con el objetivo de poder simular el puntaje de fidelidad de \
            los socios San Lorenzo. En la barra de la izquierda se pueden elegir los puntajes de los \
            distintos items. Tambien se pueden seleccionar distintos monitores para analizar la distribucion\
            de los puntajes en distintas categorias")
    	st.markdown("")
    	st.markdown("## **Para usar la app siga los siguientes pasos:**")
    	st.markdown("")
    	st.markdown("### 🎯 Primero defina los **puntajes** para cada item")
    	st.markdown("### ⏩  Luego precione el boton **Calcular**")
    	st.markdown("### 📊 En el menu de la izquierda puede seleccionar los **Monitores** disponibles")

    elif page == "General":
        st.title("Puntos de fidelidad")
        st.markdown("")
        st.markdown("### Estadisticos de la distribucion de los puntos")
        st.markdown("")
        st.write(f"- El promedio de los puntos es {round(df_fide['puntos'].mean())}")
        st.write(f"- El valor de la mediana (donde se acumula el 50%) es de \
            {round(df_fide.puntos.describe()[5])}")
        st.write(f"- El valor maximo es de \
            {round(df_fide.puntos.describe()[7])}")

        st.markdown("### Grafico de la distribucion")
        if st.button('Mostrar'):
            fig = px.histogram(df_fide, x="puntos", nbins=10, labels={"puntos":'Puntos de fidelidad', 'count':'# Socios'}).update_layout(yaxis_title="# Socios")
            st.plotly_chart(fig, use_container_width=True)

    elif page == "Tipo de socio":
        st.title("Puntos de fidelidad por Tipo de Socio")
        st.markdown("")
        st.write("En este monitor se pueden analizar la distribucion de los puntos por categoria de socios. ")
        st.markdown("### Estadisticos de la distribucion de los puntos por tipo de socio")
        st.write(f"- El promedio de los socios **vitalicios** es {round(df_fide.loc[df_fide['tipo_socio']=='VITALICIO', 'puntos'].mean())}\
            la mediana es {round(df_fide.loc[df_fide['tipo_socio']=='VITALICIO', 'puntos'].describe()[5])}")
        st.write(f"- El promedio de los socios **simples** es {round(df_fide.loc[df_fide['tipo_socio']=='SIMPLE', 'puntos'].mean())}\
            la mediana es {round(df_fide.loc[df_fide['tipo_socio']=='SIMPLE', 'puntos'].describe()[5])}")
        st.write(f"- El promedio de los socios **plenos** es {round(df_fide.loc[df_fide['tipo_socio']=='PLENO', 'puntos'].mean())}\
            la mediana es {round(df_fide.loc[df_fide['tipo_socio']=='PLENO', 'puntos'].describe()[5])}")
        st.write(f"- El promedio de los socios del **interior** es {round(df_fide.loc[df_fide['tipo_socio']=='INTERIOR', 'puntos'].mean())}\
            la mediana es {round(df_fide.loc[df_fide['tipo_socio']=='INTERIOR', 'puntos'].describe()[5])}")
        # st.write(f"- El promedio de los socios del **exterior** es {round(df_fide.loc[df_fide['tipo_socio']=='EXTERIOR', 'puntos'].mean())}\
        #     la mediana es {round(df_fide.loc[df_fide['tipo_socio']=='EXTERIOR', 'puntos'].describe()[5])}")

        st.markdown("### Grafico de la distribucion")
        if st.button('Mostrar'):
            fig = px.box(df_fide, x="tipo_socio", y="puntos", color="tipo_socio", color_discrete_sequence=["blue", "red", "blue", "red", "blue", "red"], \
                labels={"puntos":'Puntos de fidelidad', 'tipo_socio':'Tipo de socio'})
            st.plotly_chart(fig, use_container_width=True)

    elif page == "Grupo etario":
        st.title("Puntos de fidelidad por Grupo Etario")

    elif page == "Genero":
        st.title("Puntos de fidelidad por Genero")

    elif page == "Valores altos":
        st.title("Detalle de los valores mas altos")


# funciones

@st.cache(show_spinner=False, allow_output_mutation=True)
def load_datasets():
    df = pickle.load( open( "data/df_fide.p", "rb" ) )
    df['antig'] = [round((datetime.now() - x).days/365) for x in df['fecha_ingreso']]
    df['edad'] = [np.nan if pd.isnull(x) else round((datetime.now() - x).days/365) for x in df['fecha_nac']]
    df['puntos'] = 0
    df['pts_bin'] = 0
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

    df['pts_bin'] = pd.cut(df['puntos'], 10)
    df['pts_bin'] = [str(i) for i in df['pts_bin']]

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