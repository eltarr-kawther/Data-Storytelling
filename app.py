# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 13:23:37 2021

@author: straw
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_stylesheets=external_stylesheets

app = dash.Dash(__name__)

server = app.server

app.title = "CoViz"

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

app.layout = html.Div(children=[
    html.H1(children='Covid-19 Data Visualisation'),
        
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
                 for x in ['total_cases', 'total_deaths','population']],
        value='total_cases',
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="choropleth"),
])
])
             
#----------------------------------------------------------------------------
@app.callback(Output('covid-evolution', 'figure'),
              [Input('country-filter', 'value')])
def update_graph(selected_dropdown_value):
    trace1 = []
    trace2 = []
    for country in selected_dropdown_value:
        df_sub = df[df['location'] == country]
        trace1.append(go.Scatter(
                    x = df_sub['date'],
                    y = df_sub['total_cases'],
                    mode = "lines",
                    name = "Total cases",
                    text = str(country)))
                    
        trace2.append(go.Scatter(
                    x = df_sub['date'],
                    y = df_sub['total_deaths'],
                    mode = "lines+markers",
                    name = "Total deaths",
                    #marker = dict(color = 'rgba(80, 26, 80, 0.8)'),
                    text = str(country)))
    
    traces = [trace1, trace2]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(
                  title = 'Evolution de la COVID-19',
                  xaxis = dict(title = 'Date',ticklen = 5,zeroline= False),
              ),

              }
    return figure

@app.callback(Output("choropleth", "figure"), 
              [Input("feature", "value")])
def display_choropleth(feature):
    df_population = df[df['date']==df['date'].max()].reset_index(drop=True)
    worldmap = dict(type='choropleth',
            locations=df_population['location'],
            locationmode='country names',
            text=df_population['location'],
            z=df_population[feature],
            colorbar_title = feature
            )
    
    layout_map = dict(geo = dict(scope='world', showlakes= False), 
                      title="Nombre de cas et de morts de la covid-19 dans le monde")
    choromap = go.Figure(data=[worldmap], layout=layout_map)

    return choromap

if __name__ == '__main__':
    app.run_server(debug=False)
