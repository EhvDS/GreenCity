import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import shape
from streamlit_folium import st_folium
import json
import matplotlib

# Load the enriched neighborhood data with geometries
data_path = "data/Neighborhoods_Eindhoven.csv"  # Ensure the path is correct
df = pd.read_csv(data_path)

# Convert the 'geometry' column back to dictionary format using json.loads if necessary
df['geometry'] = df['geometry'].apply(json.loads)

# Use shapely's shape function to convert GeoJSON geometries to shapely geometries
df['geometry'] = df['geometry'].apply(shape)

# Create a GeoDataFrame with the geometry column
gdf = gpd.GeoDataFrame(df, geometry='geometry', crs='EPSG:4326')

# Sidebar for selecting neighborhood and adjusting variables
st.sidebar.title("🌿 Adjust Urban Parameters")
selected_neighborhood = st.sidebar.selectbox('🏙️ Select a Neighborhood', gdf['Neighborhood'])

# Filter data for the selected neighborhood
neighborhood_data = gdf[gdf['Neighborhood'] == selected_neighborhood].iloc[0]

# Slider for adjusting green space and housing space
green = st.sidebar.slider('🌳 Public Green Space (%)', 0, 100, int(neighborhood_data['G']))
# Housing automatically adjusts to ensure that green + housing = 100%
housing = 100 - green
st.sidebar.write(f'Housing Area: {100 - green}%')

# Update the AQI, temperature, and population density based on the selected values
aqi = 50 - 0.3 * green
temperature = 30 - 0.2 * green

# Convert population density to people per square km, assume a standard area size for simplicity
density = max(0, (neighborhood_data['Population'] / housing) * 100) if housing > 0 else float('nan')

# Title and catchy explanation
st.title('🌍 Urban Planning Dashboard')
st.subheader("Visualize and adjust urban development scenarios in Eindhoven.")
st.markdown("""
    Explore the impact of urban planning on the environment by selecting a neighborhood and adjusting the proportions of green space and housing area.
    """)

# Explanation of AQI scale, specific to Eindhoven
st.markdown("""
    **Air Quality Index (AQI) Range for Eindhoven:**
    - **35:** Best Air Quality (🟢)
    - **44:** Worst Air Quality (🔴)
    """)

# Display the selected neighborhood's initial data with improved formatting
st.markdown(f"### 📊 Current Data for {selected_neighborhood}:")
st.markdown(f"**Green Space:** {neighborhood_data['G']}%")
st.markdown(f"**Housing Area:** {neighborhood_data['H']}%")
st.markdown(f"**Air Quality Index:** {neighborhood_data['AQI']} AQI")
st.markdown(f"**Average Temperature:** {neighborhood_data['T']} °C")
st.markdown(f"**Population Density:** {neighborhood_data['D']:.2f} people per square km")

# Display the adjusted values after changing the sliders
st.markdown("### 🔍 Adjusted Values:")
st.markdown(f"**Estimated Air Quality Index:** {aqi:.2f} AQI")
st.markdown(f"**Estimated Average Temperature:** {temperature:.1f} °C")
st.markdown(f"**Estimated Population Density:** {density:.2f} people per square km")

# Create a base map centered around Eindhoven
m = folium.Map(location=[51.4416, 5.4697], zoom_start=12)

# Define the specific AQI range for Eindhoven
min_aqi = 35  # Best AQI
max_aqi = 44  # Worst AQI

# Function to generate a gradient color based on AQI
def get_color(aqi_value):
    norm = matplotlib.colors.Normalize(vmin=min_aqi, vmax=max_aqi)
    cmap = matplotlib.cm.get_cmap('RdYlGn_r')  # Red to green gradient (reversed)
    color = matplotlib.colors.to_hex(cmap(norm(aqi_value)))
    return color

# Update the AQI value for the selected neighborhood in the GeoDataFrame
gdf.loc[gdf['Neighborhood'] == selected_neighborhood, 'AQI'] = aqi

# Add neighborhoods to the map with a gradient color based on AQI
for _, row in gdf.iterrows():
    folium.GeoJson(
        row['geometry'],
        style_function=lambda x, aqi=row['AQI']: {
            'fillColor': get_color(aqi),
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.7,
        },
        tooltip=folium.Tooltip(f"{row['Neighborhood']}: {row['AQI']:.2f} AQI"),
    ).add_to(m)

# Display the map using Streamlit
st_folium(m, width=700, height=500)
