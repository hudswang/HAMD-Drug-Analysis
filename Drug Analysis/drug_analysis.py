# Imports
import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import math


# Save website  
@st.cache_data
def fetch_and_clean_data():
    # Fetch data from URL here, and then clean it up.
    df = pd.read_excel("Merged Research Data By PID with Demographics.xlsx")
    df = df.dropna(subset=['AGE'])
    df['AGE'] = df['AGE'].astype('int')
    df['SEX'] = df['SEX'].replace({"M":"Male", "F":"Female"})
    
    for visit in range (1,10): 
        v1 = []
        for  i in df. columns.tolist():
            if f'V{visit}' in i:
                v1.append(i)
        df[f'V{visit}-HAMD-TOTAL'] = 0
        for i in v1:
            df[f'V{visit}-HAMD-TOTAL'] += df[i]
        
    return df

# Shows the data set
df = fetch_and_clean_data()

# Select Page
option = st.sidebar.selectbox(
    "Explore the data!",
    ("Introduction", "Exploratory Data Analysis", "HAMD"),
)
    
if option == "Introduction":
    
    st.title("Introduction")
    
    st.write("This data analysis project is centered on the Hamilton Depression Rating Scale (HDRS), also known as the 'HAMD', is one of the most widely used clinician-administered tools for assessing the severity of depression. Originally developed for hospital inpatients, the HDRS measures depressive symptoms over the past week, making it an essential tool in clinical and research settings.")
    st.write("The dataset used in this project is derived from HAMD evaluations, specifcially for the HDRS17 (17-item version). This scales assess a range of symptoms, including depressed mood, feelings of guilt, suicidal ideation, insomnia, work impairment, and psychomotor agitation or retardation.")
    st.write("The scoring system helps categorize depression severity, with higher scores indicating more severe depressive states.")
    st.write("The primary objective of this analysis is to explore trends, patterns, and potential correlations within the dataset to gain deeper insights into depressive symptomatology. By leveraging statistical techniques and visualization methods, this study aims to evaluate factors that contribute to depression severity and identify possible predictors of mental health outcomes.")
    
    st.write("For th HDRS17 version, a score of 0–7 is generally accepted to be within the normal range (or in clinical remission), while a score of 20 or higher (indicating at least moderate severity) is usually required for entry into a clinical trial.")
    st.write("Below is a sample of the collected dataset:")

   
    st.dataframe(df) 

elif option == "Exploratory Data Analysis":
    
    st.title("Exploratory Data Analysis")
    age_sex_df = df[["SEX", "AGE"]].value_counts().reset_index()
    st.bar_chart(age_sex_df, x='AGE', y='count',color='SEX')



    drug_therapy_df = df[["DRUG", "THERAPY"]].value_counts().reset_index()
    st.bar_chart(drug_therapy_df, x='DRUG', y='count',color='THERAPY')



elif option == "HAMD":
    
    st.title("Total HAMD")
    st.sidebar.header("Filter Options")
    drug_option = st.sidebar.selectbox(
        "Select Drug:",
        df['DRUG'].unique(),
        index=0
    )

    therapy_option = st.sidebar.selectbox(
        "Select Therapy:",
        df[df['DRUG'] == drug_option]['THERAPY'].unique(),
        
        index=0
    )

    df1 = df[(df['DRUG'] == drug_option) & (df['THERAPY'] == therapy_option)]

    hamdMeans = []
    upperBounds = []
    lowerBounds = []

    for visit in range (1,10): 
        HAMD_standard = df1[f'V{visit}-HAMD-TOTAL'].std()
        HAMD_mean = df1[f'V{visit}-HAMD-TOTAL'].mean()
        HAMD_count = df1[f'V{visit}-HAMD-TOTAL'].count()

        if HAMD_count == 0:
            HAMD_upper = 0
            HAMD_lower = 0
            HAMD_mean = 0

        else:
            HAMD_upper = HAMD_mean + (1.96*HAMD_standard/math.sqrt(HAMD_count))
            HAMD_lower = HAMD_mean - (1.96*HAMD_standard/math.sqrt(HAMD_count))

        hamdMeans.append(HAMD_mean)
        upperBounds.append(HAMD_upper)
        lowerBounds.append(HAMD_lower)

    chart_data = pd.DataFrame({'CI Lower':lowerBounds, 'CI Upper':upperBounds, 'Mean HAMD Score':hamdMeans})
    st.line_chart(chart_data)
    
    
    st.title("Sectional HAMD")
    select = st.selectbox(
    "Select HAMD",
    ("HAMD01", "HAMD02", "HAMD03", "HAMD04", "HAMD05", "HAMD06", "HAMD07", "HAMD08", "HAMD09", "HAMD10", "HAMD11", "HAMD12", "HAMD13", "HAMD14", "HAMD15", "HAMD16", "HAMD17",),
    )
    
    text_s = open('views/Drug Analysis/drugINFO.txt', 'r').read()
    
    textdic = {}
    for i in range (1,18):
        if i < 10:
            textdic[f'HAMD0{i}'] = text_s.split('\n\n')[i-1]
        else:
            textdic[f'HAMD{i}'] = text_s.split('\n\n')[i-1]
            
    st.text("HAMD" + textdic[select])
    
    
    index = select.replace("HAMD", "")
    
    hamdMeans = []
    upperBounds = []
    lowerBounds = []

    for visit in range (1,10): 
        HAMD_standard = df1[f'V{visit}-HAMD{index}'].std()
        HAMD_mean = df1[f'V{visit}-HAMD{index}'].mean()
        HAMD_count = df1[f'V{visit}-HAMD{index}'].count()

        if HAMD_count == 0:
            HAMD_upper = 0
            HAMD_lower = 0
            HAMD_mean = 0

        else:
            HAMD_upper = HAMD_mean + (1.96*HAMD_standard/math.sqrt(HAMD_count))
            HAMD_lower = HAMD_mean - (1.96*HAMD_standard/math.sqrt(HAMD_count))

        hamdMeans.append(HAMD_mean)
        upperBounds.append(HAMD_upper)
        lowerBounds.append(HAMD_lower)

    chart_data = pd.DataFrame({'CI Lower':lowerBounds, 'CI Upper':upperBounds, 'Mean HAMD Score':hamdMeans})
    st.line_chart(chart_data)
    
    