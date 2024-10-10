import pandas as pd
import streamlit as st
import pandaslib as pl

# TODO: Write your transformation code here
#Load the states and survey data from the cache into dataframes
states_data = pd.read_csv('cache/states.csv')
survey_data = pd.read_csv('cache/survey.csv')
st.dataframe(survey_data)
#create a unique list of years from the survey data
unique_years = survey_data['year'].unique()

#For each year in the survey data, load the cost of living 
cols = []
for year in unique_years:
    col = pd.read_csv(f'cache/col_{year}.csv')
    cols.append(col)

col_data = pd.concat(cols, ignore_index=True)

# clean "Which country do you work in?" column
survey_data['_country'] = survey_data['What country do you work in?'].apply(pl.clean_country_usa)

# join state data with survey data
survey_states_combined = survey_data.merge(states_data, left_on="If you're in the U.S., what state do you work in?", right_on='State', how='inner')
survey_states_combined['_full_city'] = survey_states_combined['What city do you work in?'] + ', ' + survey_states_combined['Abbreviation'] + ', ' + survey_states_combined['_country']

#create the dataframe combined by matching the survey_states_combined to cost of living data matching on the year and _full_city columns'''
combined = survey_states_combined.merge(col_data, left_on=['year', '_full_city'], right_on=['year', 'City'], how='inner')


#normalize annual salary based on cost of living
combined['__annual_salary_cleaned'] = combined["What is your annual salary? (You'll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)"].apply(pl.clean_currency)
combined['_annual_salary_adjusted'] = combined.apply(lambda row: row['__annual_salary_cleaned'] * (100 / row['Cost of Living Index']), axis=1)

combined.to_csv('cache/combined.csv', index=False)

#create pivot table to show average salary with full city in row and age in column
pivot1 = combined.pivot_table(index='_full_city', columns='How old are you?', values='_annual_salary_adjusted', aggfunc='mean')
pivot1.to_csv('cache/annual_salary_adjusted_by_location_and_age.csv')

pivot2 = combined.pivot_table(index='_full_city', columns='What is your highest level of education completed?', values='_annual_salary_adjusted', aggfunc='mean')
st.dataframe(pivot2)
pivot2.to_csv('cache/annual_salary_adjusted_by_location_and_education.csv')