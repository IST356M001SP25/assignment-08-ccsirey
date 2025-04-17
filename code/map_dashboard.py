'''
map_dashboard.py
'''
import streamlit as st
import streamlit_folium as sf
import folium
import pandas as pd
import geopandas as gpd
# these constants should help you get the map to look better
# you need to figure out where to use them
CUSE = (43.0481, -76.1474)  # center of map
ZOOM = 14                   # zoom level
VMIN = 1000                 # min value for color scale
VMAX = 5000                 # max value for color scale

df = pd.read_csv('./cache/top_locations_mappable.csv')

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat), crs="EPSG:4326")

# Set up Streamlit UI
st.title("Syracuse Parking Violations Over $1,000")

# Create base folium map
m = folium.Map(location=CUSE, zoom_start=ZOOM, tiles="CartoDB positron")

# Explore with custom styling
cuse_map = gdf.explore(
    column='amount',
    cmap='inferno',                  # Slight variation from "magma"
    vmin=VMIN,
    vmax=VMAX,
    legend=True,
    legend_kwds={'caption': 'Total Fine Amount ($)'},
    marker_type='circle',
    marker_kwds={
        'radius': 8,
        'fill': True,
        'color': '#555555',          # circle border color
        'fill_opacity': 0.7
    },
    m=m
)

# Display in Streamlit
sf.folium_static(cuse_map, width=850, height=600)
