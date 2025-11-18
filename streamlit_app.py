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
    
    
st.text_input("Enter an address:", value ="Skaldevägen 60", key="address")
go_input = st.button("Go!", key="go_btn")


if go_input:
    
    if st.session_state.address:
        
        location = geocode_address(st.session_state.address)
    
        lat, lon = location
        st.session_state.location = location  # Save coordinates in session_state
        #st.write(f"Coordinates: {lat}, {lon}")



#Output
st.write("Outputs")
st.write("Button value:", go_input)
if st.session_state.location:
    st.write(st.session_state.location)

