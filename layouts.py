# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 14:25:15 2021

@author: straw
"""
import dash_bootstrap_components as dbc
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

head = df.head(200)
stats = df.describe()

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "12rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "color":"#E3655B"
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("CoViz", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Accueil", href="/", active="exact"),
                dbc.NavLink("Data Visualisation", href='/page-viz', active="exact"),
                dbc.NavLink("Data Analysis", href="/page-bilan", active="exact"),
                dbc.NavLink("About", href="/page-about", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

fig_head = go.Figure(data=[go.Table(
    header=dict(values=['','ISO Code','Date','Total Cases','Total Deaths','Stringency index','Population','GDP per capita','Human Development Index'],
                fill_color='#3891A6',
                align='left'),
    cells=dict(values=[head.index, head.iso_code, head.date, head.total_cases, head.total_deaths, head.stringency_index, head.population, head.gdp_per_capita, head.human_development_index],
               fill_color='#FDE74C',
               align='left'))
])

fig_stats = go.Figure(data=[go.Table(
    header=dict(values=['', 'Total Cases','Total Deaths','Stringency index','Population','GDP per capita','Human Development Index'],
                fill_color='#3891A6',
                align='left'),
    cells=dict(values=[stats.index,  stats.total_cases, stats.total_deaths, stats.stringency_index, stats.population, stats.gdp_per_capita, stats.human_development_index],
               fill_color='#FDE74C',
               align='left'))
])

heat_map = px.imshow(df.corr())

scatter_hdi = px.scatter(df_population, x="gdp_per_capita", y="human_development_index",
                 size="population", color="location",
                 hover_name="location", log_x=True, size_max=60,
                 title="Variation du GDP en fonction du HDI au 19 octobre 2020")

page_index_layout = html.Div(children=[
    html.H1(className='welcome-page-title', children='Bienvenue sur CoViz !'),
    html.P(className='welcome-page-text', children='Un dashboard de visualisation et d\'analyse de données de la Covid-19.'),
    html.Div(className='footer', children='© 2021 Kawthar ELTARR')
])

page_viz_layout = html.Div(children=[
    html.H1(className='header',children='Visualisation des données Covid-19'),
    html.Div(className='container',children=[
        dcc.Graph(id="scatter_hdi", figure=scatter_hdi),
        ]),
    html.Div(className='container', children=[
        html.P("Sélectionner un pays afin de visualiser l'évolution du virus :"),
        dcc.Dropdown(id='country-filter', options=get_options(df['location'].unique()),
                      multi=True, value=[df['location'].sort_values()[0]],
                      className='country-filter'),
        dcc.Graph(id='covid-evolution',config={'displayModeBar': False}, animate=True)
        ]),
    
    html.Div(className='container',children=[
        dcc.RadioItems(id='feature', 
        options=[{'value': x, 'label': x} 
                  for x in ['total_cases', 'total_deaths', 'stringency_index']],
        value='total_cases',
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="choropleth"),
    html.Br(),
    html.Div(className='footer', children='© 2021 Kawthar ELTARR'),
])
])

page_bilan_layout = html.Div(children=[
    html.H1(className='header', children='Analyse des données Covid-19'),
    html.Div(className='container', children=
             [
                 html.P('Les données présentées dans cet outil sont des données collectées \
                        dans le cadre d\'une étude sur l\'impact de la covid-19 \
                        sur l\'économie mondiale pour 170 pays. La table ci-dessous est \
                            aperçu de ces données.'),
                html.P('Les données sont des enregistrements journaliers faient du 31 décembre 2019\
                        au 19 octobre 2020 pour différents facteurs.'),
                dcc.Graph(figure=fig_head),
            ]
            ),
    html.Div(className='container',
             children=[
                 html.P('Statistiques sur les données :'),
                dcc.Graph(figure=fig_stats),
            ]),
    html.Div(className='container',
             children=[
                 html.P('La matrice de corrélation suivante montre une forte corrélation attendue \
                        entre le nombre de cas et le nombre morts (91%). Il existe également une \
                        forte corrélation entre le HDI et le GDP (72.6%).'),
                html.P(''),
                dcc.Graph(figure=heat_map),
            ]),
    html.Div(className='footer', children='© 2021 Kawthar ELTARR')
    ])
    
page_about_layout = html.Div(children=[
             html.H1(className='header', children='About'),
             html.Br(),
             html.Div(className='container', children=
                      [
                          html.P('CoViz a été créé dans le cadre d\'un projet étudiant à l\'école La Plateforme_.\
                                 Le but était de développer un dashboard Plotly/Dash multi-pages mettant \
                                 en scène des données permettant d’évaluer l\'impact de la pandémie Covid-19 sur \
                                l\'économie mondiale, accessible via le lien suivant : https://data.mendeley.com/datasets/b2wvnbnpj9/1.'),

                    ]),
             html.Div(className='footer', children='© 2021 Kawthar ELTARR')
             ])





