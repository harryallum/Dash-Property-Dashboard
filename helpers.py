import pandas as pd
import plotly.express as px
import numpy as np
import json
from config import app_config
import plotly.graph_objs as go

# Define the GeoJSON data globally
geojson_data = None
current_selected_region = None

# Read GeoJSON file for the selected region
def read_geojson(selected_region):
    global geojson_data
    global current_selected_region

    if current_selected_region != selected_region or geojson_data is None:
        geojson_file_path = f'geo_json/regions/{selected_region}_postcode_sectors.geojson'
        with open(geojson_file_path, 'r') as geojson_file:
            geojson_data = json.load(geojson_file)
        current_selected_region = selected_region

    return geojson_data

def update_map(selected_year, selected_region):
    # Load the CSV file based on the selected year
    csv_file_path = f'processed_data/average_price_by_year/region_data_{selected_year}.csv'
    data = pd.read_csv(csv_file_path)

    # Filter the data to the selected region
    data = data[data['region'] == selected_region]

    # Check if geojson is loaded for the selected region, load if not
    read_geojson(selected_region)

    key_min = np.percentile(data.avg_price, 5)
    key_max = np.percentile(data.avg_price, 95)

    # Fetch the configuration for the selected region
    region_config = app_config['regions'][selected_region]

    # Create choropleth map using Plotly Express
    fig = px.choropleth_mapbox(
        data,
        geojson=geojson_data,
        locations='postcode_sector',
        featureidkey='properties.name',
        color='avg_price',
        color_continuous_scale='Viridis',
        mapbox_style='carto-positron',
        range_color=[key_min, key_max],
        center=region_config['center'],
        zoom=region_config['zoom'],
        opacity=0.5,
        labels={'avg_price': 'Average Price £'},
        title=f'Average price by postcode sector for {selected_region} in {selected_year}',
        hover_data={'volume': True},
    )

    # Set the dark background color
    fig.update_layout(
        mapbox=dict(style='carto-positron'),
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        font_color='white'
    )

    return fig

def update_bar_plot(selected_year,selected_region):
    # Load the preprocessed CSV containing average prices and volumes
    csv_file_path = 'processed_data/region_avg_price/region_avg_prices.csv'
    data = pd.read_csv(csv_file_path)

    # Filter the data for the selected region
    data = data[data['region'] == selected_region]

    # Aggregate volume by year
    aggregated_data = data.groupby('year')['volume'].sum().reset_index()

    # Create stacked bar plot using Plotly Express
    fig = px.bar(
        data,
        x='year',
        y='avg_price',
        color='property_type',
        title=f'Average price and sales volume for {selected_region} in {selected_year}',
        barmode='stack',  # Set the barmode to 'stack' for stacked bars
    )

    # Add a line plot for the aggregated 'volume' over the top of the bar plot
    fig.add_trace(
        go.Scatter(x=aggregated_data['year'], y=aggregated_data['volume'], name='Volume', yaxis='y2', mode='lines+markers')
    )

    # Update layout
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Average Price /£',
        yaxis2=dict(title='Volume',overlaying='y',showgrid=False, side='right'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
        font_color='white'
    )

    return fig

def update_price_change(selected_year, selected_region):
    # Load the CSV file with price change data based on the selected year
    csv_file_path = f'processed_data/avg_price_delta/avg_price_delta_{selected_year}.csv'
    data = pd.read_csv(csv_file_path)

    # Filter the data to the selected region
    data = data[data['region'] == selected_region]

    # Fetch the configuration for the selected region
    region_config = app_config['regions'][selected_region]

    # Check if geojson is loaded for the selected region, load if not
    read_geojson(selected_region)

    key_min = np.percentile(data.delta, 5)
    key_max = np.percentile(data.delta, 98)

    # Create choropleth map using Plotly Express
    fig = px.choropleth_mapbox(
        data,
        geojson=geojson_data,
        locations='postcode_sector',
        featureidkey='properties.name',
        color='delta',
        color_continuous_scale='Viridis',
        mapbox_style='carto-positron',
        center=region_config['center'],
        zoom=region_config['zoom'],
        opacity=0.5,
        labels={'delta': 'Price Change (%)'},
        title=f'Year-on-year average price change for {selected_region} in {selected_year}',
        range_color=(key_min,key_max),
    )

    # Set the dark background color
    fig.update_layout(
        mapbox=dict(style='carto-positron'),
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        font_color='white'
    )

    return fig

def update_price_change_boxplot(selected_year,selected_region):
    start_year = int(selected_year) - 2
    end_year = int(selected_year) + 1

    # Create an empty list to store DataFrames
    all_data = []

    for year in range(start_year, end_year):
        # Load the preprocessed csvs with price change data for each year
        csv_file_path = f'processed_data/avg_price_delta/avg_price_delta_{year}.csv'
        year_data = pd.read_csv(csv_file_path)

        # Append the DataFrame to the list
        all_data.append(year_data)

    # Concatenate all DataFrames in the list
    data = pd.concat(all_data, ignore_index=True)

    # Filter the data to the selected region
    data = data[data['region'] == selected_region]

    y_min = np.percentile(data.delta, 1)
    y_max = np.percentile(data.delta, 99)

    # Create box plot using Plotly Express
    fig = px.box(
        data,
        x='year',
        y='delta',
        title=f'Year-on-year sector average price change for {selected_region} between {start_year} and {selected_year}',
        labels={'delta': 'Price Change (%)'},
        color='year',
        range_y=[y_min, y_max],
    )

    # Update layout
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Price Change (%)',
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
        font_color='white'
    )

    return fig

def update_fastest_growing_plot(selected_year, selected_region,slider_value):
    # Load the CSV file with price change data based on the selected year
    csv_file_path = f'processed_data/avg_price_delta/avg_price_delta_{selected_year}.csv'
    data = pd.read_csv(csv_file_path)

    # Filter the data to the selected region
    data = data[data['region'] == selected_region]

    # Sort the data by the 'delta' column in descending order
    data = data.sort_values('delta', ascending=False)

    # Select the top 10 rows
    top_10_data = data.head(slider_value)

    # Fetch the configuration for the selected region
    region_config = app_config['regions'][selected_region]

    # Check if geojson is loaded for the selected region, load if not
    read_geojson(selected_region)

    # Create choropleth map using Plotly Express
    fig = px.choropleth_mapbox(
        top_10_data,
        geojson=geojson_data,
        locations='postcode_sector',
        featureidkey='properties.name',
        color='delta',
        color_continuous_scale='Viridis',
        mapbox_style='carto-positron',
        center=region_config['center'],
        zoom=region_config['zoom'],
        opacity=0.5,
        labels={'delta': 'Price Change (%)'},
        title= f'Top {slider_value} fastest growing sectors in {selected_region} in {selected_year}'
    )

    # Set the dark background color
    fig.update_layout(
        mapbox=dict(style='carto-positron'),
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        font_color='white'
    )

    return fig

def update_fastest_declining_plot(selected_year, selected_region, slider_value):
    # Load the CSV file with price change data based on the selected year
    csv_file_path = f'processed_data/avg_price_delta/avg_price_delta_{selected_year}.csv'
    data = pd.read_csv(csv_file_path)

    # Filter the data to the selected region
    data = data[data['region'] == selected_region]

    # Sort the data by the 'delta' column in descending order
    data = data.sort_values('delta', ascending=False)

    # Select the top 10 rows
    top_10_data = data.tail(slider_value)

    # Fetch the configuration for the selected region
    region_config = app_config['regions'][selected_region]

    # Check if geojson is loaded for the selected region, load if not
    read_geojson(selected_region)

    # Create choropleth map using Plotly Express
    fig = px.choropleth_mapbox(
        top_10_data,
        geojson=geojson_data,
        locations='postcode_sector',
        featureidkey='properties.name',
        color='delta',
        color_continuous_scale='Viridis',
        mapbox_style='carto-positron',
        center=region_config['center'],
        zoom=region_config['zoom'],
        opacity=0.5,
        labels={'delta': 'Price Change (%)'},
        title= f'Top {slider_value} fastest declining sectors in {selected_region} in {selected_year}'
    )

    # Set the dark background color
    fig.update_layout(
        mapbox=dict(style='carto-positron'),
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        font_color='white'
    )

    return fig

def update_volume_plot(selected_year, selected_region):
    # Load data
    csv_file_path = f'processed_data/volume_by_year/region_total_volume_{selected_year}.csv'
    data = pd.read_csv(csv_file_path)

    fig = px.line(data,
                  x='month',
                  y='volume',
                  color='region',
                  markers=True,
                  title=f'Volume trend for all regions in {selected_year} by month')
    
    # Update layout
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Volume',
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
        font_color='white'
    )

    return fig

def update_volume_map(selected_year, selected_region):
    # Load the CSV file based on the selected year
    csv_file_path = f'processed_data/average_price_by_year/region_data_{selected_year}.csv'
    data = pd.read_csv(csv_file_path)

    # Filter the data to the selected region
    data = data[data['region'] == selected_region]

    # Check if geojson is loaded for the selected region, load if not
    read_geojson(selected_region)

    # Fetch the configuration for the selected region
    region_config = app_config['regions'][selected_region]

    key_min = np.percentile(data.volume, 1)
    key_max = np.percentile(data.volume, 99)

    # Create choropleth map using Plotly Express
    fig = px.choropleth_mapbox(
        data,
        geojson=geojson_data,
        locations='postcode_sector',
        featureidkey='properties.name',
        color='volume',
        color_continuous_scale='Viridis',
        range_color= [key_min,key_max],
        mapbox_style='carto-positron',
        center=region_config['center'],
        zoom=region_config['zoom'],
        opacity=0.5,
        labels={'volume': 'Volume'},
        title=f'Volume by postcode sector for {selected_region} in {selected_year}',
        hover_data={'volume': True},
    )

    # Set the dark background color
    fig.update_layout(
        mapbox=dict(style='carto-positron'),
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        font_color='white'
    )

    return fig