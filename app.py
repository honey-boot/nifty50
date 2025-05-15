import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Stock Performance Dashboard", layout="wide")

st.title("📊 Data-Driven Stock Analysis: Stock Performance Dashboard")

# Load datasets (assumes CSVs already uploaded and in working dir)
@st.cache_data
def load_data():
    volatile = pd.read_csv("viz1_top_10_volatile_stocks.csv")
    cum_returns = pd.read_csv("viz2_top5_cumulative_returns.csv", parse_dates=['date'])
    sector_perf = pd.read_csv("viz3_sector_wise_performance.csv")
    corr_matrix = pd.read_csv("viz4_stock_correlation_matrix.csv", index_col=0)
    monthly_returns = pd.read_csv("viz5_monthly_returns_all.csv")
    return volatile, cum_returns, sector_perf, corr_matrix, monthly_returns

volatile, cum_returns, sector_perf, corr_matrix, monthly_returns = load_data()

# Sidebar for navigation
page = st.sidebar.selectbox("Choose Dashboard View", [
    "Volatility Analysis",
    "Cumulative Returns",
    "Sector-wise Performance",
    "Stock Price Correlation",
    "Monthly Gainers & Losers"
])

if page == "Volatility Analysis":
    st.header("Top 10 Most Volatile Stocks")
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(data=volatile, x='Ticker', y='Volatility', palette="Reds_r", ax=ax)
    ax.set_ylabel("Volatility (Std Dev of Daily Returns)")
    ax.set_xlabel("Stock Ticker")
    ax.set_title("Top 10 Most Volatile Stocks")
    st.pyplot(fig)

elif page == "Cumulative Returns":
    st.header("Cumulative Return Over Time for Top 5 Performing Stocks")
    fig, ax = plt.subplots(figsize=(12,6))
    for ticker in cum_returns['Ticker'].unique():
        data = cum_returns[cum_returns['Ticker'] == ticker]
        ax.plot(data['date'], data['Cumulative Return'], label=ticker)
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative Return")
    ax.set_title("Cumulative Returns Over the Year")
    ax.legend()
    st.pyplot(fig)

elif page == "Sector-wise Performance":
    st.header("Average Yearly Return by Sector")
    fig, ax = plt.subplots(figsize=(12,6))
    sns.barplot(data=sector_perf, x='Sector', y='Yearly Return', palette="coolwarm", ax=ax)
    ax.set_ylabel("Average Yearly Return")
    ax.set_xlabel("Sector")
    ax.set_title("Sector-wise Average Yearly Return")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

elif page == "Stock Price Correlation":
    st.header("Stock Price Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(14,10))
    sns.heatmap(corr_matrix, cmap='coolwarm', center=0, square=True, linewidths=0.5, cbar_kws={"shrink": .5}, ax=ax)
    ax.set_title("Correlation Matrix of Stock Daily Returns")
    st.pyplot(fig)

elif page == "Monthly Gainers & Losers":
    st.header("Top 5 Gainers and Losers by Month")
    
    # Prepare month list sorted
    monthly_returns['YearMonth'] = monthly_returns['YearMonth'].astype(str)
    months = sorted(monthly_returns['YearMonth'].unique())
    
    selected_month = st.selectbox("Select Month", months)

    # Filter data for selected month
    month_data = monthly_returns[monthly_returns['YearMonth'] == selected_month]

    # Top 5 Gainers
    top_gainers = month_data.sort_values('Monthly Return', ascending=False).head(5)
    # Top 5 Losers
    top_losers = month_data.sort_values('Monthly Return').head(5)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Top 5 Gainers - {selected_month}")
        fig, ax = plt.subplots(figsize=(7,5))
        sns.barplot(data=top_gainers, x='Ticker', y='Monthly Return', palette='Greens', ax=ax)
        ax.set_ylabel("Monthly Return (%)")
        ax.set_xlabel("Ticker")
        ax.set_title("Top 5 Monthly Gainers")
        st.pyplot(fig)

    with col2:
        st.subheader(f"Top 5 Losers - {selected_month}")
        fig, ax = plt.subplots(figsize=(7,5))
        sns.barplot(data=top_losers, x='Ticker', y='Monthly Return', palette='Reds_r', ax=ax)
        ax.set_ylabel("Monthly Return (%)")
        ax.set_xlabel("Ticker")
        ax.set_title("Top 5 Monthly Losers")
        st.pyplot(fig)