import pandas as pd, streamlit as st, plotly.express as px

st.set_page_config(
    page_title="Sales",
    page_icon="🦈",
    layout="wide"
)

@st.cache_data
def GetExcelData():
    df = pd.read_excel(r"Datasets/supermarkt_sales.xlsx", engine='openpyxl',skiprows=3, usecols='B:R')
    df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour
    return df

sales = GetExcelData()

st.title("Sales Dashboard 🛍️")
st.markdown("---")

with st.sidebar:
    st.subheader("Please Filter Here")

    cityFilter = st.multiselect(
        label="City",
        options=sales['City'].unique(),
        default=sales['City'].unique()
    )

    customerTypeFilter = st.multiselect(
        label="Customer Type",
        options=sales['Customer_type'].unique(),
        default=sales["Customer_type"].unique()
    )

    genderFilter = st.multiselect(
        label="Gender",
        options=sales['Gender'].unique(),
        default=sales['Gender'].unique()
    )

salesFiltered = sales.query(
    "City == @cityFilter & Customer_type == @customerTypeFilter & Gender == @genderFilter"
)

leftColumn, middleColumn, rightColumn = st.columns(3)

with leftColumn:
    totalSales = salesFiltered['Total'].sum()
    st.header("Total Sales 💵")
    st.subheader(f"USD ${totalSales:,.2f}")

with middleColumn:
    avgSalesTransaction = salesFiltered['Total'].mean()
    st.header("Average Sales Per Transaction 👩🏻‍💻")
    st.subheader(f"USD ${avgSalesTransaction:.2f}")

with rightColumn:
    avgRating = salesFiltered['Rating'].mean()
    st.header("Average Rating")
    st.subheader(f"{avgRating:.2} {"⭐" * round(avgRating)}")

leftColumn, rightColumn = st.columns(2)

with leftColumn:
    salesByProductLine = salesFiltered.groupby(by=["Product line"])['Total'].sum().sort_values(ascending=True)
    fig_salesByProductLine = px.bar(
        data_frame=salesByProductLine,
        title="Sales By Product Line",
        orientation='h'
    )
    st.plotly_chart(fig_salesByProductLine)

with rightColumn:
    salesByHour = salesFiltered.groupby(by=['Hour'])['Total'].sum()
    fig_salesByHour = px.bar(
        data_frame=salesByHour,
        title="Sales By Hour"
    )
    st.plotly_chart(fig_salesByHour)
