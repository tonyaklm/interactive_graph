from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('social_media-ww-monthly-2009-03-2024-02.csv')
df['Date'] = pd.to_datetime(df['Date'])
years = df['Date'].dt.year.unique()
min_year = years.min()
max_year = years.max()
years = years.astype('str')

years = np.append(years, f"С {min_year} по {max_year}")

app.layout = html.Div([
    html.H1(children='Статистика пользования социальными сетями по всему миру',
            style={'text-align': 'center'}),
    html.Div([
        html.Div([
            html.Label(['Выберите год:'], style={'font-weight': 'bold'}),
            dcc.Dropdown(
                years,
                placeholder='Выберите год',
                id='dropdown',
            )
        ],
            style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(
                id='crossfilter-indicator',
                style={'margin-top': '20px'}
            )
        ], style={'width': '80%', 'margin': '10 auto'})
    ])

])


@callback(
    Output('crossfilter-indicator', 'figure'),
    Input('dropdown', 'value'))
def update_graph(year_value):
    title_graph = 'Доля рынка различных социальных сетей '
    if not year_value or year_value == f'С {min_year} по {max_year}':
        dff = df
        title_graph += f'с {min_year} по {max_year}'
    else:
        dff = df[df['Date'].dt.year == int(year_value)]
        title_graph += 'в ' + year_value

    fig = px.line(dff, x='Date', y=df.columns[1::])
    fig.update_layout(title=title_graph,
                      xaxis_title='Дата',
                      yaxis_title='Доля рынка соц. сети (%)',
                      legend_title_text='Соц. сеть'
                      )
    fig.update_traces(hovertemplate='<b>%{y}%</b><br><b>%{x}</b>')

    return fig


if __name__ == '__main__':
    app.run(debug=True, port=5002)
