import geopandas as gpd
import folium
import streamlit as st
from streamlit_folium import st_folium

# Streamlit app setup
st.set_page_config(page_title="Интерактивная карта Казаиту", layout="wide")
st.title("Интерактивная карта университета Казаиту")
st.markdown("Это карта отображает корпуса университета Казаиту.")

# Manual data for campus locations
manual_data = [
    {"name": "Главный корпус", "type": "корпус", "latitude": 51.186920 , "longitude": 71.409717},
    {"name": "Био корпус", "type": "корпус", "latitude":51.187944, "longitude": 71.409579},
    {"name": "Старый тех корпус", "type": "корпус", "latitude": 51.187625,  "longitude": 71.411373},
    {"name": "Новый тех корпус", "type": "корпус", "latitude": 51.187086, "longitude":  71.411717},
    {"name": "Военная кафедра", "type": "корпус", "latitude": 51.187306, "longitude": 71.410942},
    {"name": "Управление Земельными Ресурсами Архитектура и Дизайн", "type": "корпус", "latitude": 51.186499, "longitude": 71.415311},
    {"name": "Общежитие 7", "type": "здание", "latitude": 51.186302,  "longitude":71.412643},
    {"name": "Поликлинника/Общежитие 2А", "type": "здание", "latitude": 51.186364, "longitude": 71.413280},
    {"name": "Агрономический корпус", "type": "корпус", "latitude": 51.185989, "longitude": 71.410354}
]

# Convert manual data to GeoDataFrame
gdf = gpd.GeoDataFrame(manual_data, geometry=gpd.points_from_xy([d['longitude'] for d in manual_data], [d['latitude'] for d in manual_data]))

# Define icons for different types of buildings
def get_icon(building_type):
    if building_type == "корпус":
        return "university"
    elif building_type == "здание":
        return "home"
    else:
        return "info-sign"

# Sidebar search for campus
st.sidebar.header("Search Options")
search_query = st.sidebar.text_input("Search for a Campus Location")
filtered_gdf = gdf[gdf['name'].str.contains(search_query, case=False)] if search_query else gdf

# Step 3: Visualize Map
campus_map = folium.Map(location=[gdf.geometry.y.mean(), gdf.geometry.x.mean()], zoom_start=15, tiles='OpenStreetMap')

for _, row in filtered_gdf.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=folium.Popup(f"<b>{row['name']}</b><br>Type: {row['type']}", max_width=250),
        tooltip=row['name'],
        icon=folium.Icon(icon=get_icon(row['type']), color="blue")
    ).add_to(campus_map)

# Render map in Streamlit
st_folium(campus_map, width=700, height=500)

# Optional Step: Interactivity
st.sidebar.header("Map Options")
building_filter = st.sidebar.text_input("Filter by Building Name")
if building_filter:
    filtered_gdf_by_name = gdf[gdf['name'].str.contains(building_filter, case=False)]
    st.write("Filtered Results:", filtered_gdf_by_name[['name', 'type']])
else:
    st.write("Displaying all locations.")

# Step 4: Document Work
st.markdown("""
### Project Documentation
- **Libraries Used:**
    - Geopandas for geospatial data processing
    - Folium for interactive map rendering
    - Streamlit for web-based visualization
    - Streamlit-Folium for Folium map integration
- **Manual Data Provided:** Key buildings and points of interest on campus
- **Instructions:**
    1. Explore the interactive map.
    2. Use the sidebar to filter or search for specific buildings.
""")
