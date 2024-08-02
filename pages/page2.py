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
    df['Date'] = df['Date'].dt.strftime("%Y-%m-%d")
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

    minDate, maxDate = st.select_slider(
        label='Date',
        options=sorted(sales['Date'].unique()),
        value=[sales['Date'].min(), sales['Date'].max()]
    )

    minHour, maxHour = st.select_slider(
        label="Hour",
        options=sorted(sales['Hour'].unique()),
        value=[sales['Hour'].min(), sales['Hour'].max()]
    )   


salesFiltered = sales.query(
    "City == @cityFilter & Gender == @genderFilter & Customer_type == @customerTypeFilter & (Hour >=@minHour & Hour <= @maxHour) & (Date >= @minDate & Date <= @maxDate)"
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

tab1, tab2 = st.tabs(['Branch', 'Forecast'])

with tab1:
    st.title("Total Sales by Branch")
    salesByBranch = salesFiltered.groupby(by='Branch')['Total'].sum().reset_index()
    fig_salesByBranch = px.pie(
        data_frame=salesByBranch,
        names='Branch',
        values="Total",
        hole=0.25
    )
    st.plotly_chart(fig_salesByBranch)



with tab2:
    st.title("Total Sales Forecast (SARIMAX Model) 🔮")
    st.image("ETL/Images/forecast.png")
