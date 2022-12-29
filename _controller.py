from dash import html, dcc
from app import app
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date

df_data = pd.read_csv("dataset/datatran2020.csv", index_col=0, sep=";")

estado_municipio = df_data[['uf', 'municipio']]
estados = estado_municipio['uf'].unique()
estados = estados.tolist()
estados.sort()

municipios = estado_municipio['municipio'].unique()
municipios = municipios.tolist()
municipios.sort()

lista = []


controller = dbc.Row([
    html.H2("Analise de acidentes", style={'text-align': 'center', 'margin-top': '30px'}),
    html.H4("2020", style={'text-align': 'center', 'font-weight': 'bold'}),
    dcc.Dropdown(
                id="estado_dropdown",
                options=[{"label": i, "value": i} for i in estados],
                value=0,
                placeholder="Selecione o estado",
                style={'margin-top': '20px'}
                ),
    dcc.Dropdown(
                id="cidade_dropdown",
                options=lista, 
                value=None,
                placeholder="Selecione a cidade",
                style={'margin-top': '10px'}
                ),
    html.Div([
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=date(2020, 1, 1),
        max_date_allowed=date(2020, 12, 31),
        initial_visible_month=date(2020, 1, 1),
        end_date=date(2020, 12, 31),
        style={'margin-top': '20px'}
    ),
    html.Div(id='output-container-date-picker-range')
])
   
])

