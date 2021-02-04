# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 14:25:15 2021

@author: straw
"""
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

df = pd.read_csv('raw_data.csv', sep=',')
df = df.drop(['Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11',
       'Unnamed: 12', 'Unnamed: 13'], axis=1)
df['date'] = pd.to_datetime(df['date'])

def get_options(list_countries):
    dict_list = []
    for c in list_countries:
        dict_list.append({'label': c, 'value': c})
    return dict_list

# df_country = df_country.set_index('date').groupby(pd.Grouper(freq='2D')).sum().reset_index()
df_population = df[df['date']==df['date'].max()].reset_index(drop=True)

scatter_hdi = px.scatter(df_population, x="gdp_per_capita", y="human_development_index",
                 size="population", color="location",
                 hover_name="location", log_x=True, size_max=60,
                 title="Variation du GDP en fonction du HDI au 19 octobre 2020")

page_index_layout = html.Div(children=[
    html.H1(className='header', children='CoViz'),
    dcc.Link('Check Covid-19 Data Visualisation', href='/page-viz'),
    html.Br(),
    dcc.Link('Check Covid-19 Data Analysis', href='/page-bilan'),
])

page_viz_layout = html.Div(children=[
    html.H1(className='header',children='Covid-19 Data Visualisation'),
    html.Div(children=[
        dcc.Graph(id="scatter_hdi", figure=scatter_hdi),
        ]),
    html.Div(children=[
        html.P("Sélectionner pays :"),
        dcc.Dropdown(id='country-filter', options=get_options(df['location'].unique()),
                      multi=True, value=[df['location'].sort_values()[0]],
                      className='country-filter'),
    ]),
    html.Div(children=[
            dcc.Graph(id='covid-evolution',config={'displayModeBar': False}, animate=True)
        ]),
    
    html.Div([
        dcc.RadioItems(id='feature', 
        options=[{'value': x, 'label': x} 
                  for x in ['total_cases', 'total_deaths', 'stringency_index']],
        value='total_cases',
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="choropleth"),
    html.Br(),
    dcc.Link('Check Covid-19 Data Analysis', href='/page-bilan'),
    html.Br(),
    dcc.Link('Go back to main page', href='/')
])
])

page_bilan_layout = html.Div([
    html.H1(className='header', children='Analyse des données Covid-19'),
    html.Div(id='page-bilan-content'),
    html.Br(),
    dcc.Link('Check Covid-19 Data Visualisation', href='/page-viz'),
    html.Br(),
    dcc.Link('Go back to main page', href='/')
])


