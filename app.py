# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 13:23:37 2021

@author: straw
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_stylesheets=external_stylesheets

app = dash.Dash(__name__)

server = app.server

app.title = "Data Storytelling"

df = pd.read_csv('raw_data.csv', sep=',')
df = df.drop(['Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11',
       'Unnamed: 12', 'Unnamed: 13'], axis=1)
df['date'] = pd.to_datetime(df['date'])

country='France'

df_country = df[df['location']==country]

df_country = df_country.set_index('date').groupby(pd.Grouper(freq='2D')).sum().reset_index()

df_population = df[df['date']==df['date'].max()].reset_index(drop=True)

trace1 = go.Scatter(
                    x = df_country['date'],
                    y = df_country['total_cases'],
                    mode = "lines",
                    name = "Total cases",
                    marker = dict(color = 'rgba(16, 112, 2, 0.8)'),
                    text = 'France')
    
trace2 = go.Scatter(
                    x = df_country['date'],
                    y = df_country['total_deaths'],
                    mode = "lines+markers",
                    name = "Total deaths",
                    marker = dict(color = 'rgba(80, 26, 80, 0.8)'),
                    text = 'France')

# trace3 = go.Bar(
#                 x = df_population.iso_code,
#                 y = df_population.population,
#                 name = "population",
#                 marker = dict(color = 'rgba(255, 174, 255, 0.5)',
#                              line = dict(color ='rgb(0,0,0)',width =1.5)),
#                 text = df_population.location)

worldmap = dict(type='choropleth',
            locations=df_population['location'],
            locationmode='country names',
            text=df_population['location'],
            z=df_population['total_cases'],
            colorscale = 'Reds',
            colorbar_title = "Total cases"
            )

layout_map = dict(geo = dict(scope='world',
                         showlakes= False), 
                  title="Nombre de cas de la covid-19 dans le monde")
choromap = go.Figure(data=[worldmap], layout=layout_map)

data1 = [trace1, trace2]

layout1 = dict(title = 'Evolution de la COVID-19 en France', xaxis = dict(title = 'Date',ticklen = 5,zeroline= False))


fig1 = dict(data = data1, layout = layout1)


app.layout = html.Div(children=[
    html.H1(children='Covid-19 world wide evolution'),
    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    html.Div([dcc.Dropdown(
            id="country-filter",
            options=[
                {"label": country, "value": country}
                for country in np.sort(df_population.location.unique())
            ],
            value="Afghanistan",
            className="dropdown"
        ),
    ]
    ),
    html.Div(className='Covid evolution',
             children=[
        dcc.Graph(id='graph1', figure=fig1)
        ]),
    
    html.Div(className='World-map',
              children=[
        dcc.Graph(id='graph2', figure=choromap)
        ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
    