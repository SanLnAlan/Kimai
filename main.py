import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from utils import set_dataframe, group_by_customer

dir = "C:/Users/AlanSandoval/Downloads/all-kimai-export.csv"
include_optimen_hours = True # modify
data = set_dataframe(dir, include_optimen_hours)

app = dash.Dash(__name__)

group_customer = group_by_customer(data)
fig = px.pie(group_customer, values='Duration', names=group_customer.index, title='Historic')

app.layout = html.Div(children=[html.H1('Airline Dashboard',
                                        style={'testAlign': 'center',
                                               'color': '#503D36',
                                               'font-size': 40}),
                                html.P('Proportions of things',
                                       style={'testAlign': 'center',
                                              'color': '#FF3D36'
                                       }),
                                dcc.Graph(figure=fig)
                                ]
                    )

if __name__ == '__main__':
    app.run_server()
