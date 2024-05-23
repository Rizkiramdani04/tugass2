import streamlit as st #menginstal streamlit
import pandas as pd #menginstal pandas
import plotly_express as px #mengintasl ployly
import base64
from io import StringIO,BytesIO

#setup
st.set_page_config(page_title='Excel Plotter',page_icon='👩‍🚀')
st.title('Excel Plotter 🥗')
st.subheader('Tentang File Excel')

uploade_file=st.file_uploader('masukan File Excel',type='xlsx')
if uploade_file:
    st.markdown('---')
    df=pd.read_excel(uploade_file,engine='openpyxl')
    st.dataframe(df)
    group_columns=st.selectbox(
        'Untuk Di Analisis',
        ('Ship Mode','Segment',"Category",'Sub-Category')
    )

#group data frame
output_colum=['Sales','Profit']
df_group=df.groupby(by=[group_columns],as_index=False)[output_colum].sum()

#flot dataframe
fig=px.bar(
    df_group,
    x=group_columns,
    y='Sales',
    color='Profit',
    color_continuous_scale=['red','yellow','green'],
    template='plotly_white',
    title=f'<b>Sales & Profit By {group_columns}</b>'
)
st.plotly_chart(fig)



