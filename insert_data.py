import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import logging

# Initialize the logger
logging.basicConfig(level=logging.INFO)

# Database connection details
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'TaxiRides'
DB_USER = 'postgres'
DB_PASSWORD = 'password'

# Create a SQLAlchemy engine
def create_sqlalchemy_engine():
    connection_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(connection_string)
    return engine

def insert_data(data_dict):
    """
    Insert transformed data into the PostgreSQL database using SQLAlchemy.
    """
    engine = create_sqlalchemy_engine()

    # Inserting data into the database tables
    try:
        data_dict['datetime_dim'].to_sql('DateTime', engine, if_exists='append', index=False)
        logging.info("Inserted datetime_dim into the DateTime table.")

        data_dict['passenger_count_dim'].to_sql('PassengerCount', engine, if_exists='append', index=False)
        logging.info("Inserted passenger_count_dim into the PassengerCount table.")

        data_dict['trip_distance_dim'].to_sql('TripDistance', engine, if_exists='append', index=False)
        logging.info("Inserted trip_distance_dim into the TripDistance table.")

        data_dict['rate_code_dim'].to_sql('RateCode', engine, if_exists='append', index=False)
        logging.info("Inserted rate_code_dim into the RateCode table.")

        data_dict['pickup_location_dim'].to_sql('PickupLocation', engine, if_exists='append', index=False)
        logging.info("Inserted pickup_location_dim into the PickupLocation table.")

        data_dict['dropoff_location_dim'].to_sql('DropoffLocation', engine, if_exists='append', index=False)
        logging.info("Inserted dropoff_location_dim into the DropoffLocation table.")

        data_dict['payment_type_dim'].to_sql('PaymentType', engine, if_exists='append', index=False)
        logging.info("Inserted payment_type_dim into the PaymentType table.")

        data_dict['trip_table'].to_sql('Trip', engine, if_exists='append', index=False)
        logging.info("Inserted trip_table into the Trip table.")

    except Exception as e:
        logging.error(f"Error inserting data into database: {e}")


