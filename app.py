import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.express as px


data = pd.read_csv('/Users/datasets/odi-batting.csv')
data['MatchDate'] = pd.to_datetime(data['MatchDate'])
data['year'] = data['MatchDate'].dt.year
countries = data['Country'].unique().tolist()
years = data['year'].unique().tolist()

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar = dbc.NavbarSimple(
    brand='Dashboard',
)


filters = html.Div(
    children=[
        html.P(),
        html.Div(className='container-fluid', children=[
            dbc.Row([
                dbc.Col(html.Div(
                    dcc.Dropdown(id='filter-country',
                                 options=[{'label': i, 'value': i} for i in countries]),
                    )
                ),
            ]),
            html.P(),
            dbc.Row([
                dbc.Col(html.Div(
                    dcc.Slider(
                        id="filter-year",
                        min=min(years),
                        max=max(years),
                        step=None,
                        marks={i: str(i) for i in years},
                        value=max(years))
                )
                ),
            ])
        ])

    ],
)

@app.callback(
    output = Output("top10_players_by_runs", "children"),
    inputs = [Input('filter-country', 'value'), Input('filter-year', 'value')]
)
def on_country_click(country, year):
    if country and year:
        subdata = data[(data['Country'] == country) & (data['year'] == year)]
    elif country:
        subdata = data[(data['Country'] == country)]
    elif year:
        subdata = data[(data['year'] == year)]
    else:
        subdata = data
    top10 = subdata.groupby('Player').agg(Runs=('Runs', 'sum')).reset_index().sort_values('Runs',ascending=False).head(10)

    fig = px.bar(top10, x='Player', y='Runs')
    #fig = top10.plot.bar()
    return dcc.Graph(figure=fig)

@app.callback(
    output = Output("top10_players_by_matches", "children"),
    inputs = [Input('filter-country', 'value'), Input('filter-year', 'value')]
)
def on_year_click(country, year):
    if country and year:
        subdata = data[(data['Country'] == country) & (data['year'] == year)]
    elif country:
        subdata = data[(data['Country'] == country)]
    elif year:
        subdata = data[(data['year'] == year)]
    else:
        subdata = data
    top10 = subdata.groupby('Player').agg(Matches=('MatchDate', 'count')).reset_index().sort_values('Matches',ascending=False).head(10)

    fig = px.bar(top10, x='Player', y='Matches')
    #fig = top10.plot.bar()
    return dcc.Graph(figure=fig)

table = html.Div(
    children=[
        html.P(),
        dbc.Row(
            children=[
                dbc.Col(id="top10_players_by_runs"),
                dbc.Col(id="top10_players_by_matches")
            ]
        )
    ]
)

app.layout = html.Div(children=[
    navbar, filters, table
])


if __name__ == '__main__':
    app.run_server(debug=True)