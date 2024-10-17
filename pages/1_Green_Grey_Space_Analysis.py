import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configure the app layout and style
st.set_page_config(page_title="Green and Grey Space Analysis", layout='wide', initial_sidebar_state="expanded")

# Page title and description
st.title("🌳 Green and Grey Space Analysis in Rotterdam 🌆")
st.markdown("""
Welcome to the Green and Grey Space Analysis tool! 
This application allows you to visualize the distribution of green and grey spaces in Rotterdam by postcode. 
You can adjust the green space values and compare different postcodes, as well as see how Rotterdam compares to other cities.
""")

# City color palette for differentiation
city_colors = {
    'Amsterdam': '#90EE90',  # Light Green
    'Utrecht': '#3CB371',     # Medium Sea Green
    'The Hague': '#228B22',   # Forest Green
    'Eindhoven': '#32CD32'     # Lime Green
}

# Sample dataset for Rotterdam postcodes
postcodes = [
    '3011', '3012', '3013', '3014', '3015', 
    '3016', '3017', '3021', '3022', '3023', 
    '3024', '3025', '3026', '3031', '3032', 
    '3033', '3034', '3035', '3036', '3041'
]

# Generate random green space percentages ensuring grey space is 100 - green space
np.random.seed(42)  # For reproducibility
green_space_rotterdam = np.random.randint(0, 101, size=len(postcodes))
grey_space_rotterdam = 100 - green_space_rotterdam

# Create DataFrame for Rotterdam
data_rotterdam = {
    'Postcode': postcodes,
    'Green Space (%)': green_space_rotterdam,
    'Grey Space (%)': grey_space_rotterdam,
    'City': 'Rotterdam'
}
df_rotterdam = pd.DataFrame(data_rotterdam)

# Sample dataset for other cities
cities = ['Amsterdam', 'Utrecht', 'The Hague', 'Eindhoven']
data_other_cities = {
    'City': [],
    'Green Space (%)': [],
    'Grey Space (%)': []
}

# Generate mock data for other cities
for city in cities:
    green_space = np.random.randint(0, 101, size=5)
    total_green = green_space.mean()
    data_other_cities['City'].append(city)
    data_other_cities['Green Space (%)'].append(total_green)
    data_other_cities['Grey Space (%)'].append(100 - total_green)

df_other_cities = pd.DataFrame(data_other_cities)

# Streamlit app starts here

# Create a two-column layout for the main overview
col1, col2 = st.columns([2, 1])  # Main column wider, sidebar narrower

# Sidebar layout
st.sidebar.header("Urban Planning Tool")

# Expander for postcode selection
with st.sidebar.expander("Postcode Selection", expanded=True):
    # Select the first postcode from the dropdown
    selected_postcode_1 = st.selectbox("Select the first postcode:", df_rotterdam['Postcode'])

    # Remove the first postcode from the options for the second postcode selection
    available_postcodes_2 = df_rotterdam.loc[df_rotterdam['Postcode'] != selected_postcode_1, 'Postcode']
    selected_postcode_2 = st.selectbox("Select the second postcode (optional):", ['None'] + list(available_postcodes_2))

    # Get the current green space value for the selected first postcode
    current_green_space_1 = df_rotterdam.loc[df_rotterdam['Postcode'] == selected_postcode_1, 'Green Space (%)'].values[0]

    # If a second postcode is selected, get its data
    if selected_postcode_2 != 'None':
        current_green_space_2 = df_rotterdam.loc[df_rotterdam['Postcode'] == selected_postcode_2, 'Green Space (%)'].values[0]
    else:
        current_green_space_2 = None

# Expander for city selection
with st.sidebar.expander("City Selection", expanded=True):
    # Multi-select box for other cities
    selected_cities = st.multiselect("Select other cities to display:", cities)

# Expander for adjusting green space
with st.sidebar.expander("Adjust Green Space", expanded=True):
    # Slider for adjusting the green space for the first postcode
    new_green_space_1 = st.slider(f"Adjust Green Space (%) for postcode {selected_postcode_1}:", 0, 100, current_green_space_1)

# Optional note at the bottom
st.sidebar.markdown("---")
st.sidebar.markdown("<small>**Note**: This tool is a prototype for visualizing green and grey spaces. "
                    "For detailed urban planning insights, please refer to official urban studies and databases.</small>", unsafe_allow_html=True)

# Update grey space based on new green space
new_grey_space_1 = 100 - new_green_space_1

# Create a Plotly scatter plot
fig = px.scatter(df_rotterdam, x='Green Space (%)', y='Grey Space (%)', 
                 hover_name='Postcode', 
                 title='Scatterplot of Green vs Grey Space in Rotterdam',
                 labels={'Green Space (%)': 'Green Space (%)', 'Grey Space (%)': 'Grey Space (%)'},
                 color_discrete_sequence=['#00FF7F'])

# Highlight the first selected postcode
fig.add_scatter(x=[current_green_space_1], y=[100 - current_green_space_1], 
                 mode='markers', 
                 marker=dict(color='red', size=10, line=dict(width=2, color='red')),
                 name=f'Original Postcode: {selected_postcode_1}',
                 hovertemplate=f'{selected_postcode_1}<br>Green Space: {current_green_space_1}%<br>Grey Space: {100 - current_green_space_1}%')

# Highlight the adjusted first postcode only if it's different from the original
if new_green_space_1 != current_green_space_1:
    fig.add_scatter(x=[new_green_space_1], y=[new_grey_space_1], 
                     mode='markers', 
                     marker=dict(color='grey', size=10, line=dict(width=2, color='grey')),
                     name=f'Adjusted Postcode: {selected_postcode_1}',
                     hovertemplate=f'{selected_postcode_1}<br>Green Space: {new_green_space_1}%<br>Grey Space: {new_grey_space_1}%')

# If a second postcode is selected, highlight it
if selected_postcode_2 != 'None':
    fig.add_scatter(x=[current_green_space_2], y=[100 - current_green_space_2], 
                     mode='markers', 
                     marker=dict(color='orange', size=10, line=dict(width=2, color='orange')),
                     name=f'Original Postcode: {selected_postcode_2}',
                     hovertemplate=f'{selected_postcode_2}<br>Green Space: {current_green_space_2}%<br>Grey Space: {100 - current_green_space_2}%')

# If the user selected cities, add them to the plot as aggregated values
for city in selected_cities:
    city_data = df_other_cities[df_other_cities['City'] == city]
    fig.add_scatter(x=[city_data['Green Space (%)'].values[0]], 
                     y=[city_data['Grey Space (%)'].values[0]], 
                     mode='markers', 
                     marker=dict(size=10, opacity=0.6, color=city_colors[city]), 
                     name=city,
                     hovertemplate=f'{city}<br>Green Space: %{{x}}%<br>Grey Space: %{{y}}%')

# Update layout to improve clarity
fig.update_layout(xaxis=dict(range=[0, 100]), yaxis=dict(range=[0, 100]), showlegend=True)
fig.update_traces(marker=dict(opacity=0.7))

with col1:
    # Display the plot in Streamlit
    st.plotly_chart(fig)

with col2:
    # Dynamic statistics section
    st.header("Statistics")
    
    # Overall statistics for Rotterdam
    avg_green_space = df_rotterdam['Green Space (%)'].mean()
    avg_grey_space = df_rotterdam['Grey Space (%)'].mean()

    # Dynamic statistics based on selected postcodes
    selected_postcodes = [selected_postcode_1]
    if selected_postcode_2 != 'None':
        selected_postcodes.append(selected_postcode_2)

    avg_selected_green_space = df_rotterdam[df_rotterdam['Postcode'].isin(selected_postcodes)]['Green Space (%)'].mean()
    avg_selected_grey_space = 100 - avg_selected_green_space

    # Get green space values for both selected postcodes
    green_space_1 = df_rotterdam.loc[df_rotterdam['Postcode'] == selected_postcode_1, 'Green Space (%)'].values[0]
    grey_space_1 = 100 - green_space_1

    if selected_postcode_2 != 'None':
        green_space_2 = df_rotterdam.loc[df_rotterdam['Postcode'] == selected_postcode_2, 'Green Space (%)'].values[0]
        grey_space_2 = 100 - green_space_2

    # Provide insights based on averages for the first postcode
    if avg_selected_green_space > avg_green_space:
        st.success("The selected postcode has a higher average green space than the overall average in Rotterdam. [Discover ways to contribute!](#make-an-impact-on-green-spaces)")
    elif avg_selected_green_space < avg_green_space:
        st.warning("The selected postcode has a lower average green space than the overall average in Rotterdam. [Explore actions you can take!](#make-an-impact-on-green-spaces)")
    else:
        st.info("The selected postcode has the same average green space as the overall average in Rotterdam. [Learn how to enhance green spaces!](#make-an-impact-on-green-spaces)")

    # Additional insights if a second postcode is selected
    if selected_postcode_2 != 'None':
        st.markdown("### Comparison Between Selected Postcodes 📊")
        if green_space_1 > green_space_2:
            st.success(f"Postcode {selected_postcode_1} has a **higher green space** of **{green_space_1}%** compared to postcode {selected_postcode_2} with **{green_space_2}%**.")
        elif green_space_1 < green_space_2:
            st.warning(f"Postcode {selected_postcode_1} has a **lower green space** of **{green_space_1}%** compared to postcode {selected_postcode_2} with **{green_space_2}%**.")
        else:
            st.info(f"Both postcodes have the **same green space** of **{green_space_1}%**.")

        # Add insights about the impact of changes based on comparison
        st.markdown("### Opportunities for Improvement 🌱")
        if green_space_1 < green_space_2:
            st.markdown(f"You can help increase the green space in postcode {selected_postcode_1} by taking actions such as planting trees or creating green roofs.")
        elif green_space_1 > green_space_2:
            st.markdown(f"Postcode {selected_postcode_1} is doing well! To maintain or enhance its green space, consider encouraging community initiatives.")

# Combined information and actions to improve green spaces
st.markdown("<a id='make-an-impact-on-green-spaces'></a>", unsafe_allow_html=True)
st.markdown("### Make an Impact on Green Spaces 🌿")

st.markdown("""
You have the power to influence the amount of green space in your postcode! Here are some ways you can contribute:
- **Install a Green Roof**: Changing your roof to a green roof can increase your postcode's green space by **5-15%**, depending on the size of the roof.
- **Plant Trees**: Planting just **one tree** can increase green space by approximately **1%** in your area. A small community initiative planting **10 trees** could add **10%** to your postcode's green coverage.
- **Create Urban Gardens**: Transforming unused land into community gardens can increase green space by **20-30%** per garden, depending on the size and number of plants.
- **Support Local Parks**: Advocating for the development of a local park can add **15-40%** green space to your community, based on the park's size.
- **Engage in Clean-Up Campaigns**: Keeping existing green areas clean and well-maintained can enhance their usability and attractiveness, potentially increasing the effective green space by **5-10%** as more people use these areas.

### Take Action to Increase Green Spaces

By making simple changes and encouraging others to do the same, you can help enhance the green coverage in your area, contributing to a healthier, more sustainable environment.

**Every action counts towards creating a greener, healthier community!** 🌍
""")
