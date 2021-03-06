# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 14:25:41 2021

@author: straw
"""
from dash.dependencies import Input, Output
from app import app
from layouts import df, df_population
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

@app.callback(Output("scatter", "figure"), 
              [Input("facteur", "value")])
def display_scatter(feature):
    fig = px.scatter(df_population, x="gdp_per_capita", y=feature,
                 size="population", color="location",
                 hover_name="location", log_x=True, size_max=60,
                 title="Variation du GDP en fonction du {} au 19 octobre 2020".format(feature))
    return fig

@app.callback(Output('covid-evolution', 'figure'),
              [Input('country-filter', 'value')])
def update_graph(selected_dropdown_value):
    trace1 = []
    trace2 = []
    trace3 = []
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
        
        trace3.append(go.Scatter(
                    x = df_sub['date'],
                    y = df_sub['stringency_index'],
                    mode = "lines+markers",
                    name = "Stringency index",
                    #marker = dict(color = 'rgba(80, 26, 80, 0.8)'),
                    text = str(country)))
    
    traces = [trace1, trace2, trace3]
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
    df_dates = df.groupby([df.date.dt.strftime('%m %Y'), 'location','iso_code'])[['total_cases', 'total_deaths', 'population', 'gdp_per_capita', 'human_development_index', 'stringency_index']].max().reset_index()
    df_dates['date'] = pd.to_datetime(df_dates['date'])
    df_dates = df_dates.sort_values(by='date',ascending=True).reset_index(drop=True)
    df_dates['date'] = df_dates['date'].astype(str)
    fig = px.choropleth(df_dates, locations="iso_code",
                    color=feature, 
                    hover_name="location",
                    animation_frame="date",
                    animation_group="location",
                    title = "Visualisation des cas et des morts de la covid-19 dans le monde")
    return fig


