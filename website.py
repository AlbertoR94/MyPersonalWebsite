import os
import streamlit as st
from PIL import Image

# --- path settings ---
main_directory = os.getcwd()
main_file = os.path.join(main_directory, "website.py") # path to application file

styles_directory = os.path.join(main_directory, "styles") # path to styles folder
assets_directory = os.path.join(main_directory, "assets") # path to assets folder

style_file = os.path.join(styles_directory, "main.css")
profile_pic_path = os.path.join(assets_directory, "myPhotoCircular.png")

# --- general settings ---
TITLE = "AlbertoR94"
NAME = "Alberto Ruiz"
DESCRIPTION = """
    Physicist with 3+ years of experience analyzing data. Master's Degree in Physical Sciences 
    from National Autonomous University of Mexico. Passionate about using Data Science and Machine 
    Learning to draw insights and tell stories.
"""

EMAIL = "alberto.ruiz.gayosso@gmail.com"
SOCIAL_MEDIA = {
    "LinkedIn": {"logo":"https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg", 
                 "link":"https://www.linkedin.com/in/alberto-ruiz-gayosso-a4746827a/"},
    "GitHub": {"logo":"https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png", 
               "link":"https://github.com/AlbertoR94"}
}

PROJECTS = {
    "Sales Dashboard - Comparing sales across three stores": "https://youtu.be/Sb0A9i6d320",
    "Income and Expense Tracker - Web app with NoSQL database": "https://youtu.be/3egaMfE9388",
    "Desktop Application - Excel2CSV converter with user settings & menubar": "https://youtu.be/LzCfNanQ_9c",
    "MyToolBelt - Custom MS Excel add-in to combine Python & Excel": "https://pythonandvba.com/mytoolbelt/",
}

PUBLICATIONS = [
"[Human mobility in the airport transportation network of the United States](https://www.worldscientific.com/doi/abs/10.1142/S0129183123500729)",
"[Correlating USA COVID-19 cases at epidemic onset days to domestic flights passenger inflows by state](https://www.worldscientific.com/doi/abs/10.1142/S0129183121500145)",
"[COVID-19 cases in countries and territories at onset days as function of external tourism inflows](https://www.worldscientific.com/doi/abs/10.1142/S0129183120501533)"
]

# define style 

profile_pic = Image.open(profile_pic_path)

st.set_page_config(page_title=TITLE, layout="wide")

with open(style_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="small")

# --- hero section ---
with col1:
    st.image(profile_pic)

with col2:
    st.title(NAME)
    st.write(DESCRIPTION)
    st.write("✉️", EMAIL)

    # --- SOCIAL LINKS ---
    cols = st.columns([0.10, 0.25, 0.10, 0.21, 0.35], gap="small")
    
    cols[0].image(f"{SOCIAL_MEDIA['LinkedIn']['logo']}", width=12*2)
    #cols[1].text("\n")
    cols[1].write(f"[LinkedIn]({SOCIAL_MEDIA['LinkedIn']['link']})")

    cols[2].image(f"{SOCIAL_MEDIA['GitHub']['logo']}", width=10*2)
    #<cols[3].text("\n")
    cols[3].write(f"[GitHub]({SOCIAL_MEDIA['GitHub']['link']})")


# --- EXPERIENCE & QUALIFICATIONS ---
st.write('\n')
st.subheader("Experience & Qulifications")
st.write(
    """
- 🔨 7 Years expereince extracting actionable insights from data
- 🔨 Strong hands on experience and knowledge in Python and Excel
- 🔨 Good understanding of statistical principles and their respective applications
- 🔨 Excellent team-player and displaying strong sense of initiative on tasks
"""
)


# --- SKILLS ---
st.write('\n')
st.subheader("Skills")
st.write(
    """
- 💻 Programming: Python (Scikit-learn, Pandas), SQL, VBA
- 📈 Data Visulization: PowerBi, MS Excel, Plotly
- 📚 Modeling: Logistic regression, linear regression, decition trees
- 🗄️ Databases: Postgres, MongoDB, MySQL
"""
)

# --- Projects & Accomplishments ---
st.write('\n')
st.subheader("Projects & Accomplishments")
st.write("---")
for project, link in PROJECTS.items():
    st.write(f"[{project}]({link})")


# --- Publications ---
st.write('\n')
st.subheader("Publications")
st.write("---")
for publication in PUBLICATIONS:
    st.write(publication)