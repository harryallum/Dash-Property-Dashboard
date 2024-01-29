import dash
from dash import html, dcc, Input, Output, callback, State
import dash_bootstrap_components as dbc
from helpers import update_fastest_growing_plot, update_fastest_declining_plot
from config import app_config

dash.register_page(__name__, path='/growth')

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
                    html.H5("Filter by top:", className="slider-h5"),
                    width=2,
                    style={"display": "flex", "align-items": "center", "height": "50px"}
                ),
                dbc.Col(
                    dcc.Slider(
                        id='slider',
                        min=0,
                        max=100,
                        step=10,
                        value=50,  # Default selected value
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    width=10,
                    style={"height": "50px"}
                ),
            ],
            className="mb-4 top-x-slider",
            style={"margin": "0 0px"}  # Add margin to the row
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='fastest-growing-map',
                        style={'height': '60vh'}
                    ),
                    width=6
                ),
                dbc.Col(
                    dcc.Graph(
                        id='fastest-declining-map',
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

# Add a dcc.Store component to store the selected values
layout.children.insert(
    0,  # Insert the dcc.Store component at the beginning of the layout
    dcc.Store(id='dropdown-store-growth', storage_type='memory', data={'region_value': 'South East', 'year_value': '2023', 'slider_value': 50})
)

# Callback for fastest growing map
@callback(
    Output('fastest-growing-map', 'figure'),
    [Input('dropdown-store-growth', 'data')]
)
def update_fastest_growing_callback(data):
    selected_year = data.get('year_value', '2023')
    selected_region = data.get('region_value', 'South East')
    slider_value = data.get('slider_value', 50)
    return update_fastest_growing_plot(selected_year, selected_region, slider_value)

# Callback for fastest declining map
@callback(
    Output('fastest-declining-map', 'figure'),
    [Input('dropdown-store-growth', 'data')]
)
def update_fastest_declining_callback(data):
    selected_year = data.get('year_value', '2023')
    selected_region = data.get('region_value', 'South East')
    slider_value = data.get('slider_value', 50)
    return update_fastest_declining_plot(selected_year, selected_region, slider_value)

# Define callback to update the stored dropdown values when changed
@callback(
    Output('dropdown-store-growth', 'data'),
    [Input('region-dropdown', 'value'),
     Input('year-dropdown', 'value'),
     Input('slider', 'value')],
    prevent_initial_call=True
)
def update_dropdown_store_growth(region_value, year_value, slider_value):
    return {'region_value': region_value, 'year_value': year_value, 'slider_value': slider_value}
