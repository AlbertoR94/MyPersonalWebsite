import streamlit as st
from utils import *

# Model and Prediction Code



# Application Code
# Brief description of application 
st.markdown("# Tweet Sentiment Prediction")

# user input
text = st.text_area(label="Enter text to classify")
file = st.file_uploader(label="Or upload a file with several tweets to classify")

if text or file:
    with st.spinner("Please wait a moment while predictions are generated"):
        st.text("Something")
    if text:
        text = preprocess_string(text)
        prediction = predict_sentiment(text, classifier, vectorizer)
        st.text(text)
        st.markdown(f"{prediction}")
    if file:
        st.download_button("Download File", data=None)
