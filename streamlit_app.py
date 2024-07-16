import plotly.express as px
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import sqlite3
st.set_page_config(layout="wide")


"""
# Welcome!

"""

file_path = "/Users/nitinupadhyay/Library/CloudStorage/OneDrive-SharedLibraries-SpotlessFacilityServicesPtyLtd/0.SPC - Documents/2_Category_Projects/1.HVAC/Data/HVAC Combined Data/Combined_Supplier_data_v2.xlsx"

# Key Columns for Analysis
item_num_column = "Supplier Item Code"
item_column = 'Supplier Line Item Description  (Product / Service)'
spend_column = 'Total Line Item Invoice Value (AUD) (Excl. GST)'
unit_price_column = 'Unit Price (AUD) (Excl. Delivery & GST)'
qty_supplied_column = 'Quantity Supplied '
category_column = "Category Level 3"


@st.cache_data
def load_data():

    df = pd.read_excel(file_path, sheet_name="Sheet1")
    clean_columns = [col.replace("\n", " ")
                     for col in df.columns.values.tolist()]
    df.columns = clean_columns
    return df


def spend_by_column(df: pd.DataFrame, groupby_col, spend_column):
    spend_by_col = df.groupby([groupby_col])[spend_column].sum().reset_index()
    spend_by_col = spend_by_col.sort_values(by=spend_column, ascending=False)
    spend_by_col[spend_column] = spend_by_col[spend_column].apply(lambda x: f"{
                                                                  x:,.2f}")
    return spend_by_col


df = load_data()


spend_by_category = spend_by_column(df, category_column, spend_column)

st.write("Top 10 Records")
st.write(df.head(10))

st.write("Spend by Category")
st.write(spend_by_category)

spend_by_category_chart = px.bar(spend_by_category, x=category_column, y=spend_column,
                                 title='Spend by Category', labels={'Total Line Item Invoice Value (AUD) (Excl. GST)': "Spend"})
# Show the plot in Streamlit
st.plotly_chart(spend_by_category_chart)
