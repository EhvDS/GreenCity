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
    </style>
    """,
    unsafe_allow_html=True
)

# Create a grid layout with HTML and CSS
html = "<div class='grid-container'>"
for item in filtered_items:
    html += f"""
    <div class='grid-item'>
        <img src='{item['image']}' alt='{item['name']}'>
        <h3>{item['name']}</h3>
        <form action='#' method='POST'>
            <input type='submit' name='select_{item['name']}' value='Select' style='width: 100%; padding: 10px;'>
        </form>
    </div>
    """
html += "</div>"

# Render the grid with Streamlit
st.markdown(html, unsafe_allow_html=True)

# Check which item was selected
selected_item_name = None
for item in filtered_items:
    if st.session_state.get(f"select_{item['name']}"):
        selected_item_name = item["name"]

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
