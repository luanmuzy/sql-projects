import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import sqlite3
import pandas as pd
import plotly.express as px

# Inicializar o app Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Função para conectar ao banco de dados e buscar os dados com base no intervalo de datas
def fetch_data(start_date, end_date):
    conn = sqlite3.connect('database/retrun.db')
    query = f'''
    SELECT MOTIVO, COUNT(*) as cat_count
    FROM returns
    WHERE DATE("DATA (OBRIGATORIO)") BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY MOTIVO
    ORDER BY cat_count DESC
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Layout do dashboard
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Dashboard de Motivos de Retorno", className="text-center"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.DatePickerRange(
                id='date-picker-range',
                min_date_allowed='2022-01-01',
                max_date_allowed='2024-12-31',
                start_date='2024-01-01',
                end_date='2024-12-31',
                display_format='YYYY-MM-DD',
                style={"margin-top": "20px"}
            )
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='graph-output'), width=12)
    ])
])

# Callback para atualizar o gráfico com base no intervalo de datas selecionado
@app.callback(
    Output('graph-output', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graph(start_date, end_date):
    # Buscar os dados com base no intervalo de datas
    df = fetch_data(start_date, end_date)

    # Verifica se há dados retornados
    if not df.empty:
        fig = px.bar(df, x='MOTIVO', y='cat_count', title=f'Motivos de Retorno ({start_date} a {end_date})',
                     labels={'MOTIVO': 'Motivo', 'cat_count': 'Quantidade'})
    else:
        fig = px.bar(x=[], y=[], title="Nenhum dado disponível para o intervalo selecionado")

    return fig

# Rodar o servidor Dash
if __name__ == '__main__':
    app.run_server(debug=True)
