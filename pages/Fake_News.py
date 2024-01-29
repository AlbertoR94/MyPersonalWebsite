import streamlit as st
import os

import requests
import json

FILE_NAME = "predictions.json"

main_directory = os.getcwd()
styles_directory = os.path.join(main_directory, "styles") # path to styles folder
style_file = os.path.join(styles_directory, "main.css")

# Apply style 
with open(style_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)


# Application Code
st.markdown("# News Classification")
# Brief description of application 


# user input
st.markdown("#### Enter News Title to classify:")
news_title = st.text_area(label="## Enter text to classify", value="What a wonderful day!", label_visibility="collapsed")

if news_title:
    json_file = {"id":0, "text": news_title}
    req = requests.post("http://127.0.0.1:5000/predict_one", json=json_file)

    result = req.json()

    st.markdown(f"#### *{news_title}* has a probability {result['prob']:{1}.{3}} of being real.")
    prediction = ":green[Real]" if result["pred"] == 1 else ":red[Fake]"	
    st.markdown(f"#### ▶️ Text is {prediction}")
    
    st.markdown("")

st.markdown("\n")

file = st.file_uploader(label="Or upload a json file with several news to classify")

if file:
    # read file as string
    json_file = json.loads(file.read())

    # make predictions with API
    req = requests.post("http://127.0.0.1:5000/predict", json=json_file)

    # save predictions as json
    with open(FILE_NAME, "w") as f:
        json.dump(req.json(), f)

    # download predictions as json file
    with open(FILE_NAME, "r") as f:
        st.download_button("Download Predictions", f, file_name=FILE_NAME)
