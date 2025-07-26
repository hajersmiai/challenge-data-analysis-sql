import streamlit as st
from PIL import Image
# Import all modules used for each page
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
        "Sector Analysis (NACE)",
        "Geographic Distribution",
        "Dominant Economic Sectors",
        "Business Status",
        "Full Report"  
    ]
)

# ---------- CONTENU DYNAMIQUE EN FONCTION DU BOUTON ----------
if menu == "Home":
    st.header(" Introduction")
    st.write("""KBO Explorer is an interactive data analysis dashboard designed to explore and visualize insights from the official Belgian company registry (Banque-Carrefour des Entreprises, or BCE/KBO).
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
    st.subheader("Legal Structure Analysis of Belgian Companies")

    st.markdown("###  1. Business Longevity: Nearly All Companies Still Active")
    st.image("insights/Distribution of active vs deregistered companies.png", use_container_width=True)
    st.markdown("""
**Insight:** A remarkable **98.8%** of companies remain active in the KBO registry, while only **1.2%** are deregistered.  
**Interpretation:** This reflects strong continuity but may also include dormant or shell companies.
""")

    st.markdown("### 2. Physical Presence: Majority Have Establishments")
    st.image("insights/Distribution of companies with and without establishements.png", use_container_width=True)
    st.markdown("""
**Insight:** **77.7%** of companies report a physical/legal establishment.  
**Interpretation:** Indicates formal presence, but 22.3% may operate virtually or on paper only.
""")

    st.markdown("###  3. Activity Declaration Transparency")
    st.image("insights/Distribution of companies with and without main activity declared.png", use_container_width=True)
    st.markdown("""
**Insight:** Only **64.9%** of companies declared a main activity.  
**Interpretation:** 35.1% lack transparency — they may be new, inactive, or holding entities.
""")

    st.markdown("###  4. Preferred Legal Forms")
    st.image("insights/Top 10 Juridical Form distribution with entreprise type.png", use_container_width=True)
    st.markdown("""
**Insight:** LLCs dominate, followed by Natural Persons and Limited Partnerships.  
**Interpretation:** Reflects risk mitigation and entrepreneurial flexibility.
""")

    st.markdown("###  Summary Table")
    st.table({
        "Legal Attribute": ["Business continuity", "Physical presence", "Activity transparency", "Top legal structures"],
        "Observation": ["98.8% remain active", "77.7% have establishments", "35.1% lack declared activity", "LLC, Natural Person, Partnership"]
    })

elif menu == "Sector Analysis (NACE)":
    st.header("Sector Analysis (NACE): Oldest and Newest Sectors")

    # --- Introduction
    st.markdown("""
    This section explores the evolution of economic sectors in Belgium based on company age.
    By analyzing the average age of businesses in each NACE category, we can identify both long-standing economic pillars and fast-growing emerging industries.
    """)

   # business_creation.show()  

    # --- Mature Sectors
    st.subheader("🔹 Top 10 Most Mature Sectors")
    st.image("insights/top 10 most mature sectors.png", use_container_width=True)

    st.markdown("""
    These sectors reflect Belgium's traditional economic backbone:

    - **Education**, **social housing**, and **municipal administration** indicate long-term public service presence.
    - **Insurance** and **credit institutions** highlight financial stability.
    - **Coal mining** and **telephony device manufacturing** represent Belgium’s industrial heritage.

    **Insight:** These sectors are **institutional and resilient**, evolving slowly but remaining essential to economic and social infrastructure.
    """)

    st.markdown("""
    **Example - Deep Dive:**  
    - **Insurance**: Belgium's oldest sector, with firms from the 19th century.  
    - **Education**: Historic presence, supporting national knowledge capital.  
    - **Housing**: Real estate and public housing have deep roots in economic life.
    """)

    # --- Newest Sectors
    st.subheader("🔸 Top 10 Newest Sectors")
    st.image("insights/Top 10 newest sectors.png", use_container_width=True)

    st.markdown("""
    These sectors illustrate Belgium’s recent waves of innovation:

    - High-tech and defense industries such as **military aircraft**, **electricity storage**, and **spacecraft manufacturing**.
    - Specialized health services like **dental and ocular care**.
    - **Education support** and **intermediation services** indicating trends toward **personalized learning** and **digital transformation**.

    **Insight:** These emerging sectors are **young, agile, and high-potential**, but may face **regulatory challenges** and **market uncertainty** in their early stages.
    """)

    st.markdown("""
    **Emerging Trends Driving Growth:**  
    - **Defence**: Linked to increased European defense cooperation  
    - **Renewable Energy**: Green transition and sustainability policies  
    - **Technology Services**: Expanding digital economy and automation
    """)

    # --- Combined Analysis
    st.markdown("###  Interpretation and Policy Implications")
    st.markdown("""
    | Category         | Characteristics                   | Implications                                      |
    |------------------|------------------------------------|--------------------------------------------------|
    | Mature Sectors   | Public, industrial, financial      | Stable, institutional, essential                 |
    | Emerging Sectors | Tech, health, green industries     | Agile, innovative, growth-oriented               |
    | Policy Needs     | Modernize legacy, support startups | Incentivize innovation, reduce barriers to entry |

    This analysis helps policymakers and analysts understand where **Belgium’s economic roots lie**, and where **its future opportunities are blooming**.
    """)

    # --- Strategic Use Case
    st.markdown("###  Strategic Value of KBO Explorer")
    st.write("""
    KBO Explorer provides valuable insights for:

    -  Regional economic development planning  
    -  Entrepreneurship support targeting  
    -  Investment opportunity identification  
    -  Navigating legacy vs. innovation balances
    """)


elif menu == "Geographic Distribution":
    st.header("Where companies are located and which sectors are dominant.")
    st.subheader(" Regional Concentration of Companies")

    st.markdown("""
    Belgium's business landscape is **geographically diverse**, with significant variation in sectoral dominance across provinces and regions.

    **Highlights by Province:**

    - **Brussels-Capital**: Predominantly administrative and service-oriented, with a high density of consultancy, legal, and NGO sectors.
    - **Antwerp & East Flanders**: Major logistics and **manufacturing hubs**, thanks to port activity and industrial infrastructure.
    - **Walloon provinces (e.g., Liège, Hainaut)**: Strong presence of **construction**, **heavy industry**, and **social services**.
    - **Luxembourg & Namur**: Focused on **agriculture**, **forestry**, and **public sector employment**, reflecting rural characteristics.

    These trends are shaped by **historical specializations**, **infrastructure access**, and **policy incentives**.
    """)

    st.markdown("The following charts explore company counts and sector dominance per province:")

    GeographicDistribution.show()
    dominant_sector_province.show()
    dominant_economic_sector_per_province.show()

  

elif menu == "Dominant Economic Sectors":
    st.header("Dominant Sectors by Province")
    st.subheader(" Sectoral Landscape by Province")

    st.markdown("""
    Each Belgian province exhibits a distinct economic identity, closely linked to local resources, urbanization levels, and labor markets.

    **Key Observations:**

    - **Antwerp**: Leads in **wholesale trade, transport, and petrochemical industries**.
    - **East & West Flanders**: Strong in **textile manufacturing**, **logistics**, and **agri-food processing**.
    - **Brussels**: Dominated by **professional services**, **international institutions**, and **ICT firms**.
    - **Liège & Hainaut**: Traditional **heavy industries**, now increasingly diversified into **renewable energy** and **healthcare**.
    - **Limburg**: Emergence of **cleantech** and **logistics corridors**.
    - **Namur & Luxembourg**: Lower company density but strong in **public services**, **tourism**, and **rural economy**.

    This diversity reflects Belgium’s **polycentric development model**, combining historical strengths with emerging innovations.
    """)

    dominant_sector_province.show()

   

elif menu == "Business Status":
    st.header("Business Status")
    st.subheader(" Business Activity & Status Insights")

    st.markdown("""
    Belgium's business register shows **high survival and stability**, but also points to some challenges in transparency and classification.

    **Key Metrics:**

    -  **98.8% of companies are still listed as active**, indicating strong continuity. However, some may be **dormant** or **inactive in practice**.
    -  **77.7%** have at least one physical establishment — confirming a **significant role for physical presence** in business operations.
    -  **35.1% of companies do not declare their main activity**, which can hinder policymaking, tax oversight, and economic modeling.

    **Implications:**

    - Authorities may need to improve **monitoring and updating mechanisms** in the KBO.
    - Data users should be aware of the **potential overestimation of actual business activity**.

    These statistics highlight the need for better **administrative transparency** and offer room for **modernization of registration practices**.
    """)

    st.markdown("The following charts explore the status of enterprises in Belgium:")
    status_entrprise.show()
elif menu == "Full Report":
   
    st.header(" KBO Explorer — Full Analytical Report")

    st.markdown("### Project Overview")
    st.markdown("""
    **KBO Explorer** is an analytical dashboard built on Belgian enterprise registry data (KBO/BCE), designed to uncover patterns in business creation, legal structures, and sectoral evolution.
    
    **Tech stack:** SQLite + SQLAlchemy + Streamlit.
    """)

    st.markdown("###  Recent Drop in Business Creation")
    st.markdown("""
    After nearly a decade of steady growth, 2025 shows a significant downturn in enterprise formation, affecting both legal entities and sole proprietors.

     Potential reasons:
    - Falling economic confidence
    - Regulatory tightening
    - Barriers to entrepreneurship
    """)

    st.markdown("###  30-Year Boom in Enterprise Formation")
    st.markdown("""
    - **Accelerating growth** over decades
    - **Legal entities** now lead over sole traders
    - Trend remained **resilient** even through crises (2008, COVID-19)
    """)

    st.markdown("###  Business Longevity")
    st.markdown("""
    - **98.8%** of companies remain active  
    - May include dormant or administrative shells  
    """)

    st.markdown("###  Physical Establishments")
    st.markdown("""
    - **77.7%** of businesses maintain physical establishments  
    - Despite digital trends, bricks-and-mortar remains dominant
    """)

    st.markdown("###  Activity Declaration Gaps")
    st.markdown("""
    - **35%** of businesses haven’t declared a main activity  
    - Affects transparency, regulation, tax compliance
    """)

    st.markdown("###  Legal Structures")
    st.markdown("""
    - Private limited companies (BV/SRL) dominate post-2019 reforms  
    - Sole traders still significant
    """)

    st.markdown("###  Most Mature Sectors")
    st.markdown("""
    - **Insurance**  
    - **Education**  
    - **Housing**
    """)

    st.markdown("###  Emerging Sectors")
    st.markdown("""
    - **Defence**: Driven by European security  
    - **Renewables**: Linked to green transition  
    - **Tech Services**: Supporting digital transformation
    """)

    st.markdown("###  Provincial Sector Highlights")
    st.markdown("""
    - **Brussels**: Administrative & services  
    - **Antwerp & East Flanders**: Logistics & manufacturing  
    - **Hainaut & Liège**: Industry & construction  
    - **Luxembourg & Namur**: Agriculture & public services
    """)

    st.markdown("###  Conclusion")
    st.markdown("""
    KBO Explorer helps identify:
    - Regional business strengths  
    - Policy improvement areas  
    - Investment & innovation opportunities  
    """)

    st.markdown("###  Limitations")
    st.markdown("""
    - Static database (no real-time updates)  
    - Missing fields (e.g., activity codes)  
    - No financial indicators (turnover, profit)  
    """)

    st.markdown("###  Intended For")
    st.markdown("""
    Policymakers, investors, entrepreneurs, researchers
    """)

    st.markdown("### 📎 Links")
    st.markdown("[🔗 Streamlit App](https://challenge-data-analysis-sql-2dgn49fne5teas8lu5p6d9.streamlit.app/)")
    st.markdown("[🔗 GitHub Repository](https://github.com/hajersmiai/challenge-data-analysis-sql)")

