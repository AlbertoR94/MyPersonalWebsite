import streamlit as st
from utils import *
import os

main_directory = os.getcwd()
styles_directory = os.path.join(main_directory, "styles") # path to styles folder
style_file = os.path.join(styles_directory, "main.css")


# Apply style 
with open(style_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)


# Application Code
st.markdown("# Tweet Sentiment Prediction")
# Brief description of application 


# user input
st.markdown("#### Enter text to classify:")
text = st.text_area(label="## Enter text to classify", value="What a wonderful day!", label_visibility="collapsed")

if text:
    with st.spinner("Please wait a moment while predictions are generated"): # 
        processed_text = preprocess_string(text)
        prediction = predict_sentiment(processed_text, classifier, vectorizer)
        st.markdown(f"#### *{text}* has a probability {prediction:{1}.{3}} of being negative")
        result = ":green[Positive]" if prediction < 0.5 else ":red[Negative]"	
        st.markdown(f"#### ▶️ Text is {result}")
        
        st.markdown("")

st.markdown("\n")

file = st.file_uploader(label="Or upload a file with several tweets to classify")

if file:
    dataframe = pd.read_csv(file, index_col="id")
    dataframe.text = dataframe.text.apply(preprocess_string)
    st.write(dataframe)
    with st.spinner("Please wait a moment while predictions are generated"):
        # st.download_button("Download File", data=None)
        #data = torch.tensor(dataframe.text.values)
        with open("results.txt", mode="w+") as pred_results:
            for row in dataframe.text:
                prediction = predict_sentiment(row, classifier, vectorizer)
                pred_results.write(str(prediction))
                pred_results.write("\n")

    pred_results = open("results.txt", "r")

    st.download_button("Download file with results", data=pred_results)

