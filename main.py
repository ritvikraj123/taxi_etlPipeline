from helper import (
    postgres_connection,
    init_logger,
    create_tables,
    close_connection,
    create_database
)
from etl import transform_data
from insert_data import insert_data
import pandas as pd

def main():
    # Initialize logger
    init_logger()

    # Define the database name
    database_name = 'TaxiRides'

    # Drop the old database and create a new one
    create_database(database_name)

    # Connect to the newly created PostgreSQL database
    conn = postgres_connection(database_name)

    if conn:
        # Create tables in the database
        create_tables(conn)

        # Load your taxi data into a DataFrame (replace with actual CSV loading or data retrieval)
        df = pd.read_csv('uber_data.csv')  # Replace with your actual data source

        # Transform the data
        data_dict = transform_data(df)

        # Insert data into PostgreSQL tables
        insert_data(data_dict)  # Updated to remove the connection parameter

        # Close the database connection
        close_connection(conn)

if __name__ == "__main__":
    main()
