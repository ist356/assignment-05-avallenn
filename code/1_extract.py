import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl
  
#TODO Write your extraction code here
statesurl = "https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv"
statedf = pd.read_csv(statesurl)
statedf['lineage'] = 'statecsv'
surveyurl = "https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv"
surveydf = pd.read_csv(surveyurl)
surveydf['lineage'] = 'surveycsv'
surveydf['Year'] = surveydf['Timestamp'].apply(pl.extract_year_mdy)

surveydf.to_csv('cache/survey.csv', index=False)
statedf.to_csv('cache/states.csv', index=False)

st.dataframe(statedf)
st.dataframe(surveydf)
