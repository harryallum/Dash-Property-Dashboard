import dash
from dash import html
import dash_bootstrap_components as dbc

# Create the dash app
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SLATE, '/assets/custom.css'])

# Define the navigation bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Price", href="/")),
        dbc.NavItem(dbc.NavLink("Price Change", href="/sector-avg")),
        dbc.NavItem(dbc.NavLink("Top Movers", href="/growth")),
        dbc.NavItem(dbc.NavLink("Volume", href="/volume")),
    ],
    brand="Property Investment Dashboard",
    brand_href="/",
    color="dark",
    dark=True,
)

footer = dbc.Container(
    dbc.Row(
        [
            dbc.Col(html.A("Harry Allum | GitHub", href="https://github.com/harryallum/Dash-Property-Dashboard"), align="left"),
        ],
    ),
    className="footer",
    fluid=True,
)

# Overall layout
app.layout = html.Div([
    navbar,  # Include the navigation bar
    dash.page_container,
    footer,  # Include the footer
])

# Run the dash app
if __name__ == '__main__':
    app.run_server(debug=True)
