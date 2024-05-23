#mengimport library 
import pandas as  pd
import streamlit as st
import plotly_express as px

#membuat emoji dan mengganti title
st.set_page_config(page_title="Sales Dashboard",page_icon=":bar_chart:",layout='wide')

#memasukan file excel
@st.cache_data
def get_data_from_excel():
    df=pd.read_excel(
        io='supermarkt_sales.xlsx',
        engine='openpyxl',
        sheet_name='Sales',
        skiprows=3,
        usecols='B:R',
        nrows=1000,
    )#memasukan file excel
    df['hour']=pd.to_datetime(df['Time'], format="%H:%M:%S").dt.hour #merubah tipe waktu
    return df

df=get_data_from_excel()#memanggil fungsi

#sidebar
st.sidebar.header('Tolong Filter Ya')
city=st.sidebar.multiselect(
    'Masukan Kota',
    options=df['City'].unique(),
    default=df['City'].unique()
)
customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

df_selection = df.query(
    "City == @city & Customer_type ==@customer_type & Gender == @gender"
)
#check dataframe menggunakan if
if df_selection.empty:
    st.warning('Tidak Ada data')
    st.stop()

#mainpage
st.title(':bar_chart: Dashboard Sales')
st.markdown("##")

#dataframe
st.dataframe(df_selection.head())
st.markdown("""---""")

#top kpi

total_sales=int(df_selection['Total'].sum())
average_rating=round(df_selection['Rating'].mean(),1)
star_rating=":star:"*int(round(average_rating,0))
average_sale_by_transtion=round(df_selection['Total'].mean(),2)

left_column,middle_column,right_columns=st.columns(3)
with left_column:
    st.subheader('Total Sales')
    st.subheader(f'Us $ {total_sales:,}')
with middle_column:
    st.subheader('Average Rating:')
    st.subheader(f'{average_rating} {star_rating}')

with right_columns:
    st.subheader("Average Sales Per Transaction")
    st.subheader(f'US $ {average_sale_by_transtion}')

st.markdown("""---""")


#sales by product line
sales_by_product_line=df_selection.groupby(by=['Product line'])[['Total']].sum().sort_values(by='Total')
fig_product_sales=px.bar(
    sales_by_product_line,
    x='Total',
    y=sales_by_product_line.index,
    orientation='h',
    title='<b>Sales By Product Line</b>',
    color_discrete_sequence=['#006769'] *len(sales_by_product_line),
    template='plotly_white',
)
fig_product_sales.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False))
)

#sales by hour
sales_by_hour=df_selection.groupby(by=['hour'])[['Total']].sum()
fig_hourly_sales=px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y='Total',
    title='<b> Sales By Hour</b>',
    color_discrete_sequence=["#FFFAE6"]*len(sales_by_hour),
    template='plotly_white',
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode='linear'),
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=dict(showgrid=False)
)

left_column,right_columns=st.columns(2)
left_column.plotly_chart(fig_hourly_sales,use_container_width=True)
right_columns.plotly_chart(fig_product_sales,use_container_width=True)



hide_st_style="""
                <style>
                #MainMenu {visibility:hidden;}
                footer {visibility:hidden;}
                header{visibility:hidden;}
                </style>
"""
st.markdown(hide_st_style,unsafe_allow_html=True)






