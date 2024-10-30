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

# Convert the 'geometry' column back to dictionary format if necessary
df['geometry'] = df['geometry'].apply(json.loads)
df['geometry'] = df['geometry'].apply(shape)

# Create a GeoDataFrame with the geometry column
gdf = gpd.GeoDataFrame(df, geometry='geometry', crs='EPSG:4326')

# Initial Instruction
st.info("Welcome to the Urban Planning Dashboard! Start by selecting a neighborhood from the sidebar to explore and adjust urban planning scenarios in Eindhoven.")

# Sidebar for selecting neighborhood and adjusting variables
st.sidebar.title("🌿 Adjust Urban Parameters")
selected_neighborhood = st.sidebar.selectbox('🏙️ Select a Neighborhood', gdf['Neighborhood'])

# Filter data for the selected neighborhood
neighborhood_data = gdf[gdf['Neighborhood'] == selected_neighborhood].iloc[0]

# Slider for adjusting green space and housing space
green = st.sidebar.slider('🌳 Public Green Space (%)', 0, 100, int(neighborhood_data['G']))
housing = 100 - green
st.sidebar.write(f'Housing Area: {housing}%')

# Calculate updated AQI, temperature, and population density
aqi = 50 - 0.3 * green
temperature = 30 - 0.2 * green

# Get the current data for comparison
current_aqi = neighborhood_data['AQI']
current_temperature = neighborhood_data['T']
current_density = neighborhood_data['D']

# Define helper function to format values with color and arrow
def format_change(value, current_value, is_higher_better):
    if isinstance(value, str) or isinstance(current_value, str):
        return value
    arrow_up = "↑"
    arrow_down = "↓"
    if value < current_value:
        color = "red" if is_higher_better else "green"
        arrow = arrow_up if is_higher_better else arrow_down
    elif value > current_value:
        color = "green" if is_higher_better else "red"
        arrow = arrow_down if is_higher_better else arrow_up
    else:
        return f"**{value:.2f}**"
    return f"<span style='color:{color}; font-weight:bold;'>{value:.2f} {arrow}</span>"

# Handle population density to avoid NaN
if housing > 0:
    density = (neighborhood_data['Population'] / housing) * 2
else:
    density = "No Population"

# Title and explanation
st.title('🌍 Urban Planning Dashboard')
st.subheader("Visualize and adjust urban development scenarios in Eindhoven.")
st.markdown("by Momchil Valkov")
st.markdown("""
    <hr>
            
    ### 🌳 How to Use This Dashboard:
    **Step 1**: Select a neighborhood from the sidebar.
    
    **Step 2**: Adjust the **Public Green Space** slider to see how changing the green space affects:
      - 💨 **Air Quality Index (AQI)** – A lower AQI means cleaner air! The map color will adjust automatically based on air quality. Lower AQI leads to better air quality - 🟢, higher is worse 🔴.
      - 🌡️ **Temperature** – More green space can help cool the area!
      - 🏠 **Population Density** – Changes in housing area will impact population density.

    ### 🔍 Data Sections:
    **📊 Current Data**: This section shows the existing conditions in your selected neighborhood.
    
    **🔍 Adjusted Values**: After adjusting the green space slider, this section will show the updated values.
    
    **Arrows**: 🟢⬇️ for improvements, 🔴⬆️ for negative changes.
    """, unsafe_allow_html=True)

# Display the initial and adjusted data
st.markdown(f"### 📊 Current Data for {selected_neighborhood}:")
st.markdown(f"**Green Space:** {neighborhood_data['G']}%")
st.markdown(f"**Housing Area:** {neighborhood_data['H']}%")
st.markdown(f"**Air Quality Index:** {neighborhood_data['AQI']} AQI")
st.markdown(f"**Average Temperature:** {neighborhood_data['T']} °C")
st.markdown(f"**Population Density:** {neighborhood_data['D']:.2f} people per square km")

# Adjusted Values with comparison indicators
st.markdown("### 🔍 Adjusted Values:")
st.markdown(f"**Estimated Air Quality Index:** {format_change(aqi, current_aqi, is_higher_better=False)} AQI", unsafe_allow_html=True)
st.markdown(f"**Estimated Average Temperature:** {format_change(temperature, current_temperature, is_higher_better=False)} °C", unsafe_allow_html=True)
st.markdown(f"**Estimated Population Density:** {format_change(density, current_density, is_higher_better=False)} people per square km", unsafe_allow_html=True)

# Create a static map centered around Eindhoven with no reloads on zoom
m = folium.Map(location=[51.4416, 5.4697], zoom_start=12, control_scale=True, no_touch=True)

# Define the AQI range for the color gradient
min_aqi = 35
max_aqi = 44

# Function to generate color based on AQI
def get_color(aqi_value):
    norm = matplotlib.colors.Normalize(vmin=min_aqi, vmax=max_aqi)
    cmap = matplotlib.cm.get_cmap('RdYlGn_r')
    color = matplotlib.colors.to_hex(cmap(norm(aqi_value)))
    return color

# Update AQI value for the selected neighborhood in the GeoDataFrame
gdf.loc[gdf['Neighborhood'] == selected_neighborhood, 'AQI'] = aqi

# Highlight the selected neighborhood with a purple outline
for _, row in gdf.iterrows():
    style = {
        'fillColor': get_color(row['AQI']),
        'color': 'blue' if row['Neighborhood'] == selected_neighborhood else 'black',
        'weight': 5 if row['Neighborhood'] == selected_neighborhood else 0.5,  # Thicker outline for the selected neighborhood
        'fillOpacity': 0.7,
    }
    folium.GeoJson(
        row['geometry'],
        style_function=lambda x, style=style: style,
        tooltip=folium.Tooltip(f"{row['Neighborhood']}: {row['AQI']:.2f} AQI"),
    ).add_to(m)


# Adjust map zoom to the selected neighborhood
if selected_neighborhood:
    bounds = gdf[gdf['Neighborhood'] == selected_neighborhood].geometry.bounds.values[0]
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

# Display the static map
st_folium(m, width=700, height=500)
