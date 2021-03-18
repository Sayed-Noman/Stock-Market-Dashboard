# Importing Modules
import dash
import dash_core_components as dcc
import dash_html_components as html
import yfinance as yf
from dash.dependencies import Input,Output
import pandas as pd


app =dash.Dash()

#main Div
app.layout= html.Div([
   #Navigation Bar 
   html.Div([
       



    ], className = 'navigation') 

])

app.run_server(debug = True)