import logging
from datetime import datetime
from store_data import (
    create_db_and_tables,
    write_data,
    read_all_data,
    read_latest_data,
    read_specific_data,
)
from scraper import plot_heating_oil_prices, write_csv, get_heating_oil 


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def menu():
    while True:
        print("\n📊 Heating Oil Price Tracker Menu 📊")
        print("1️⃣ Fetch & Save Latest Price")
        print("2️⃣ Read All Data")
        print("3️⃣ Read Latest Data")
        print("4️⃣ Read Data for Specific Date")
        print("5️⃣ Plot Graph from CSV")
        print("0️⃣ Exit")

        choice = input("Enter your choice (1-6 or  0 to exit): ")

        if choice == "1":
            # Get today's date
            curr_date = datetime.utcnow().date()
            
            # Fetch the latest record from the DB
            latest_record = read_latest_data()
            
            # Compare dates
            if not latest_record or curr_date != latest_record.created_at.date():
                price = get_heating_oil()
                write_data(price)  # Save to database
                write_csv(price)   # Save to CSV
                print(f"✅ New price {price} saved!")
            else:
                print("✅ Today's price data is already recorded.")

        elif choice == "2":
            all_data = read_all_data()
            for record in all_data:
                print(record)

        elif choice == "3":
            latest = read_latest_data()
            print(f"🔥 Latest Data: {latest}")

        elif choice == "4":
            date = input("Enter date (YYYY-MM-DD): ")
            specific_data = read_specific_data(date)
            if specific_data:
                for record in specific_data:
                    print(record)
            else:
                print("⚠️ No data found for this date.")


        elif choice == "5":
            csv_file = input("Enter CSV filename (default: heating_oil_prices.csv): ") or "heating_oil_prices.csv"
            plot_heating_oil_prices(csv_file)

        elif choice == "0":
            print("🚀 Exiting Program. Goodbye!")
            break

        else:
            print("❌ Invalid choice, please enter a number between 1-7.")

if __name__ == "__main__":
    create_db_and_tables()  # Ensure DB is ready
    menu()
