import streamlit as st
from PIL import Image
# Importe les modules une seule fois en haut
import JuridicalForms
import GeographicDistribution
import dominant_sector_province
import business_creation
import status_entrprise
import dominant_economic_sector_per_province

st.set_page_config(page_title="KBO Explorer", layout="wide")

image = Image.open("insights/KBO-logo.jpg")
st.image(image, use_container_width=True)

# ---------- TITLE ----------
st.markdown("""
<style>
.title-section {
    text-align: center;
    margin-top: -20px;
}
.title-section h1 {
    font-size: 48px;
    color: #2c3e50;
    margin-bottom: 0px;
}
.title-section h3 {
    font-size: 20px;
    color: #7f8c8d;
    margin-top: 5px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='title-section'>
    <h1>Belgian Companies Storytelling</h1>
    <h3> Insights into Belgian Companies</h3>
</div>
""", unsafe_allow_html=True)
st.markdown("""
            
Welcome to this interactive application that explores Belgian company data from the Crossroads Bank for Enterprises (CBE).
         
This project was developed using Python, SQLite, SQLAlchemy, and Streamlit.
""")

# ---------- MENU LATÉRAL ----------
st.sidebar.title(" Navigation")
menu = st.sidebar.radio(
    "Available sections",
    [   "Home",
        "Legal Forms",
        "Geographic Distribution",
        "Sector Analysis (NACE)",
        "Dominant Economic Sectors",
        "Business Status"
    ]
)

# ---------- CONTENU DYNAMIQUE EN FONCTION DU BOUTON ----------
if menu == "Home":
    st.header(" Introduction")
    st.write("""KBO Explorer is an interactive data analysis dashboard designed to explore and visualize insights from the official Belgian company registry (Banque-Carrefour des Entreprises, or BCE/KBO.
                This project leverages a local SQLite database extracted from open KBO data to answer key business questions and uncover structural patterns in the Belgian economic landscape.
                Using Streamlit, we offer a user-friendly web interface that allows users to interactively explore company characteristics, including:
             
             1. Legal forms and juridical structures. 

             2. Annual trends in business creation.

             3. Dominant economic sectors by region and province.

             4. Distribution of active vs. inactive enterprises.

             5. Correlation analysis across company attributes.

            The goal of this tool is to provide a compact yet powerful storytelling platform for policymakers, entrepreneurs, data analysts, and researchers who want to better understand how Belgian enterprises are structured, how they evolve, and where economic strengths lie across the country.""")
    
elif menu == "Legal Forms":
    st.header("Distribution of legal statuses.")
    JuridicalForms.show()

elif menu == "Geographic Distribution":
    st.header(" Where companies are located and which sectors are dominant.")
    GeographicDistribution.show()
    dominant_sector_province.show()
    dominant_economic_sector_per_province.show()

elif menu == "Sector Analysis (NACE)":
    st.header("Sector Analysis (NACE): oldest and newest sectors.")
    business_creation.show()

elif menu == "Dominant Economic Sectors":
    st.header(" Dominant Sectors by Province")
    dominant_sector_province.show()

elif menu == "Business Status":
    st.header(" Business Status")
    status_entrprise.show()
