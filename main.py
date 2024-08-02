import pandas as pd, streamlit as st, plotly.express as px

st.set_page_config(
    page_title="Sales",
    page_icon="🦈",
    layout="wide"
)

def MyanmarLatLon(s : str)->str:
        if s == 'Mandalay':
            return "21.97473,96.08359"
        elif s == 'Yangon':
            return "16.871311,96.199379"
        elif s == "Naypyitaw":
            return "19.763306,96.078510"

@st.cache_data
def GetExcelData():
    df = pd.read_excel(r"Datasets/supermarkt_sales.xlsx", engine='openpyxl',skiprows=3, usecols='B:R')
    df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour
    df[['Lat', 'Lon']] = df['City'].apply(MyanmarLatLon).str.split(",", expand=True).astype(float)

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

leftColumn, middleLeftColumn, middleRightColumn, rightColumn = st.columns(4)

with leftColumn:
    percetage = salesFiltered.shape[0] / sales.shape[0] * 100
    st.title("Percentage Data")
    st.markdown(f"## {percetage:.0f}%")

with middleLeftColumn:
    totalSales = salesFiltered['Total'].sum()
    st.header("Total Sales 💵")
    st.markdown(f"## USD ${totalSales:,.2f}")

with middleRightColumn:
    avgSalesTransaction = salesFiltered['Total'].mean()
    st.header("Average Sales Per Transaction 👩🏻‍💻")
    st.markdown(f"## USD ${avgSalesTransaction:.2f}")

with rightColumn:
    avgRating = salesFiltered['Rating'].mean()
    st.header("Average Rating")
    st.markdown(f"## {avgRating:.2} {"⭐" * round(avgRating)}")

st.markdown("---")
leftColumn, rightColumn = st.columns(2)

with leftColumn:
    st.header("Total Sales by Product Line and Payment")
    salesByProductLine = salesFiltered.groupby(by=["Product line",'Payment'])[['Total']].sum().reset_index().sort_values(by='Total', ascending=False)
    fig_salesByProductLine = px.bar(
        data_frame=salesByProductLine,
        y='Product line',
        x='Total',
        color='Payment',
        text='Payment',
        orientation='h'
    )
    st.plotly_chart(fig_salesByProductLine)

with rightColumn:
    st.header("Total Sales by City")
    cities = salesFiltered[["City", 'Total']].groupby('City').sum().reset_index()
    cities[['Lat','Lon']] = cities['City'].apply(MyanmarLatLon).str.split(",", expand=True).astype(float)
    st.map(
        data=cities,
        latitude='Lat',
        longitude='Lon',
        size='Total'
    )