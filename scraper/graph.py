import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def plot_heating_oil_prices(csv_file="heating_oil_prices.csv"):
    """
    Reads the CSV file and plots the Heating Oil price trend over time inside Streamlit.
    
    :param csv_file: The CSV file containing historical price data.
    """
    try:
        df = pd.read_csv(csv_file, names=["Timestamp", "Price"], parse_dates=["Timestamp"])
        
        if df.empty:
            st.warning("⚠️ No data available in CSV.")
            return
        
        df = df.sort_values(by="Timestamp")  # Ensure sorted order

        # Create the figure
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df["Timestamp"], df["Price"], marker="o", linestyle="-", label="Heating Oil Price")

        ax.set_xlabel("Timestamp")
        ax.set_ylabel("Price (USD)")
        ax.set_title("Heating Oil Price Trend")
        plt.xticks(rotation=45)
        ax.legend()
        ax.grid(True)

        # Embed in Streamlit
        st.pyplot(fig)

    except FileNotFoundError:
        st.error(f"❌ File {csv_file} not found.")
    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
