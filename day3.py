import pandas as pd
import streamlit as st
import plotly_express as px
from PIL import Image

st.set_page_config(page_title='Survey Result')
st.title('Survey Results 2021')

#load data
excel_file='Survey_Results.xlsx'
sheet_name='DATA'

df=pd.read_excel(excel_file,
                 sheet_name=sheet_name,
                 usecols='B:D',
                 header=3)
df_participant=pd.read_excel(excel_file,sheet_name=sheet_name,usecols='F:G',
                             header=3)
df_participant.dropna(inplace=True)
col1,col2=st.columns(2)
col1.dataframe(df)
col2.dataframe(df_participant)
#streamlit selection

departement=df['Department'].unique().tolist()
age=df['Age'].unique().tolist()

age_selection=st.slider('Age:',
                        min_value=min(age),
                        max_value=max(age),
                        value=(min(age),max(age)))

departement_selection=st.multiselect('Department:',
                                     departement,
                                     default=departement)
mask=(df['Age'].between(*age_selection)) & (df['Department'].isin(departement_selection))
number_of_result=df[mask].shape[0]
st.markdown(f'Avalilable Results: {number_of_result}')

#group dataframe after selection

df_group=df[mask].groupby(by=['Rating']).count()[['Age']]
df_group=df_group.rename(columns={'Age':'Votes'})
df_group=df_group.reset_index()

bar_chart=px.bar(df_group,
                 x='Rating',
                 y='Votes',
                 text='Votes',
                 color_discrete_sequence=['#F63366']*len(df_group),
                 template='plotly_white')
st.plotly_chart(bar_chart)
pie_chart=px.pie(df_participant,
                 title='Total Partisipant',
                 values='Participants',
                 names='Departments')
st.plotly_chart(pie_chart)