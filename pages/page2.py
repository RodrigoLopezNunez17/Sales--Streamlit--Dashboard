import streamlit as st, pandas as pd, plotly.express as px

st.set_page_config(
    page_title="Temporal Analysis ⏰",
    page_icon="⏰",
    layout="wide"
)

@st.cache_data
def GetExcelData():
    df = pd.read_excel(r"Datasets/supermarkt_sales.xlsx", engine='openpyxl',skiprows=3, usecols='B:R')
    df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour
    return df

sales = GetExcelData()

with st.sidebar:
    cityFilter = st.multiselect(
        label="City",
        options=sales['City'].unique(),
        default=sales['City'].unique(),
    )

    genderFilter = st.multiselect(
        label="Gender",
        options=sales['Gender'].unique(),
        default=sales['Gender'].unique(),
    )

    customerTypeFilter = st.multiselect(
        label="Customer Type",
        options=sales['Customer_type'].unique(),
        default=sales['Customer_type'].unique(),
    )


salesFiltered = sales.query(
    "City == @cityFilter & Gender == @genderFilter & Customer_type == @customerTypeFilter"
)

st.title("Temporal Analysis 🕑")
st.markdown("---")

leftColumn, rightColumn = st.columns(2)

with leftColumn:
    salesByDate = salesFiltered.groupby('Date')['Total'].sum()
    fig_salesByDate = px.line(
        salesByDate,
        title="Total Sales by Date"
    )
    st.plotly_chart(fig_salesByDate)
with rightColumn:
    salesByHour = salesFiltered.groupby('Hour')['Total'].sum()
    fig_salesByHour = px.line(
        salesByHour,
        title='Total Sales by Hour'
    )
    st.plotly_chart(fig_salesByHour)

st.markdown("---")
st.image("ETL/Images/forecast.png")
