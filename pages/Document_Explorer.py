import streamlit as st
import os

import requests

OK_STATUS_CODE = 200

# Define session variables here:
if "user_session" not in st.session_state:
    st.session_state['user_session'] = None

if 'initialized' not in st.session_state:
    st.session_state['initialized'] = False

st.session_state

PREDICT_ENDPOINT = "http://127.0.0.1:5000/predict"


main_directory = os.getcwd()
styles_directory = os.path.join(main_directory, "styles") # path to styles folder
style_file = os.path.join(styles_directory, "main.css")

# Apply style 
with open(style_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)


# Application Code
st.markdown("# Document Explorer")
# Brief description of application
st.markdown("""This App uses a LLM and Vector Embeddings to answer questions about a document provided by the user. 
            You can change the temperature to introduce some randomness into the model. Larger values of temperates mean
            a more "creative" model. 
            """)

DEFAULT_URL = "https://www.gutenberg.org/cache/epub/11/pg11-images.html" # Alice in Worderland
DEFAULT_QUERY = "What didn't Alice think so very much about?"

# user input
st.markdown("#### Enter the URL of a document you want to explore:")
document_url = st.text_input(label="## Enter URL", 
                            placeholder=DEFAULT_URL, 
                            label_visibility="collapsed")

if document_url and not st.session_state.initialized:

    st.session_state.user_session = requests.session()

    json_data = {"web_path":document_url}

    with st.spinner('Wait for model initialization'):
        req = st.session_state.user_session.post("http://127.0.0.1:5000/predict", json=json_data)
        if req.json()["response"] == "Initialized":
            st.session_state.initialized = True

if st.session_state.initialized:
    st.markdown("#### Enter query: ")
    query = st.text_input(label="## Enter query", 
                        placeholder=DEFAULT_QUERY, 
                        label_visibility="collapsed")
    
    if query:
        json_data = {"web_path":document_url, "query":query}
        req = st.session_state.user_session.post("http://127.0.0.1:5000/predict", json=json_data)

        if req.status_code == OK_STATUS_CODE:
            st.write(req.json()["response"])


