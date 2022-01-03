from datetime import timedelta
from pandas.core.reshape import tile
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Output, Input

import numpy as np
import pandas as pd


# =====================================================================
# Data Load

df =pd.read_excel('dados.xlsx')

valor_meta = 321111

# =====================================================================
# Data manipulation
# produção mensal
producao_mensal = df['PESO'].sum()
cartao_producao_mensal = (f'{producao_mensal:_.2f} KG')
cartao_producao_mensal = cartao_producao_mensal.replace(
    '.', ',').replace('_', '.')

# Meta mensal
meta_mensal = valor_meta
cartao_meta_mensal = (f'{meta_mensal:_.2f} KG')
cartao_meta_mensal = cartao_meta_mensal.replace('.', ',').replace('_', '.')

# Média Operador
quantidade_operador = df['NOME'].nunique()
media_operador = (f'{producao_mensal / quantidade_operador:_.2f} KG')
cartao_media_operador = media_operador.replace('.', ',').replace('_', '.')

# Meta operador
meta_operador = (f'{meta_mensal / quantidade_operador:_.2f} KG')
cartao_meta_operador = meta_operador.replace('.', ',').replace('_', '.')

# Gráfico produção por turno
df_turno = df.groupby('TURNO').agg({'PESO': np.sum}).reset_index()
list_turno_nome = list(
    map(lambda nturno: (f'<b>Turno 0{nturno}</b>'), df_turno['TURNO'].to_list()))
list_turno_peso = df_turno['PESO'].to_list()

fig_turno = go.Figure(layout={"template": "plotly_dark"})
fig_turno.add_trace(go.Bar(x=list_turno_nome, y=list_turno_peso))
fig_turno.update_traces(width=0.5, marker=dict(color="#fff101"))

cont = 0
peso_label_turno = list(map(lambda xlabel: (f'<b>{xlabel:_.2f}</b>').replace(
    '.', ',').replace('_', '.'), list_turno_peso))
for i, t in enumerate([list_turno_peso]):
    fig_turno.data[i].text = peso_label_turno
    fig_turno.data[i].textposition = 'outside'
    cont += 1

fig_turno.update_layout(
    paper_bgcolor='rgb(40,40,40)',
    height=500,
    activeshape_fillcolor='rgb(40,40,40)',
    plot_bgcolor='rgb(40,40,40)',
    xaxis_showgrid=False, yaxis_showgrid=False,
    yaxis_visible=False,
    autosize=True,
    margin=dict(l=50, r=50, b=0, t=60),
    font=dict(
        family="Montserrat",
        size=20,
        color='#fff'),
    xaxis=dict(linecolor='#fff')
)

# Table top 5 protividade por operador
df_operador = df.groupby('NOME').agg({'PESO': np.sum}).sort_values(
    'PESO', ascending=False).reset_index()
df_operador = df_operador.loc[:9]
list_operador_nome = list(
    map(lambda nome: f'<b>{nome.title()}</b>', df_operador['NOME'].to_list()))
list_operador_peso = list(map(lambda xlabel: (f'<b>{xlabel:_.2f}</b>').replace(
    '.', ',').replace('_', '.'), df_operador['PESO'].to_list()))

fig_tabela = go.Figure(
    data=[go.Table(
        header=dict(values=['<b>Posição</b>', '<b>Nome</b>', '<b>Produção</b>'], height=30, align=['center', 'left', 'center'], fill_color='rgba(40,40,40,0)',
                    font=dict(color='#fff101', size=16), line_color='rgb(40,40,40)'),
        cells=dict(values=[['<b>1°</b>', '<b>2°</b>', '<b>3°</b>', '<b>4°</b>', '<b>5°</b>', '<b>6°</b>', '<b>7°</b>', '<b>8°</b>', '<b>9°</b>', '<b>10°</b>'],
                           list_operador_nome, list_operador_peso], height=30, align=['center', 'left', 'center'],
                   fill_color=[['rgba(255,255,255,0.1)', 'rgb(40,40,40)']*5],
                   font=dict(size=22)),
        columnwidth=[100, 400, 200],
    )
    ], layout={"template": "plotly_dark"}
)

fig_tabela.update_layout(
    height=600,
    paper_bgcolor='rgb(40,40,40)',
    plot_bgcolor='rgb(40,40,40)',
    margin=dict(l=50, r=30, b=30, t=50),
    font=dict(
        family="Montserrat",
        size=20,
        color='#fff'),
)

# =====================================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# =====================================================================
# Layout
app.layout = dbc.Container(
    dbc.Row([
            #-------------- Title
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.P("Painel de produção - Picotadeiras", style={
                               'color': "#fff101", 'font-size': '40px', 'font-weight': '800', 'height':'40px', "border-radius": "10px 10px 10px 10px"})
                    ])
                ], style={"margin": "20px 20px 15px 20px","border-radius": "10px 10px 10px 10px"})], md=12),
            #------------- Cards
            dbc.Col([dbc.Card([
                dbc.CardBody([
                    html.P("Produção mensal", style={
                           'color': "#fff", 'font-size': '25px'}),
                    html.P(children=cartao_producao_mensal, id='card-producao-mensal', style={
                           'color': "#fff101", 'font-size': '40px', 'font-weight': '700'})
                ])
            ], style={"margin": "0px 0px 0px 20px", "border-right": "solid 0.1px rgba(255,255,255,0.2)", "border-radius": "10px 0 0 10px"})], md=3),
            dbc.Col([dbc.Card([
                dbc.CardBody([
                    html.P("Meta mensal", style={
                           'color': "#fff", 'font-size': '25px'}),
                    html.P(children=cartao_meta_mensal, style={
                           'color': "#fff101", 'font-size': '40px', 'font-weight': '700'}, id='card-meta-mensal')
                ])
            ], style={"margin": "0px 20px 0px 0px", "border-left": "solid 0.1px rgba(255,255,255,0.2)", "border-radius": "0 10px 10px 0"})], md=3),
            dbc.Col([dbc.Card([
                dbc.CardBody([
                    html.P("Média operador", style={
                           'color': "#fff", 'font-size': '25px'}),
                    html.P(children=cartao_media_operador, style={
                           'color': "#fff101", 'font-size': '40px', 'font-weight': '700'}, id='card-media-operador')
                ])
            ], style={"margin": "0px 0px 0px 0px", "border-right": "solid 0.1px rgba(255,255,255,0.2)", "border-radius": "10px 0 0 10px"})], md=3),
            dbc.Col([dbc.Card([
                dbc.CardBody([
                    html.P("Meta operador", style={
                           'color': "#fff", 'font-size': '25px'}),
                    html.P(children=cartao_meta_operador, style={
                           'color': "#fff101", 'font-size': '40px', 'font-weight': '700'}, id='card-meta-operador')
                ])
            ], style={"margin": "0px 20px 0px 0px", "border-left": "solid 0.1px rgba(255,255,255,0.2)", "border-radius": "0 10px 10px 0"})], md=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.P("Produção por Turno", style={
                               'color': "#fff", 'font-size': '30px', 'font-weight': '600'}),
                        dcc.Graph(figure=fig_turno, style={
                                  "background-color": "#242424"}, id='graph-producao-turno')
                    ])
                ], style={'height': '78%', "margin": "15px 20px 15px 20px","border-radius": "10px 10px 10px 10px"})], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.P("5 Maiores produtividades do mês", style={
                               'color': "#fff", 'font-size': '30px', 'font-weight': '600'}),
                        dcc.Graph(figure=fig_tabela, style={
                                  "background-color": "#242424"}, id='table-classificacao')
                    ])
                ], style={'height': '78%', "margin": "15px 20px 15px 0","border-radius": "10px 10px 10px 10px"})], md=6),
            dcc.Interval(id='dash-update', interval = 10000)
            ], className="g-0"), fluid=True)

# =====================================================================
# Updating Data
@app.callback(
    [
        Output("card-producao-mensal", "children"),
        Output("card-meta-mensal", "children"),
        Output("card-media-operador", "children"),
        Output("card-meta-operador", "children")
    ],[Input('dash-update', 'n_intervals')]
    )
def update_dash(df):

    df =pd.read_excel('dados.xlsx')
    valor_meta = 321111

    # produção mensal
    producao_mensal = df['PESO'].sum()
    cartao_producao_mensal = (f'{producao_mensal:_.2f} KG')
    cartao_producao_mensal = cartao_producao_mensal.replace(
        '.', ',').replace('_', '.')

    # Meta mensal
    meta_mensal = valor_meta
    cartao_meta_mensal = (f'{meta_mensal:_.2f} KG')
    cartao_meta_mensal = cartao_meta_mensal.replace('.', ',').replace('_', '.')

    # Média Operador
    quantidade_operador = df['NOME'].nunique()
    media_operador = (f'{producao_mensal / quantidade_operador:_.2f} KG')
    cartao_media_operador = media_operador.replace('.', ',').replace('_', '.')

    # Meta operador
    meta_operador = (f'{meta_mensal / quantidade_operador:_.2f} KG')
    cartao_meta_operador = meta_operador.replace('.', ',').replace('_', '.')

    return (cartao_producao_mensal,
    cartao_meta_mensal,
    cartao_media_operador,
    cartao_meta_operador
    )

if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
