import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import dash
from helpers import update_volume_plot, update_volume_map
from config import app_config

dash.register_page(__name__,name="Volume", path='/volume')

layout = dbc.Container(
    [
               dbc.Row(
    [
        dbc.Col(
            html.Div("Select region:", className="dropdown-label"),
            width=1,
        ),
        dbc.Col(
            dcc.Dropdown(
                id='region-dropdown',
                options=[
                    {'label': region, 'value': region}
                    for region in app_config['regions']
                ],
                value='South East',  # Default selected region
            ),
            width=2
        ),
        dbc.Col(
            html.Div("Select year:", className="dropdown-label"),
            width=1,
        ),
        dbc.Col(
            dcc.Dropdown(
                id='year-dropdown',
                options=[{"label": i, "value": i} for i in app_config['years']],
                value='2023',  # Default selected year
            ),
            width=2,
        ),
    ],
    className = "dropdown-row"
),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='volume-plot-line',
                        style={'height': '60vh'}
                    ),
                    width=6
                ),
                dbc.Col(
                    dcc.Graph(
                        id='volume-plot-map',
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

# Define callback to update the new plot based on selected year and region
@callback(
    Output('volume-plot-line', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('region-dropdown', 'value')]
)
def update_volume_plot_callback(selected_year, selected_region):
    return update_volume_plot(selected_year, selected_region)

# Define callback to update the new plot based on selected year and region
@callback(
    Output('volume-plot-map', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('region-dropdown', 'value')]
)
def update_volume_map_callback(selected_year, selected_region):
    return update_volume_map(selected_year, selected_region)