import dash
from dash import dcc
from dash import html

def main_layout(fig):
    return html.Div(
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
            html.Div(["Input: ", dcc.Input(id="input-customer", value="ALASKA (ASA)",
                                           type='number', style={'height':'50px',
                                                                 'font-size':35}),],
                                            style={'font-size': 40}
            ),
            html.Br(),
            html.Br(),
            html.Div(dcc.Graph(id='bar-plot')),
            # dcc.Graph(figure=fig)
        ]
    )
