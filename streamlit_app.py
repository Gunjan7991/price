import streamlit as st
from datetime import datetime, timedelta
from store_data import (
    create_db_and_tables,
    write_data,
    read_all_data,
    read_latest_data,
    read_specific_data,
)
from scraper import get_heating_oil, write_csv, plot_heating_oil_prices
import pandas as pd

# ✅ Set Page Config (Must be First)
st.set_page_config(page_title="Heating Oil Price Tracker", layout="wide")

# Initialize database
create_db_and_tables()

# ✅ Function to fetch and save latest price every 24 hours
def fetch_price_if_needed():
    now = datetime.utcnow()

    # Check if last fetch time exists in session state
    if "last_fetch_time" not in st.session_state:
        st.session_state.last_fetch_time = now - timedelta(days=1)  # Set to yesterday to trigger first fetch

    # If 24 hours have passed, fetch new data
    if now - st.session_state.last_fetch_time >= timedelta(hours=24):
        st.session_state.last_fetch_time = now  # Update last fetch time
        price = get_heating_oil()
        write_data(price)  # Save to Database
        write_csv(price)   # Save to CSV
        st.success(f"✅ Automatically fetched & saved new price: {price}")

# ✅ Run fetch function when app starts
fetch_price_if_needed()

# ✅ Display Last Updated Time
st.title("📊 Heating Oil Price Tracker")
st.info(f"🔥 **Last Updated:** {st.session_state.last_fetch_time.strftime('%Y-%m-%d %H:%M:%S')}")

# ✅ Sidebar Navigation
st.sidebar.title("Menu")
menu_option = st.sidebar.radio(
    "Select an option:",
    ["View All Data", "View Latest Data", "View Data for Specific Date", "Plot Graph"]
)

# ✅ 1️⃣ View All Data
if menu_option == "View All Data":
    st.subheader("📌 All Stored Prices")
    all_data = read_all_data()

    if all_data:
        df = pd.DataFrame([(d.created_at, d.pricing) for d in all_data], columns=["Timestamp", "Price"])
        st.dataframe(df)
    else:
        st.warning("⚠️ No data found in the database.")

# ✅ 2️⃣ View Latest Data
elif menu_option == "View Latest Data":
    st.subheader("📌 Latest Recorded Price")
    latest = read_latest_data()

    if latest:
        st.write(f"🔥 **Latest Price:** {latest.pricing}")
        st.write(f"📅 **Timestamp:** {latest.created_at}")
    else:
        st.warning("⚠️ No latest data found.")

# ✅ 3️⃣ View Data for a Specific Date
elif menu_option == "View Data for Specific Date":
    st.subheader("📌 Fetch Data for a Specific Date")
    date = st.date_input("Select a date", datetime.utcnow().date())
    specific_data = read_specific_data(date.strftime("%Y-%m-%d"))

    if specific_data:
        df = pd.DataFrame([(d.created_at, d.pricing) for d in specific_data], columns=["Timestamp", "Price"])
        st.dataframe(df)
    else:
        st.warning(f"⚠️ No data found for {date.strftime('%Y-%m-%d')}.")

# ✅ 4️⃣ Plot Graph from CSV
elif menu_option == "Plot Graph":
    st.subheader("📌 Price Trend Graph")
    csv_file = st.text_input("Enter CSV filename", "heating_oil_prices.csv")

    if st.button("Plot Graph"):
        plot_heating_oil_prices(csv_file)  # Calls the fixed function
