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

# Custom CSS for button styling and flex container with border
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
    /* Flex container with border between left and right columns */
    .flex-container {
        display: flex;
    }
    .left-column {
        border-right: 2px solid #ccc;
        padding-right: 15px;
        flex: 3;
    }
    .right-column {
        flex: 2;
        padding-left: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Create a flex container to hold left and right columns with a border between them
st.markdown('<div class="flex-container">', unsafe_allow_html=True)

# Left column with border
with st.container():
    st.markdown('<div class="left-column">', unsafe_allow_html=True)
    
    st.header("📋 Nature Inclusive Measures")
    st.info("Select an item from the grid to display its details on the right.")
    st.markdown("""
    <div style="background-color: #FFF3CD; padding: 1rem; border-radius: 5px; color: #856404; font-size: 1rem;">
        <strong>For more information on nature inclusive measures, discover the NEST inclusive platform.</strong>
        <br>
        <a href="https://natuurinclusiefontwikkelen.nl/" target="_blank" style="color: #856404; text-decoration: underline;">
            Explore actions you can take!
        </a>
        <br>   
        <a href="https://nestnatuurinclusief.nl/referenties/" target="_blank" style="color: #856404; text-decoration: underline;">
            Explore NEST projects!
        </a>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='border:1px solid gray;'>", unsafe_allow_html=True)
    
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

    st.markdown('</div>', unsafe_allow_html=True)  # Close the left column div

# Right column
with st.container():
    st.markdown('<div class="right-column">', unsafe_allow_html=True)
    
    if selected_item_name:
        selected_item = next(item for item in items if item["name"] == selected_item_name)
        st.header("Selected: " + selected_item["name"])

        # Points
        st.subheader("Points")
        st.write("Amount of nature points: " + str(selected_item["points"]))

        # Sections
        st.subheader("Description")
        for section in selected_item["sections"]:
            if section['header'].strip():  # Only display the header if it's not empty or just whitespace
                st.write(f"*{section['header']}*") 
            st.write(section["text"])  # Always display the text

        # Guidelines
        st.subheader("Guidelines")
        if "options" in selected_item["guidelines"] and selected_item["guidelines"]["options"]:
            for guideline in selected_item["guidelines"]["options"]:
                # Check if 'title' is empty and display "Empty." if so
                title = guideline.get("title", "").strip()
                if title == "":
                    st.write("Empty.")
                else:
                    st.write(f"*{title}*")
                st.write(guideline["text"])  # Display the text for each guideline, regardless of whether the title is empty
        else:
            st.write("Empty.")
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close the right column div

st.markdown('</div>', unsafe_allow_html=True)  # Close the flex container div
