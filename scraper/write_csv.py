import csv
from datetime import datetime

def write_csv(heating_oil_price: float, csv_file: str = "heating_oil_prices.csv") -> None:
    """
    Writes the heating oil price along with the timestamp to a CSV file.

    :param heating_oil_price: The latest heating oil price to be recorded.
    :param csv_file: The filename where data should be stored (default: 'heating_oil_prices.csv').
    """
    # Data to save
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_row = [timestamp, heating_oil_price]

    # Append data to CSV
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data_row)

    print(f"✅ Data saved to {csv_file}")

