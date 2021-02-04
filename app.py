# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 14:21:56 2021

@author: straw
"""
import dash

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server
app.title = "CoViz"
