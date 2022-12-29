from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px

from app import app
from _controller import *
from _map import *

#====================================
#Ingestão de dados
#====================================


df_data = pd.read_csv("dataset/datatran2020.csv", index_col=0, sep=";")
df_data['data'] = df_data['data_inversa'] + ' ' + df_data['horario']
df_data['data'] = pd.to_datetime(df_data['data'])

df_data['latitude'] = df_data['latitude'].apply(lambda x: x.replace(',', '.'))
df_data['longitude'] = df_data['longitude'].apply(lambda x: x.replace(',', '.'))

df_data['latitude'] = df_data['latitude'].apply(lambda x: float(x))
df_data['longitude'] = df_data['longitude'].apply(lambda x: float(x))

del df_data['horario']
del df_data['data_inversa']

centerLat = -8.50094
centerLong = -55.87449


app.layout = dbc.Container(
        children=[
                dbc.Row([
                    dbc.Col([controller], md=3 ),
                    dbc.Col([map_area], md=9)
                ]),
        ], fluid=True, )

#====================================
#Callbacks
#====================================


@app.callback(
    [Output('cidade_dropdown', 'options')],
    [Input('estado_dropdown', 'value')]
)
def MunicipioController(uf):
    lista = df_data[df_data['uf'] == uf]['municipio'].unique()
    lista = lista.tolist()
    lista.sort()
    lista = [{"label": i, "value": i} for i in lista]
    
    return [lista]



@app.callback(
    Output('output-container-date-picker-range', 'children'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_output(start_date, end_date):
    string_prefix = 'Você selecionou: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Data inicial: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Data final ' + end_date_string
    if len(string_prefix) == len('Você selecionou: '):
        return 'Selecione a data'
    else:
        return string_prefix


@app.callback(Output('map-graph', 'figure'), Input('cidade_dropdown', 'value'))
def updateMap(cidade):
    if cidade != None:
        df_intermediate = df_data[df_data["municipio"] == cidade] if cidade != 0 else df_data.copy()
    else:
        df_intermediate = df_data.copy()

    px.set_mapbox_access_token(open("keys/mapbox_key").read())
    
    map_fig = px.scatter_mapbox(df_intermediate, lat="latitude", lon="longitude",
                color='pessoas', size="feridos", size_max=20, zoom=3, opacity=0.4 )
    
    map_fig.update_layout(mapbox=dict(center=go.layout.mapbox.Center(lat=centerLat, lon=centerLong)),
                template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                margin=go.layout.Margin(l=10, r=10, t=10, b=10))
    print(cidade)
    print(df_intermediate)
    return map_fig


if __name__ == '__main__':
    app.run_server(debug=True)