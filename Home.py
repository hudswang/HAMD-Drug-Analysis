import streamlit as st
# Page Setup

about_page = st.Page(
    page = "views/about_me.py",
    title = "About Me",
    icon = ":material/account_circle:",
    default = True,
)

drug_analysis = st.Page(
    page = "views/Drug Analysis/drug_analysis.py",
    title = "Drug Analysis",
    icon = ":material/bar_chart:",

)

pg = st.navigation(
    {
        "Info": [about_page],
        "Projects": [drug_analysis],
    }
)

pg.run()
# Navigation










