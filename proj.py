import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import os

app = dash.Dash()
server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')

colors = {
    'background': '#F0F8FF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1(children='''
        Data o krabech
    '''),

    html.Div(children='''
        Variabilita krabů druhu Leptograpsus variegatus      
    '''),

	
	html.Div(children='''Zdroj dat: Campbell, N.A. and Mahon, R.J., 1974           
    '''),
	
	html.Img(src='http://decapoda.free.fr/images/brachyura/letptograpsus_variegatus.jpg'
	),
	
	html.Img(src='http://farm8.static.flickr.com/7521/15890515157_7237fc565f.jpg'
	),
	
	html.Div(children='''
        Obr.1: Tito krabi se vyskytují ve dvou formách - MODRÁ a ORANŽOVÁ      
    '''),
	
	html.Img(src='https://ars.els-cdn.com/content/image/1-s2.0-S0305440314004774-gr2.jpg'
	),
	html.Div(children='''
	
        Obr.2: U jednotlivců byla měřena délka a šířka karapaxu      
    '''),
	
    dcc.Graph(
        id='example-graph',
    ),
	html.Div("""Grafy ukazují rozdíly v rozměrech karapaxu v závislosti na pohlaví nebo formě kraba
	"""),
	
    html.H3("""
        Vybrat graf
    """),
    dcc.Dropdown(
        options=[
            {'label': 'Délka CW podle pohlaví', 'value': 'CW_sex'},
            {'label': 'Délka CL podle pohlaví', 'value': 'CL_sex'},
            {'label': 'Délka CW podle druhu', 'value': 'CW_sp'},
            {'label': 'Délka CL podle druhu', 'value': 'CL_sp'},
        ],
        value='CW_sex',
        id="dropdown-input"
    ),
    dcc.RadioItems(
        options=[
            {'label': 'Histogram', 'value': 'hist'},
            {'label': 'Boxplot', 'value': "boxplot"},
            {'label': 'Barplot', 'value':'bar'},

        ],
        value='hist',
        id='radio-input'
    )
	
])

@app.callback(
    Output(component_id='example-graph', component_property='figure'),
    [Input(component_id="dropdown-input", component_property='value'),
     Input(component_id='radio-input', component_property='value')]
)
def update_figure(data_type, plot_type):
    if data_type == "CW_sex": 
        traces=0
        male = crabs[crabs.sex == "M"].CW
        female = crabs[crabs.sex == "F"].CW
    
        plot_function = go.Histogram if plot_type == 'hist' else go.Box if plot_type == "boxplot" else go.Bar
    
        trace1 = plot_function(x = male, opacity = 0.75, name = 'Šířka samci')
        trace2 = plot_function(x = female, opacity = 0.75, name = 'Šířka samice')
        data = [trace1, trace2]
    
   
        figure={
            'data': data,
            "layout": {
               "title" : 'Distribuce šířky karapaxu vzhledem k pohlaví',
                  "xaxis" :{'title':'Šířka těla'}, "yaxis":{'title':'Počet jedinců'}
              }
            }
            
    elif data_type == "CW_sp": 
        traces=0
        orange = crabs[crabs.sp == "O"].CW
        blue = crabs[crabs.sp == "B"].CW
		
        plot_function = go.Histogram if plot_type == 'hist' else go.Box if plot_type == "boxplot" else go.Bar

        trace1 = plot_function(x = blue, opacity = 0.75, name = 'Šířka modří')
        trace2 = plot_function(x = orange, opacity = 0.75, name = 'Šířka oranžoví')
        data = [trace1, trace2]

        figure={
            'data': data,
            'layout': {
                "title" : 'Distribuce šířky karapaxu vzhledem k druhu',
               "xaxis" :{'title':'Šířka těla'}, "yaxis":{'title':'Počet jedinců'}
              }

        }
    elif data_type == "CL_sex":
	
        traces=0
        male = crabs[crabs.sex == "M"].CL
        female = crabs[crabs.sex == "F"].CL
		
        plot_function = go.Histogram if plot_type == 'hist' else go.Box if plot_type == "boxplot" else go.Bar

        trace1 = plot_function(x = male, opacity = 0.75, name = 'Délka samci')
        trace2 = plot_function(x = female, opacity = 0.75, name = 'Délka samice')
        data = [trace1, trace2]

        figure={
            'data': data,
            'layout': {
                "title" : 'Distribuce délky karapaxu vzhledem k pohlaví',
               "xaxis" :{'title':'Délka těla'}, "yaxis":{'title':'Počet jedinců'}
              }

        }
	
    elif data_type == "CL_sp": 
        traces=0
        orange = crabs[crabs.sp == "O"].CL
        blue = crabs[crabs.sp == "B"].CL
		
        plot_function = go.Histogram if plot_type == 'hist' else go.Box if plot_type == "boxplot" else go.Bar

        trace1 = plot_function(x = blue, opacity = 0.75, name = 'Délka modří')
        trace2 = plot_function(x = orange, opacity = 0.75, name = 'Délka oranžoví')
        data = [trace1, trace2]

        figure={
            'data': data,
            'layout': {
                "title" : 'Distribuce délky karapaxu vzhledem k druhu',
               "xaxis" :{'title':'Druh'}, "yaxis":{'title':'Šířka těla'}
              }

        }
    return figure

crabs = pd.read_csv('https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/MASS/crabs.csv')

if __name__ == '__main__':
    app.run_server()
