from logging import StrFormatStyle
from os import terminal_size
import dash
# import dash_core_components as dcc
from dash import dcc
# import dash_html_components as html
from dash import html
import numpy as np
import pandas as pd
import plotly.express as px
import pickle
# import GradientBoostingRegressor
import plotly.graph_objects as go
# from Predict_input import *
from dash.dependencies import Input, Output
import joblib as jb
# from sklearn.externals import joblib

# external_stylesheets=['style.css'] 

df = pd.read_csv('Data/cleaned_data.csv')
dff = df.groupby(["location" ,"bed" ,"bath" ,"toilet" , "Property_Type"	,"Parking_Space" ,"Security" ,"Electricity" ,"Furnished" ,"Security_Doors" ,"CCTV" ,"Pool" ,"Gym" ,"BQ"])['price'].median().reset_index()

def ecod_data(prot):
    prot.replace("Flat / apartment", 12, inplace=True)
    prot.replace("Blocks of flats", 11, inplace=True)
    prot.replace("Massionette house", 10, inplace=True)
    prot.replace("Penthouse flat", 9, inplace=True)
    prot.replace("Terraced duplex", 8, inplace=True)
    prot.replace("Terraced bungalow", 7, inplace=True)
    prot.replace("Detached duplex", 6, inplace=True)
    prot.replace("Mini flat", 5, inplace=True)
    prot.replace("Self contain", 4, inplace=True)
    prot.replace("Detached bungalow", 3, inplace=True)
    prot.replace("Semi detached duplex", 2, inplace=True)
    prot.replace("Semi detached bungalow", 1, inplace=True)
    return prot

def enco_loti(loca):
    loca.replace("lekki phase 1", 7, inplace=True)
    loca.replace("ikeja", 6, inplace=True)
    loca.replace("gbagada", 5, inplace=True)
    loca.replace("surulere", 4, inplace=True)
    loca.replace("yaba", 3, inplace=True)
    loca.replace("ajah", 2, inplace=True)
    loca.replace("ikorodu", 1, inplace=True)
    return loca


with open('Data/model_pickle', 'rb')as file:
    GB_model = pickle.load(file)
    GB_model = jb.load('Data/model_pickle')
# GB_model= decompress_pickle('small_model.pbz2')


app = dash.Dash(__name__)#,external_stylesheets=['style.css'],  


app.title = 'test'
server = app.server

location = dff["location"].unique()
print(location)


Property_Type = dff["Property_Type"].unique()
print(location)

app.layout = html.Div([
    html.Div([
        html.Div([
             html.Div([
                html.H1('Lagos House Price Project', style={'margin-bottom': '0px', 'color': 'white'}),
                html.H4('An appication that gives you an estimate of rent prices of houses in Lagos', style={'margin-bottom': '0px', 'color': 'white'})
            ]),
    
            html.Img(src=app.get_asset_url('datajedi.jpg'),
                     id='datajedi-image',
                     style={'height': '80px',
                            'width': 'auto',
                            'margin-bottom': '0px'})
        ]),
        ] , id='header', className='row flex-display', style={'margin-bottom': '25px'}),
           
    html.Div([
        html.Div([
        html.P('Location:', className='fix_label', style={'color': 'white'}),
        dcc.Dropdown(id='location',
                     multi = False,
                     clearable = True,
                     disabled= False,
                     style = {'display': True},
                     value='ajah',
                     placeholder="Select Location",
                     options=[{'label': c, 'value': c }for c in location]
                     ),
        # html.P('Select Area:',className ='fix_label', style = {'color': 'white'}),
        # dcc.Dropdown(id='area',
        #              multi = False,
        #              clearable = True,
        #              disabled =  False,
        #              style = {'display': True},
        #              options=[]
        #              ),
        html.P('Property Type:', className='fix_label', style={'color': 'white'}),
        dcc.Dropdown(id='Property_Type',
                     multi = False,
                     clearable = True,
                     disabled= False,
                     style = {'display': True},
                     value='Mini flat',
                     placeholder="Select Property Type",
                     options=[{'label': c, 'value': c }for c in Property_Type]
                     ),
        html.P('Select No Bedrooms;', className ='fix_label',style={'color':'white','margin-left': '1%'}),
        dcc.Slider(id='bed--slider',
                   min=df['bed'].min(),
                   max=df['bed'].max(),
                   value=df['bed'].max(),
                   marks={str(bed): str(bed) for bed in df['bed'].unique()},
                   step=None),
                   #Style= {'color':'black'}),
        html.P('Select No Bathrooms;', className ='fix_label',style={'color':'white','margin-left': '1%'}),           
        dcc.Slider(id='bath--slider',
                   min=df['bath'].min(),
                   max=df['bath'].max(),
                   value=df['bath'].max(),
                   marks={str(bath): str(bath) for bath in df['bath'].unique()},
                   step=None),
        html.P('Select No Toilets;', className ='fix_label',style={'color':'white','margin-left': '1%'}),           
        dcc.Slider(id='toilet--slider',
                   min=df['toilet'].min(),
                   max=df['toilet'].max(),
                   value=df['toilet'].max(),
                   marks={str(toilet): str(toilet) for toilet in df['toilet'].unique()},
                   step=None), 
        # html.P('service level;', className ='fix_label',style={'color':'white','margin-left': '1%'}),                                                
        # dcc.RadioItems(id='service_level',
        #                options=[{'label': ' :Yes', 'value': 1}, {'label': ' :No', 'value': 0}],
        #                value=0,
        #                style={'margin-bottom': '0px', 'color': 'grey'}),
        html.P('Do you need a parking space ?', className ='fix_label',style={'color':'white','margin-left': '1%'}),               
        dcc.RadioItems(id='Parking Space',
                       options=[{'label': ' :Yes', 'value': 1}, {'label': ' :No', 'value': 0}],
                       value=0,
                       style={'margin-bottom': '0px', 'color': 'grey'}),
        html.P('Do you need dedicated security ?', className ='fix_label',style={'color':'white','margin-left': '1%'}),               
        dcc.RadioItems(id='Security',
                       options=[{'label': ' :Yes', 'value': 1}, {'label': ' :No', 'value': 0}],
                       value=0,
                       style={'margin-bottom': '0px', 'color': 'grey'}),
        html.P('Does your property need furnished ?', className ='fix_label',style={'color':'white','margin-left': '1%'}),               
        dcc.RadioItems(id='furnished',
                       options=[{'label': ' :Yes', 'value': 1}, {'label': ' :No', 'value': 0}],
                       value=0,
                       style={'margin-bottom': '0px', 'color': 'grey'}),
        html.P('Do you need a 24/7 electricity ?', className ='fix_label',style={'color':'white','margin-left': '1%'}),
        dcc.RadioItems(id='Electricity',
                       options=[{'label': ' :Yes', 'value': 1}, {'label': ' :No', 'value': 0}],
                       value=0,
                       style={'margin-bottom': '0px', 'color': 'grey'}),
        html.P('Do you need Security Doors ?', className ='fix_label',style={'color':'white','margin-left': '1%'}),
        dcc.RadioItems(id='Security Doors',
                       options=[{'label': ' :Yes', 'value': 1}, {'label': ' :No', 'value': 0}],
                       value=0,
                       style={'margin-bottom': '0px', 'color': 'grey'}),
        html.P('Do you need CCTV survalance ?', className ='fix_label',style={'color':'white','margin-left': '1%'}),
        dcc.RadioItems(id='CCTV',
                       options=[{'label': ' :Yes', 'value': 1}, {'label': ' :No', 'value': 0}],
                       value=0,
                       style={'margin-bottom': '0px', 'color': 'grey'}),
        html.P('Do you need a swimming pool ?', className ='fix_label',style={'color':'white','margin-left': '1%'}),
        dcc.RadioItems(id='Pool',
                       options=[{'label': ' :Yes', 'value': 1}, {'label': ' :No', 'value': 0}],
                       value=0,
                       style={'margin-bottom': '0px', 'color': 'grey'}),
        html.P('Do you need gym facilies ?', className ='fix_label',style={'color':'white','margin-left': '1%'}),
        dcc.RadioItems(id='Gym',
                       options=[{'label': ' :Yes', 'value': 1}, {'label': ' :No', 'value': 0}],
                       value=0,
                       style={'margin-bottom': '0px', 'color': 'grey'}),
        html.P('Do you need a boy quater ?', className ='fix_label',style={'color':'white','margin-left': '1%'}),
        dcc.RadioItems(id='BQ',
                       options=[{'label': ' :Yes', 'value': 1}, {'label': ' :No', 'value': 0}],
                       value=0,
                       style={'margin-bottom': '0px', 'color': 'white'})
    ], className = "create_container six columns"),
    html.Div([
        html.Div([
            html.H6(children='Budgeted Price',
                    style={'textAlign': 'center','color': 'white'}),
            html.P(id='my_output',
                   style={'textAlign': 'center','color': '#3e7dbd','fontSize': 80})
    ],className ="create_contain six columns"),
        ]),
    html.Div([
            dcc.Graph(id='bar_chart'),
        ], className="create_container six columns"),
], className = "row flex-display"),
])


@app.callback(
    Output('bar_chart', 'figure'),
    Input('bed--slider', 'value'),
    Input('location', 'value'),
    Input('Property_Type', 'value'))
    #Input('serviced', 'value'),
    #Input('furnished', 'value'))
#def update_figure(bed_slider,location_name,new_flag,serviced,furnished):
    #df_filter= dff[(dff['bed'] == bed_slider) & (dff['location'] == location_name) & (dff['new_flag'] == new_flag) & (dff['serviced_flag'] == serviced) & (dff['furnish_flag'] == furnished)]
def update_figure(bed_slider, location_name):
    df_filter = dff[(dff['bed'] == bed_slider) & (dff['location'] == location_name)]
    fig = px.bar(df_filter, x= 'price', y='Property_Type',color_discrete_sequence=['#3e7dbd']*len(df_filter),orientation='h')
    fig.update_layout(autosize= True,
                      margin=dict(l=30, r=30, t=70, b=30),
                      paper_bgcolor = "#202a3b",plot_bgcolor= "#202a3b",
                      font=dict(color="#c3c3c3"))
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, categoryorder = 'total ascending')
    return fig


@app.callback(
    Output('my_output','children'),
    Input('location', 'value'),
    Input('Property_Type', 'value'),
    Input('bed--slider', 'value'),
    Input('bath--slider', 'value'),
    Input('toilet--slider', 'value'),
    Input('Parking Space','value'),
    Input('Security','value'),
    Input('furnished', 'value'),
    Input('Electricity', 'value'),
    Input('Security Doors', 'value'),
    Input('CCTV', 'value'),
    Input('Pool', 'value'),
    Input('Gym', 'value'),
    Input('BQ','value'))
def price_value(locator,bed_n,bath_n,toiler_n,pt,ps,sec,furn,elect,sec_d,cam,sp,gf,bq):
    price_val = dff[(enco_loti(dff['location']) == locator) & (dff['bed'] == bed_n) & (dff['bath'] == bath_n) & (dff['toilet'] == toiler_n) & (ecod_data(dff['Property_Type']) == pt) & (dff['Parking_Space'] == ps) & (dff['Security'] == sec) & (dff['Furnished'] == furn) & (dff['Electricity'] == elect) & (dff['Security_Doors'] == sec_d) & (dff['CCTV'] == cam) & (dff['Pool'] == sp) & (dff['Gym'] == gf) & (dff['BQ'] == bq)]
    print(price_val)
    try:
        final_price = int(float(str(price_val['price'].unique()[0])))
        min_budget = int(final_price - (final_price * 0.2))
        max_budget = int(final_price + (final_price * 0.2))
        output = "Your rent budget is between {} and {} ".format(min_budget, max_budget)
        data = predict_input(location, bed, bath, toilet, Property_Type, Parking_Space, Security, Electricity, Furnished, Security_Doors, CCTV, Pool, Gym, BQ)
        final_price = GB_model.predict(data)[0]
        final_price = str(price_val['price'].unique()[0])
    except:
        final_price = 'Not available'
        output= final_price
    return output











if __name__ == '__main__':
    app.run_server(debug=True)