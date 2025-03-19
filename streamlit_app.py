import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
#create dropdown box
drop_option = st.selectbox(
    "What category do you prefer?",
    df['Category'].unique(),
    index=None,
    placeholder="Select category...",
)
st.write("You selected:", drop_option)
cat_df = df[df['Category'] == drop_option]
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")

multi_options = st.multiselect(
    "Select Subcategories (if applicable)",
    cat_df['Sub_Category'].unique(),
)

st.write("You selected:", multi_options)
multi_df = cat_df[cat_df['Sub_Category'].isin(multi_options)]
sales_by_month_multi = multi_df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.line_chart(sales_by_month_multi, y="Sales")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
sum_sales = round(sum(multi_df['Sales']), 2)
sum_all_sales = round(sum(df['Sales']), 2)
sum_profit = round(sum(multi_df['Profit']), 2)

df["Profit_Margin"] = (df["Profit"] / df["Sales"]) * 100  # Calculate profit margin
multi_df["Profit_Margin"] = (multi_df["Profit"] / multi_df["Sales"]) * 100
avg_margin = round(multi_df["Profit_Margin"].mean(), 2)
avg_margin_all = round(df["Profit_Margin"].mean(), 2)
delta_margin = round(avg_margin - avg_margin_all, 2)

st.metric(label="Total Sales", value= sum_sales)
st.metric(label="Total Profit", value=sum_profit)
st.metric(label="Profit Margin", value=f"{avg_margin}%", delta=f"{delta_margin}%")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
