import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from utils import set_dataframe, group_by_customer, get_customers_available, get_years_available
from utils_html import main_layout

dir = "C:/Users/AlanSandoval/Downloads/kimai_complete.csv"
include_optimen_hours = True # modify
data = set_dataframe(dir, include_optimen_hours, data_prepared=True)

app = dash.Dash(__name__)

group_customer = group_by_customer(data)
fig = px.pie(group_customer, values='Duration', names=group_customer.index, title='Historic')

# app.layout = main_layout(fig)
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
            # html.Div(["Year: ", dcc.Input(id="input-year", value="2024",
            html.Div(["Year: ", dcc.Dropdown(get_years_available(data), 'All', multi=False,id="input-year"),],
                                        #    type='number', style={'height':'50px',
                                                                #  'font-size':35}),],
                                            style={'font-size': 40}
            ),
            html.Div(["Month: ", dcc.Input(id="input-month", value="January",
                                           type='text', style={'height':'50px',
                                                                 'font-size':35}),],
                                            style={'font-size': 40}
            ),
            html.Div(["Customer: ", dcc.Dropdown(get_customers_available(data), 'All', multi=True,id="input-customer"),],
                                            style={'font-size': 40}
            ),
            html.Br(),
            html.Br(),
            html.Div(dcc.Graph(id='bar-plot')),
            # dcc.Graph(figure=fig)
        ]
    )


@app.callback(Output(component_id='bar-plot', component_property='figure'),
              Input(component_id="input-year", component_property='value'),
              Input(component_id="input-month", component_property='value'),
              Input(component_id="input-customer", component_property='value'))

def get_graph(year, month, customer):
    # set_values = get_set_posible_values()
    # df_year = data[(data['Date'].dt.year == year) & (data['Date'].dt.month_name() == month)]
    # df_year = data[data['Date'].dt.year == year]
    # # df_year = data
    # df_year.groupby('Customer')['Duration'].sum().reset_index()
    # fig1 = px.pie(df_year, values='Duration', names='Customer', title= f"{month} {year}", hole=.3)
    # fig1.update_layout()
    # return fig1
    # if year != "":
        # data = data[data['Date'].dt.year == year]

    fig = px.sunburst(data, path=['Customer', 'Project', 'Activity'], values='Duration')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
