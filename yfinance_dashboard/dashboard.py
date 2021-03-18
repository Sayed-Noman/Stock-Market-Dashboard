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
       #Dropdown Title
        html.P("Chose a Ticker Name :", className ='start'),
        #Dropdown List
        dcc.Dropdown("Dropdown_Tickers", options = [
                {"label" : "Apple", "value" :"AAPL" },
                {"label" : "Tesla", "value" :"TSLA" }, 
                {"label" : "Facebook", "value" :"FB" },              
        ]),
       #Dropdown Button
       html.Div([
            html.Button('Stock Price', className= 'stock-btn', id ='stock'),
            html.Button('Indicators', className = 'indicator-btn', id = 'indicators'),
        ], className='buttons'),

    ], className = 'navigation'),

    #Content Block
    html.Div([
        #Content Header
        html.Div([
            html.P(id='ticker'),
            html.Img(id='logo'),
        ], className='header'),

        #Content Description
        html.Div(id='description',className= 'description_ticker'),

        #Content Graphs
        html.Div([
            html.Div([], id ='graphs-content')
        ], id = 'main-content')

    ], className='content')

], className = 'container')

app.run_server(debug = True)