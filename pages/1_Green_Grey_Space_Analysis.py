import streamlit as st
import pandas as pd
import plotly.express as px

# Configure the app layout and style
st.set_page_config(page_title="Green Space Analysis", layout='wide', initial_sidebar_state="expanded")

# Page title and description
st.title("🌳 Green Space Analysis in Rotterdam 🌆")
st.markdown("""
Welcome to the Green Space Analysis tool! 
This application allows you to visualize the distribution of green in Rotterdam by postal code. 
You can adjust the green space values and compare different postcodes.
""")

# Load the dataset
df_rotterdam = pd.read_csv('data/PC4_TreesBushesGrass.csv', delimiter=';')

# Streamlit app starts here
col1, col2 = st.columns([2, 1])  # Main column wider, sidebar narrower

# Sidebar layout
st.sidebar.header("Urban Planning Tool")

# Expander for postcode selection
with st.sidebar.expander("Postal code Selection", expanded=True):
    selected_postcode_1 = st.selectbox("Select the first postal code:", df_rotterdam['Postcode'])
    available_postcodes_2 = df_rotterdam.loc[df_rotterdam['Postcode'] != selected_postcode_1, 'Postcode']
    selected_postcode_2 = st.selectbox("Select the second postal code (optional):", ['None'] + list(available_postcodes_2))

with st.sidebar.expander("Surrounding postal code Selection", expanded=False):
    st.write(
        "Use the slider below to select the number of surrounding postcodes you wish to display. "
        "This allows you to customize the view based on how many nearby postcodes you want to consider."
    )
    # Slider for selecting the number of surrounding postcodes
    surrounding_count = st.slider(
        "Select number of surrounding postal codes to display:",
        min_value=0,
        max_value=len(df_rotterdam),
        step=1,  # Change step to 1 for more granular control
        value=len(df_rotterdam)  # Default value set to the total number of postcodes
    )

# Create a sorted list of unique postcodes
sorted_postcodes = sorted(df_rotterdam['Postcode'].unique())

# Find the index of the selected postcode
selected_index = sorted_postcodes.index(selected_postcode_1)

# Calculate the start and end indices for surrounding postcodes
start_index = max(selected_index - surrounding_count, 0)
end_index = min(selected_index + surrounding_count + 1, len(sorted_postcodes))

# Filter the DataFrame to include only the selected postcode and the surrounding ones
surrounding_postcodes = sorted_postcodes[start_index:end_index]  # Remove .tolist()
df_rotterdam = df_rotterdam[df_rotterdam['Postcode'].isin(surrounding_postcodes)]

# print(len(df_filtered))

# Filter the DataFrame based on selected postcodes
df_filtered = df_rotterdam[df_rotterdam['Postcode'] != selected_postcode_1]
if selected_postcode_2 != 'None':
    df_filtered = df_filtered[df_filtered['Postcode'] != selected_postcode_2]

selected_row_1 = df_rotterdam.loc[df_rotterdam['Postcode'] == selected_postcode_1]
size_value_1 = float(selected_row_1['PercentageBushes'].values[0])
selected_green_space_trees = int(selected_row_1['PercentageTrees'].values[0])
selected_green_space_grass = int(selected_row_1['PercentageGrass'].values[0])
selected_green_space_bushes = int(selected_row_1['PercentageBushes'].values[0])

# Expander for adjusting green space
with st.sidebar.expander(f"Adjust Green Space (Postal code: {selected_postcode_1})", expanded=False):
    new_green_space_trees = st.slider("Adjust the percentage of Trees:", 0, 100, selected_green_space_trees)
    new_green_space_grass = st.slider("Adjust the percentage of Grass:", 0, 100, selected_green_space_grass)
    new_green_space_bushes = st.slider("Adjust the percentage of Bushes:", 0, 100, selected_green_space_bushes)

# Optional note at the bottom
st.sidebar.markdown("---")
st.sidebar.markdown("<small>**Note**: This tool is a prototype for visualizing greenness in Rotterdam. "
                    "For detailed urban planning insights, please refer to official urban studies and databases.</small>", unsafe_allow_html=True)

max_size = df_filtered['PercentageBushes'].max()
# Create a Plotly scatter plot
fig = px.scatter(df_filtered, x='PercentageTrees', y='PercentageGrass', 
                 hover_name='Postcode', 
                 size='PercentageBushes',
                 size_max=max_size,
                 title='Scatterplot of Green in Rotterdam',
                 labels={'PercentageTrees': 'Trees (%)', 'PercentageBushes': 'Bushes (%)', 'PercentageGrass': 'Grass (%)'},                 
                 color_discrete_sequence=['#00FF7F'])

# Highlight the first selected postcode
st.write(size_value_1)

fig.add_scatter(x=[selected_row_1['PercentageTrees'].values[0]], y=[selected_row_1['PercentageGrass'].values[0]], 
                 mode='markers', 
                 marker=dict(color='red', size=size_value_1, line=dict(width=2, color='red')),
                 name=f'Original Postal Code: {selected_postcode_1}',
                 hovertemplate=f'{selected_postcode_1}<br>Tree Coverage: {selected_row_1["PercentageTrees"].values[0]}%<br>Bush Coverage: {selected_row_1["PercentageBushes"].values[0]}%<br>Grass Coverage: {selected_row_1["PercentageGrass"].values[0]}%')

# If new green space values are adjusted, add them to the plot
if (new_green_space_trees != selected_green_space_trees or 
    new_green_space_grass != selected_green_space_grass or 
    new_green_space_bushes != selected_green_space_bushes):
    
    fig.add_scatter(x=[new_green_space_trees], y=[new_green_space_grass],
                    mode='markers',
                    marker=dict(color='grey', size=new_green_space_bushes, line=dict(width=2, color='grey')),
                    name=f'Adjusted Postal Code: {selected_postcode_1}',
                    hovertemplate=f'{selected_postcode_1}<br>Tree Coverage: {new_green_space_trees}%<br>Bush Coverage: {new_green_space_bushes}%<br>Grass Coverage: {new_green_space_grass}%')

# If a second postcode is selected, highlight it
if selected_postcode_2 != 'None':
    selected_row_2 = df_rotterdam.loc[df_rotterdam['Postcode'] == selected_postcode_2]
    size_value_2 = float(selected_row_2['PercentageBushes'].values[0])
    
    fig.add_scatter(x=[selected_row_2['PercentageTrees'].values[0]], y=[selected_row_2['PercentageGrass'].values[0]], 
                     mode='markers', 
                     marker=dict(color='orange', size=size_value_2, line=dict(width=2, color='orange')),
                     name=f'Original Postal Code: {selected_postcode_2}',
                     hovertemplate=f'{selected_postcode_2}<br>Tree Coverage: {selected_row_2["PercentageTrees"].values[0]}%<br>Bush Coverage: {selected_row_2["PercentageBushes"].values[0]}%<br>Grass Coverage: {selected_row_2["PercentageGrass"].values[0]}%')

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
    avg_trees = df_rotterdam['PercentageTrees'].mean()
    avg_bushes = df_rotterdam['PercentageBushes'].mean()
    avg_grass = df_rotterdam['PercentageGrass'].mean()

    total_avg = avg_trees + avg_bushes + avg_grass

    # Dynamic statistics based on selected postcodes
    selected_postcodes = [selected_postcode_1]
    if selected_postcode_2 != 'None':
        selected_postcodes.append(selected_postcode_2)

    avg_selected_trees = df_rotterdam[df_rotterdam['Postcode'].isin(selected_postcodes)]['PercentageTrees'].mean()
    avg_selected_bushes = df_rotterdam[df_rotterdam['Postcode'].isin(selected_postcodes)]['PercentageBushes'].mean()
    avg_selected_grass = df_rotterdam[df_rotterdam['Postcode'].isin(selected_postcodes)]['PercentageGrass'].mean()

    # Get green space values for both selected postcodes
    selected_trees_1 = df_rotterdam.loc[df_rotterdam['Postcode'] == selected_postcode_1, 'PercentageTrees'].values[0]
    selected_bushes_1 = df_rotterdam.loc[df_rotterdam['Postcode'] == selected_postcode_1, 'PercentageBushes'].values[0]
    selected_grass_1 = df_rotterdam.loc[df_rotterdam['Postcode'] == selected_postcode_1, 'PercentageGrass'].values[0]
    green_space_1 = selected_bushes_1 + selected_grass_1 + selected_trees_1

    if selected_postcode_2 != 'None':
        selected_trees_2 = df_rotterdam.loc[df_rotterdam['Postcode'] == selected_postcode_2, 'PercentageTrees'].values[0]
        selected_bushes_2 = df_rotterdam.loc[df_rotterdam['Postcode'] == selected_postcode_2, 'PercentageBushes'].values[0]
        selected_grass_2 = df_rotterdam.loc[df_rotterdam['Postcode'] == selected_postcode_2, 'PercentageGrass'].values[0]

    # Provide insights based on averages for the first postcode
    if green_space_1 > total_avg:
        st.success("🌳 The selected postal code has a higher average of green than the overall average in Rotterdam. ")
    elif green_space_1 < total_avg:
        st.warning("🌳 The selected postal code has a lower average of green than the overall average in Rotterdam. ")
    else:
        st.info("🌳 The selected postal code has the same average of green as the overall average in Rotterdam. ")

    # Additional insights if a second postcode is selected
    if selected_postcode_2 != 'None':
        green_space_2 = selected_bushes_2 + selected_grass_2 + selected_trees_2
        st.markdown("### Comparison Between Selected Postcodes 📊")
        if green_space_1 > green_space_2:
            st.success(f"Postal code {selected_postcode_1} has a **higher green space** of **{green_space_1}%** compared to postcode {selected_postcode_2} with **{green_space_2}%**.")
        elif green_space_1 < green_space_2:
            st.warning(f"Postal code {selected_postcode_1} has a **lower green space** of **{green_space_1}%** compared to postcode {selected_postcode_2} with **{green_space_2}%**.")
        else:
            st.info(f"Both postal codes have the **same green space** of **{green_space_1}%**.")

        # Add insights about the impact of changes based on comparison
        st.markdown("### Opportunities for Improvement 🌱")
        if green_space_1 < green_space_2:
            st.markdown(f"You can help increase the green space in postal code {selected_postcode_1} by taking actions such as planting trees or creating green roofs.")
        elif green_space_1 > green_space_2:
            st.markdown(f"Postal code {selected_postcode_1} is doing well! To maintain or enhance its green space, consider encouraging community initiatives.")

# Combined information and actions to improve green spaces
st.markdown("### Make an Impact on Green Spaces 🌿")
st.markdown("""
You have the power to influence the amount of green space in your postal code! Here are some ways you can contribute:
- **Install a Green Roof**: Changing your roof to a green roof can increase your postal code's green space by **5-15%**.
- **Plant Trees**: Planting just **one tree** can increase green space by approximately **1%** in your area.
- **Create Urban Gardens**: Transforming unused land into community gardens can increase green space by **20-30%** per garden.
- **Support Local Parks**: Advocating for the development of a local park can add **15-40%** green space to your community.
- **Engage in Clean-Up Campaigns**: Keeping existing green areas clean and well-maintained can enhance their usability and attractiveness.

**Every action counts towards creating a greener, healthier community!** 🌍
""")
