import streamlit as st
import json

# Load the JSON data
with open("./data/youssef/json.json", "r") as file:
    data = json.load(file)
items = data["items"]

st.set_page_config(page_title="Nature Inclusive Measures", layout='wide', initial_sidebar_state="expanded")

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
       (selected_target_group == "All" or selected_target_group in item.get("Target group", []))
]

# Custom CSS for button styling and divider
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        height: auto;
        min-height: 60px;
        font-size: 16px;
        margin-top: 10px;
        padding: 10px;
        word-wrap: break-word;
        white-space: normal;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .stButton {
        display: flex;
        flex-direction: column;
    }
    /* Flex container for columns to make divider full height */
    .flex-container {
        display: flex;
        align-items: stretch;
    }
    /* Divider styling */
    .divider {
        width: 1px;
        background-color: white;
        margin: 0 auto;
    }
    </style>
""", unsafe_allow_html=True)

# Use columns to display grid and details side-by-side with a vertical divider
# Wrap left_col, mid_col, right_col in a flex container
st.markdown('<div class="flex-container">', unsafe_allow_html=True)
left_col, mid_col, right_col = st.columns([3, 0.05, 2])

with left_col:
    # Display header and grid info
    st.header("📋 Nature Inclusive Measures")
    st.info("Select an item from the grid to display its details on the right.")
    
    # Display the grid layout of items in a 4-column grid within the left column
    selected_item_name = None
    for i in range(0, len(filtered_items), 4):  # Loop through items with a step of 4 (one row per loop)
        cols = st.columns(4)  # Create exactly 4 columns per row
        for j, item in enumerate(filtered_items[i:i+4]):  # Populate the row with up to 4 items
            with cols[j]:
                # Display the image in the column, ensuring a consistent size
                st.image(item["image"], use_column_width=True)
                
                # Display the name of the item as a button
                if st.button(item["name"], key=item["name"]):
                    selected_item_name = item["name"]

# Add the vertical line in the middle column, which should now fill the full height
with mid_col:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

with right_col:
    # Show details for the selected item in the right column
    if selected_item_name:
        selected_item = next(item for item in items if item["name"] == selected_item_name)
        st.header("Selected: " + selected_item["name"])

        # Sections
        st.subheader("Description")
        for section in selected_item["sections"]:
            if section['header'].strip():  # Only display the header if it's not empty or just whitespace
                st.write(f"*{section['header']}*") 
            st.write(section["text"])  # Always display the text

        # Guidelines
        st.subheader("Guidelines")
        for guideline in selected_item["guidelines"]["options"]:
            st.write(f"*{guideline['title']}*")
            st.write(guideline["text"])

# Close the flex container div
st.markdown('</div>', unsafe_allow_html=True)
