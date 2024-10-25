import streamlit as st
import json

# Load the JSON data
with open("./data/youssef/json.json", "r") as file:
    data = json.load(file)
items = data["items"]

# Sidebar filters for Category and Target Group
st.sidebar.header("Filter Options")
available_categories = list(set([item["categories"] for item in items]))
available_target_groups = list(set([group for item in items if "Target group" in item for group in item["Target group"]]))

selected_category = st.sidebar.selectbox("Select Category", ["All"] + available_categories)
selected_target_group = st.sidebar.selectbox("Select Target Group", ["All"] + available_target_groups)

# Filter items based on selected category and target group
filtered_items = [
    item for item in items
    if (selected_category == "All" or item["categories"] == selected_category) and
       (selected_target_group == "All" or selected_target_group in item["Target group"])
]

# Add custom CSS for the grid layout and spacing
st.markdown(
    """
    <style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);  /* 4 columns */
        gap: 20px;  /* Spacing between grid items */
    }
    .grid-item {
        text-align: center;
        padding: 10px;
        font-size: 16px;
        border: 1px solid #ccc;
        border-radius: 10px;
        background-color: #f9f9f9;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
    }
    .grid-item img {
        max-width: 100%;
        height: auto;
        border-radius: 10px;
    }
    .grid-item button {
        padding: 8px 16px;
        margin-top: 10px;
        font-size: 14px;
        border: none;
        border-radius: 5px;
        background-color: #007bff;
        color: white;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use Streamlit buttons to select items
selected_item_name = None

# Create a grid layout with HTML and Streamlit buttons
html = "<div class='grid-container'>"
for i, item in enumerate(filtered_items):
    image_path = item["image"]
    name = item["name"]
    
    # Create the grid item with image and button
    html += f"""
    <div class='grid-item'>
        <img src='{image_path}' alt='{name}'>
        <h3>{name}</h3>
    """
    
    # Add a Streamlit button for selecting the item (HTML wrapped)
    if st.button(f"Select {name}", key=i):
        selected_item_name = name
    
    html += "</div>"

html += "</div>"

# Render the HTML grid layout
st.markdown(html, unsafe_allow_html=True)

# Show details for the selected item
if selected_item_name:
    selected_item = next(item for item in items if item["name"] == selected_item_name)
    st.header(selected_item["name"])

    # Sections
    st.subheader("Sections")
    for section in selected_item["sections"]:
        st.write(f"**{section['header']}**")
        st.write(section["text"])

    # Guidelines
    st.subheader("Guidelines")
    for guideline in selected_item["guidelines"]["options"]:
        st.write(f"**{guideline['title']}**")
        st.write(guideline["text"])
