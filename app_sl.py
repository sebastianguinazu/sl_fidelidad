from vega_datasets import data
import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
from datetime import datetime


def main():

    # df, eval = load_datasets()
    st.sidebar.header('Elija el monitor')
    page = st.sidebar.selectbox("Choose a page", ["Homepage", "Users", "Uso de la API", "Longitud de los mails"])

    st.sidebar.header('Elija puntajes')
    patrimonial = st.sidebar.slider("Patrimonial pts:", 0, 2000, 2000, 25, '%d')
    refundador = st.sidebar.slider("Refundador pts", 0, 2000, 1500, 25, '%d')
    debito = st.sidebar.slider("Debito pts", 0, 500, 25, 25, '%d')
    ant_simple = st.sidebar.slider("Antiguedad Simple pts", 0, 1000, 250, 25, '%d')
    ant_pleno = st.sidebar.slider("Antiguedad Pleno pts", 0, 1000, 350, 25, '%d')
    ant_interior = st.sidebar.slider("Antiguedad Interior pts", 0, 1000, 350, 25, '%d')
    ant_exterior = st.sidebar.slider("Antiguedad Exterior pts", 0, 1000, 500, 25, '%d')
    ant_vitalic = st.sidebar.slider("Antiguedad Vitalicio pts", 0, 1000, 350, 25, '%d')
    abo_bidegain = st.sidebar.slider("Abono Bidegain pts", 0, 2000, 1000, 25, '%d')
    abo_polideportivo = st.sidebar.slider("Abono Polideportivo pts", 0, 2000, 500, 25, '%d')
    vita_abonando = st.sidebar.slider("Vitalicio cuota pts", 0, 2000, 25, 25, '%d')
    cuota_dia_aspo = st.sidebar.slider("Cuota al dia ASPO pts", 0, 2000, 1000, 25, '%d')
    eve_bid_amba = st.sidebar.slider("Bidegain Ingreso AMBA pts", 0, 2000, 50, 25, '%d')
    eve_bid_inte = st.sidebar.slider("Bidegain Ingreso Interior pts", 0, 2000, 75, 25, '%d')
    eve_pol_amba = st.sidebar.slider("Polideportivo Ingreso AMBA pts", 0, 2000, 50, 25, '%d')
    eve_pol_inte = st.sidebar.slider("Polideportivo Ingreso Interior pts", 0, 2000, 75, 25, '%d')


    if page == "Homepage":
    	st.image('helpers/sl_cabecera.PNG')
    	st.title("💻 Simulador de puntos de Fidelidad")
    	st.markdown("> Para uso interno")
    	st.markdown("En el panel de la izquierda se pueden elegir los puntajes para cada item")
    	st.markdown("En el menu de la izquierda puede seleccionar los monitores disponibles")

    elif page == "Tipo de socio":
        st.title("Puntos de fidelidad por Tipo de Socio")

    elif page == "Grupo etario":
        st.title("Puntos de fidelidad por Grupo Etario")

    elif page == "Provincias":
        st.title("Puntos de fidelidad por Provincias")

    elif page == "Genero":
        st.title("Puntos de fidelidad por Genero")


@st.cache(show_spinner=False)
def load_datasets():
    df = pickle.load( open( "data/df_fide.p", "rb" ) )
    df['antig'] = [round((datetime.now() - x).days/365) for x in df['fecha_ingreso']]
    df['edad'] = [np.nan if pd.isnull(x) else round((datetime.now() - x).days/365) for x in df['fecha_nac']]
    return df

COLOR = "black"
BACKGROUND_COLOR = "#fff"

max_width = 1350
padding_top = 2
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