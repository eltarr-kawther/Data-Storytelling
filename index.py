# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 14:23:16 2021

@author: straw
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from app import server
from layouts import page_viz_layout, page_bilan_layout, page_index_layout
import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

#Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-viz':
        return page_viz_layout
    elif pathname == '/page-bilan':
        return page_bilan_layout
    else:
        return page_index_layout

if __name__ == '__main__':
    app.run_server(debug=True)
