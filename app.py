# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 14:21:56 2021

@author: straw
"""
import dash

BS = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/solar/bootstrap.min.css"

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[BS])
server = app.server
app.title = "CoViz"
