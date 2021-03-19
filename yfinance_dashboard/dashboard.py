# Importing Modules
import dash
import dash_core_components as dcc
import dash_html_components as html
import yfinance as yf
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objects as go


def get_stock_price_fig(data_frame):
    fig = go.Figure()
    fig.add_trace(go.Scatter(mode = 'lines', x= data_frame['Date'], y= data_frame['Close']))
    return fig






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


#Call Backs
@app.callback(
    [Output("ticker","children"),Output("logo","src"),Output("description", "children")],
    [Input("Dropdown_Tickers", "value")],
)

def update_data(ticker_name):
        if ticker_name == None:
            raise PreventUpdate

        ticker = yf.Ticker(ticker_name)
        ticker_info = ticker.info

        data_frame = pd.DataFrame().from_dict(ticker_info, orient="index").T
        data_frame = data_frame[['logo_url','shortName','longBusinessSummary']]


        return data_frame['shortName'].values[0],  data_frame['logo_url'].values[0], data_frame['longBusinessSummary'].values[0]


@app.callback(
    [Output('graphs-content', 'children')],
    [Input('stock','n_clicks'),Input('Dropdown_Tickers','value')],
)

def stock_price(no_time_clicks, ticker_name):
    if no_time_clicks == None:
        raise PreventUpdate
    
    data_frame = yf.download(ticker_name)
    data_frame.reset_index(inplace = True)

    graph_figure = get_stock_price_fig(data_frame)

    return [dcc.Graph(figure = graph_figure)]

app.run_server(debug = True)