import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from helpers import update_map, update_bar_plot
from config import app_config

dash.register_page(__name__, path='/')

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id='region-dropdown',
                        options=[
                            {'label': region, 'value': region}
                            for region in app_config['regions']
                        ],
                        value='South East',  # Default selected region
                    ),
                    width=6
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='year-dropdown',
                        options=[{"label": i, "value": i} for i in app_config['years']],
                        value='2023',  # Default selected year
                    ),
                    width=6
                ),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='bar-plot',
                        style={'height': '60vh'}
                    ),
                    width=6
                ),
                dbc.Col(
                    dcc.Graph(
                        id='avg-price-map',
                        style={'height': '60vh'}
                    ),
                    width=6
                ),
            ],
            className="mb-4",
        ),
    ],
    fluid=True,
)

# Define callback to update the choropleth map based on selected year and region
@callback(
    Output('avg-price-map', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('region-dropdown', 'value')]
)
def update_map_callback(selected_year, selected_region):
    return update_map(selected_year, selected_region)

# Define callback to update the bar plot based on selected region
@callback(
    Output('bar-plot', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('region-dropdown', 'value')]
)
def update_bar_plot_callback(selected_year,selected_region):
    return update_bar_plot(selected_year,selected_region)