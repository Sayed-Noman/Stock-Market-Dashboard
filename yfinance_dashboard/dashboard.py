# Importing Modules
import dash
import dash_core_components as dcc
import dash_html_components as html
import yfinance as yf
from dash.dependencies import Input,Output,State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objects as go


def get_stock_price_fig(data_frame):
    fig = go.Figure()
    fig.add_trace(go.Scatter(mode = 'lines', x= data_frame['Date'], y= data_frame['Close']))
    return fig

def get_dounuts_fig(data_frame, label):
    non_main = 1 - data_frame.values[0]
    labels = ['main', label]
    values = [non_main, data_frame.values[0]]
    fig = go.Figure(data = [go.Pie(labels=labels, values= values, hole=0.449)])
    return fig




app =dash.Dash(external_stylesheets = ["https://fonts.googleapis.com/css2?family=Montserrat:wght@300&display=swap"])

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

    ], className='content'),

], className = 'container')


#Call Backs
@app.callback(
    [dash.dependencies.Output("ticker","children"),dash.dependencies.Output("logo","src"),dash.dependencies.Output("description", "children")],
    [dash.dependencies.Input("Dropdown_Tickers", "value")],
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
    [dash.dependencies.Output('graphs-content', 'children')],
    [dash.dependencies.Input('stock','n_clicks'),dash.dependencies.Input('Dropdown_Tickers','value')],
    
)

def stock_price(no_time_clicks, ticker_name):
    if no_time_clicks == None:
        raise PreventUpdate
    
    if ticker_name == None:
        raise PreventUpdate
    
    data_frame = yf.download(ticker_name)
    data_frame.reset_index(inplace = True)

    graph_figure = get_stock_price_fig(data_frame)

    return [dcc.Graph(figure = graph_figure)]


@app.callback(
    [dash.dependencies.Output('main-content', 'children'),dash.dependencies.Output('stock','n_clicks')],
    [dash.dependencies.Input('indicators', 'n_clicks'),dash.dependencies.Input('Dropdown_Tickers','value')],
    
)
def stock_price_indicator(no_time_clicks, ticker_name):
    if no_time_clicks == None:
        raise PreventUpdate
    
    if ticker_name == None:
        raise PreventUpdate
    
    ticker = yf.Ticker(ticker_name)
    ###Ticker info is converted into dataframe and inverted into column from dictonary format
    data_frame_info = pd.DataFrame.from_dict(ticker.info, orient='index').T
    data_frame_info = data_frame_info[['priceToBook','profitMargins','bookValue','enterpriseToEbitda','shortRatio','beta','payoutRatio','regularMarketPreviousClose','country','sector','trailingEps']]
    print(data_frame_info)
    kpi_data = html.Div([
        html.Div([
                html.Div([
                html.H4('Price to Book'),
                html.P(data_frame_info['priceToBook'])
            ]),
            html.Div([
                html.H4('Enterprise Data'),
                html.P(data_frame_info['enterpriseToEbitda'])
            ]),
            html.Div([
                html.H4('Country'),
                html.P(data_frame_info['country'])
            ]),
            html.Div([
                html.H4('Sector'),
                html.P(data_frame_info['sector'])
            ]),
        ], className='kpi'),

        html.Div([
            dcc.Graph(figure = get_dounuts_fig(data_frame_info['profitMargins'],'Profit Margin')),
            dcc.Graph(figure = get_dounuts_fig(data_frame_info['payoutRatio'],'Payout Ratio')),
        ], className = 'dounuts')
    ])
    
    return [html.Div([kpi_data], id = 'graphs-contents')], None
    



app.run_server(debug = True)