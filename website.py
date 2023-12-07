import os
import streamlit as st
from PIL import Image

# --- path settings ---
main_directory = os.getcwd()
main_file = os.path.join(main_directory, "website.py") # path to application file

styles_directory = os.path.join(main_directory, "styles") # path to styles folder
assets_directory = os.path.join(main_directory, "assets") # path to assets folder

# --- general settings ---
TITLE = "AlbertoR94"
NAME = "Alberto Ruiz"
DESCRIPTION = """
    Physi
"""

EMAIL = "alberto.ruiz.gayosso@gmail.com"
SOCIAL_MEDIA = {
    "LinkedIn": "https://linkedin.com",
    "GitHub": "https://github.com",
}

PROJECTS = {
    "Sales Dashboard - Comparing sales across three stores": "https://youtu.be/Sb0A9i6d320",
    "Income and Expense Tracker - Web app with NoSQL database": "https://youtu.be/3egaMfE9388",
    "Desktop Application - Excel2CSV converter with user settings & menubar": "https://youtu.be/LzCfNanQ_9c",
    "MyToolBelt - Custom MS Excel add-in to combine Python & Excel": "https://pythonandvba.com/mytoolbelt/",
}

col1, col2 = st.columns(2)

with col1:
    st.image()