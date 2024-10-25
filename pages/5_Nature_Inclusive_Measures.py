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

# Display the items in a 4-column grid view with spacing and image resizing
for i in range(0, len(filtered_items), 4):  # Loop through items with a step of 4
    cols = st.columns([1, 1, 1, 1])  # Create 4 equal-width columns
    for idx, item in enumerate(filtered_items[i:i+4]):  # Access a group of 4 items at a time
        with cols[idx]:
            st.image(item["image"], width=120)  # Adjust the image size to prevent overlapping
            st.write(item["title"])  # Display the title of the item
            st.write(item["description"])  # You can also add descriptions or other details if necessary
