import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from config import app_config

# Create the Dash app
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SLATE, '/assets/custom.css'])

# Define the navigation bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Price", href="/"))
    ] + [
        dbc.NavItem(dbc.NavLink("Price Change", href="/sector-avg"))
    ] + [
        dbc.NavItem(dbc.NavLink("Top Movers", href="/growth"))
    ] + [
        dbc.NavItem(dbc.NavLink("Volume", href="/volume"))
    ],
    brand="Property Investment Dashboard",
    brand_href="/",  # Assuming home page is at '/'
    color="dark",
    dark=True,
)

# Overall layout
app.layout = html.Div([
    navbar,  # Include the navigation bar
    dash.page_container
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
