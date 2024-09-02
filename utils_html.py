import dash
from dash import dcc
from dash import html

def main_layout(fig):
    container = html.Div(
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
            dcc.Graph(figure=fig)
        ]
    )
    return container
