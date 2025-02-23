from sqlmodel import SQLModel, create_engine, Field, Session, select
import uuid
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Daily_Price(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    pricing: float
    created_at: datetime | None = Field(default_factory=datetime.utcnow)

# Database Configuration
sqlite_file_name = "b99.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# Create Tables
def create_db_and_tables():
    try:
        SQLModel.metadata.create_all(engine)
        logging.info("✅ Database Initialized.")
    except Exception as e:
        logging.fatal(f"❌ Failed to initialize database: {e}")

# Write Data
def write_data(price: float):
    """Inserts price data into the database with timestamp."""
    try:
        with Session(engine) as session:
            new_price = Daily_Price(pricing=price)
            session.add(new_price)
            session.commit()
            logging.info(f"✅ Data saved: {price}")
    except Exception as e:
        logging.error(f"❌ Database Error: {e}")

def read_all_data():
    """Fetches all records from the database."""
    try:
        with Session(engine) as session:
            results = session.exec(select(Daily_Price)).all()
            return results
    except Exception as e:
        logging.error(f"❌ Error reading all data: {e}")
        return []

def read_latest_data():
    """Fetches the most recent record from the database."""
    try:
        with Session(engine) as session:
            result = session.exec(select(Daily_Price).order_by(Daily_Price.created_at.desc())).first()
            return result
    except Exception as e:
        logging.error(f"❌ Error reading latest data: {e}")
        return None

def read_specific_data(date: str):
    """
    Fetches records for a specific date.
    
    :param date: Date in format 'YYYY-MM-DD'
    """
    try:
        # Convert string date to datetime format
        date_start = datetime.strptime(date, "%Y-%m-%d")
        date_end = date_start.replace(hour=23, minute=59, second=59)  # Get entire day's data

        with Session(engine) as session:
            results = session.exec(select(Daily_Price)
                                   .where(Daily_Price.created_at >= date_start)
                                   .where(Daily_Price.created_at <= date_end)).all()
            return results
    except Exception as e:
        logging.error(f"❌ Error reading data for {date}: {e}")
        return []