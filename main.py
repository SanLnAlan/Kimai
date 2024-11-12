import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from Dataframe import Dataframe, filter_by_date, filter_by_customer, filter_by_user
from datetime import *


dir = "C:/Users/AlanSandoval/Downloads/kimai_test.csv"
data = Dataframe(dir, data_prepared=False)

app = dash.Dash(__name__)

app.layout = html.Div(
        style={'padding': '20px', 'backgroundColor': '#f9f9f9'},
        children=[
            html.H1(
                'Airline Dashboard',
                style={
                    'textAlign': 'center',
                    'color': '#503D36',
                    'fontSize': 40,
                    'marginBottom': '20px'
                }
            ),
            html.Div(
                [
                    "Date: ",
                    dcc.DatePickerRange(
                        start_date=datetime.date(datetime.now().replace(day=1)),
                        end_date_placeholder_text='Select a date!',
                        id="input-date"
                    ),
                ],
                                        #    type='number', style={'height':'50px',
                                                                #  'font-size':35}),],
                style={'font-size': 40}
            ),
            
            # html.Div(["Month: ", dcc.Input(id="input-month", value="January",
            #                                type='text', style={'height':'50px',
            #                                                      'font-size':35}),],
            #                                 style={'font-size': 40}
            # ),
            html.Div(["User: ", dcc.Dropdown(data.get_users_available(), '', multi=True,id="input-user"),],
                                            style={'font-size': 40}
            ),
            html.Div(["Customer: ", dcc.Dropdown(data.get_customers_available(), '', multi=True,id="input-customer"),],
                                            style={'font-size': 40}
            ),
            html.Br(),
            html.Br(),
            html.Div(dcc.Graph(id='bar-plot')),
            # dcc.Graph(figure=fig)
        ]
    )


@app.callback(Output(component_id='bar-plot', component_property='figure'),
            #   Input(component_id="input-year", component_property='value'),
              Input("input-date", "start_date"),
              Input("input-date", "end_date"),
            #   Input(component_id="input-month", component_property='value'),
              Input(component_id="input-customer", component_property='value'),
              Input(component_id="input-user", component_property='value')
            )

def get_sunburst(start_date,end_date, customer, user):
    # df_year = data[(data['Date'].dt.year == year) & (data['Date'].dt.month_name() == month)]
    # df_year = data[data['Date'].dt.year == year]
    # # df_year = data
    # df_year.groupby('Customer')['Duration'].sum().reset_index()
    # fig1 = px.pie(df_year, values='Duration', names='Customer', title= f"{month} {year}", hole=.3)
    # fig1.update_layout()
    # return fig1
    data_output = data.df

    data_output = filter_by_date(data_output, start_date, end_date)

    if customer not in ["", []]:
        data_output = filter_by_customer(data_output, customer)

    if user not in ["", []]:
        data_output = filter_by_user(data_output, user)

    return px.sunburst(data_output, path=['Customer', 'Project', 'Activity', 'Ticket'], values='Duration', title=f'{start_date} - {end_date}')
    # fig = px.sunburst(data_output, path=['Customer', 'Project', 'Activity'], values='Duration', title=str(years))
    # return fig


if __name__ == '__main__':
    app.run_server(debug=True)
