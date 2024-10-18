import streamlit as st
import re
from transformers import pipeline

st.set_page_config(page_title="Nature-Inclusive Construction Chatbot", page_icon="🌿", layout="centered")
### st.title("🌿 Animal Information Chatbot for Nature-Inclusive Construction")

# Initialize the Hugging Face question-answering pipeline
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# Load the document content
def load_document(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

# Build an index of animal sections in the document
def build_document_index(document):
    sections = re.split(r'\n\n', document)
    animal_index = {}
    for section in sections:
        match = re.match(r'^([A-Z][a-zA-Zéëä\s]+)\s?\([^)]+\)', section.strip())
        if match:
            animal_name = match.group(1).strip().lower()
            animal_index[animal_name] = section.strip()
    return animal_index

# Extract the animal name from the user's query (improved parsing)
def extract_animal_name(query):
    query = query.lower()
    query = re.sub(r'[?.!]', '', query)  # Remove punctuation marks for better extraction
    query = re.sub(r'\b(the|a|an)\b', '', query).strip()  # Remove articles for better extraction
    if "about" in query:
        return query.split("about")[-1].strip()
    elif "tell me" in query:
        return query.split("tell me")[-1].strip()
    return query

# Mapping of common animal names from English to Dutch
animal_name_mapping = {
    "squirrel": "eekhoorn",
    "house martin": "huiszwaluw",
    "starling": "spreeuw",
    "great tit": "koolmees",
    "blue tit": "koolmees",  # Redirect blue tit to great tit
    "peregrine falcon": "slechtvalk",
    "black redstart": "zwarte roodstaart",
    "amphibians": "amfibieën",
    "bees": "bijen",
    "butterflies": "bijen",  # Redirect butterflies to bees (same text)
    # Add more mappings as needed
}

# Path to your document
document_path = "data/AnimalsTest.txt"

# Load document content and build the index
document_content = load_document(document_path)
animal_index = build_document_index(document_content)

# Streamlit Interface - Enhancing the front-end
### Simona: set_page_config can only be used once
### st.set_page_config(page_title="Nature-Inclusive Construction Chatbot", page_icon="🌿", layout="centered")
### st.title("🌿 Animal Information Chatbot for Nature-Inclusive Construction")
# Page title and description
st.title("🌿 Animal Information Chatbot for Nature-Inclusive Construction")
st.subheader("by Aleksandar Stoyanov")
st.markdown("""
Welcome to the Animal Information Chatbot designed to assist with 
    nature-inclusive construction and animal habitat information. 
    You can ask me questions about different animals and how to create environments 
    that are friendly for their needs.
""")
st.markdown("""
 Example Questions:
    - "What can you tell me about *animal*?"
    - "Tell me about *animal*?"

    Animals you can ask about:
    - Squirrel
    - House Martin
    - Starling
    - Great Tit
    - Blue Tit
    - Peregrine Falcon
    - Black Redstart
    - Amphibians
    - Bees
    - Butterflies
""")
# User input for the chatbot
user_query = st.text_input("Type your question here:", "")

if user_query:
    # Extract the animal name from the user query
    animal_name = extract_animal_name(user_query)

    # Map the animal name from English to Dutch if available
    if animal_name in animal_name_mapping:
        animal_name = animal_name_mapping[animal_name].lower()

    # Find the relevant section for the animal from the index
    if animal_name in animal_index:
        animal_section = animal_index[animal_name]

        # Use the QA model to answer specific questions within the animal section
        if "about" in user_query or "tell me" in user_query:
            response = f"Full information about {animal_name}:\n\n{animal_section}"
        else:
            try:
                qa_result = qa_pipeline({
                    'question': user_query,
                    'context': animal_section
                })
                response = qa_result.get('answer', "Sorry, I couldn't find the specific information.")
            except Exception as e:
                # If the QA model fails, fall back to showing the whole section
                response = f"Sorry, an error occurred while trying to find the answer. Here is the full information about {animal_name}:\n\n{animal_section}"
    else:
        response = f"Sorry, no information found for '{animal_name}'."

    # Update session state to store only the last response
    st.session_state.conversation = [(user_query, response)]

# Display the last conversation
if 'conversation' in st.session_state and st.session_state.conversation:
    user_input, bot_response = st.session_state.conversation[-1]
    st.markdown(f'<div class="chat-container"><p class="user-query">**You:** {user_input}</p><p class="bot-response">**Chatbot:** {bot_response}</p></div>', unsafe_allow_html=True)

