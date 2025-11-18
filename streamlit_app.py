import streamlit as st
import folium
from streamlit_folium import st_folium
#from geopy.geocoders import Nominatim
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import plotly.express as px
import networkx as nx
import xlrd

#from folium import GeoJson, GeoJsonTooltip

import requests
import time
import branca.colormap as cm# 8. Create a linear color scale for grade_abs
from opencage.geocoder import OpenCageGeocode


# Load OpenCage API key from Streamlit secrets
OPENCAGE_KEY = st.secrets["opencage"]["api_key"]

# Initialize the geocoder
geocoder = OpenCageGeocode(OPENCAGE_KEY)

def geocode_address(address):
    # geolocator = Nominatim(user_agent="Navigator")
    # return geolocator.geocode(address)
    results = geocoder.geocode(address)
    lat = results[0]['geometry']['lat']
    lon = results[0]['geometry']['lng']
    return lat, lon


st.set_page_config(page_title="Relocation Navigator",
                   layout="wide",
                   initial_sidebar_state="collapsed")

st.title("Relocation Navigator")
st.write("App started at:", time.time())

# Initialize session state variables if they don't exist
if "location" not in st.session_state:
    st.session_state.location = None
if "map" not in st.session_state:
    st.session_state.map = None    
if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True
    
st.text_input("Enter an address:", value ="Skaldevägen 60", key="address")
st.slider('Show PoIs within:', min_value=100, max_value=2000, value=500, key="POI_radius")
go_input = st.button("Go!", on_click=click_button)


if st.session_state.clicked:
    
    if st.session_state.address:
        
        location = geocode_address(st.session_state.address)
        #lat, lon = location
        
        st.session_state.location = geocode_address(st.session_state.address)  # Save coordinates in session_state
        #st.write(f"Coordinates: {lat}, {lon}")
        
        # Map
        
        m = folium.Map(location=st.session_state.location, zoom_start=14)         
        # Add address marker
        folium.Marker(location, popup=st.session_state.address, icon=folium.Icon(color='red', icon='home')).add_to(m)
        folium.Circle(
            location=location,
            radius=st.session_state.POI_radius,  # in meters
            color='black',       
            fill=False,
            weight=2.5            
            ).add_to(m)
         
        st.session_state.map = m


#Output
st.write("Button value:", go_input)
if st.session_state.location:
    st.write(st.session_state.location)
    st_folium(st.session_state.map, width=700, height=500)
    
