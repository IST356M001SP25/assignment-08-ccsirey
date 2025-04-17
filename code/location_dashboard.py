'''
location_dashboard.py
'''
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import streamlit_folium as sf
st.set_page_config(layout="wide")

df = pd.read_csv('./cache/tickets_in_top_locations.csv')

locations = df['location'].unique()


selected_location = st.selectbox("Choose a location", sorted(locations))


filtered = df[df['location'] == selected_location]

# Layout columns
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Tickets", value=len(filtered))

with col2:
    st.metric("Total Fines ($)", value=filtered['amount'].sum())

col3, col4 = st.columns(2)

with col3:
    st.subheader("Tickets by Day of Week")
    day_counts = filtered['dayofweek'].value_counts().reindex([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ]).fillna(0)
    st.bar_chart(day_counts)

with col4:
    st.subheader("Tickets by Hour")
    hour_counts = filtered['hourofday'].value_counts().sort_index()
    st.bar_chart(hour_counts)

# Map
st.subheader("Map of Selected Location")
lat = filtered['lat'].iloc[0]
lon = filtered['lon'].iloc[0]
m = folium.Map(location=(lat, lon), zoom_start=17)
folium.Marker(location=(lat, lon), popup=selected_location).add_to(m)
sf.folium_static(m, width=700, height=500)