# Taxi Rides Data Processing

## Overview
This project processes taxi ride data using PostgreSQL for database management and Python for ETL (Extract, Transform, Load) operations. The system automates database setup, transforms raw taxi data, and inserts it into structured tables.

## Project Structure
```
├── createTable_sqlStatement.py  # Contains SQL table creation scripts
├── etl.py                       # Transforms raw data
├── helper.py                    # Helper functions for database operations
├── insert_data.py                # Inserts transformed data into PostgreSQL
├── main.py                       # Main script to run the entire pipeline
├── sampleQueries.sql             # Sample SQL queries for testing
```

## Prerequisites
Ensure you have the following installed:
- Python 3.x
- PostgreSQL
- Required Python libraries (install with `pip install -r requirements.txt` if available)

## Setting Up PostgreSQL
### 1. Install PostgreSQL
Follow the instructions from [PostgreSQL's official site](https://www.postgresql.org/download/) to install PostgreSQL.

### 2. Configure PostgreSQL
- Ensure the PostgreSQL service is running.
- Create a PostgreSQL user and database (or modify credentials in `helper.py` and `insert_data.py`).

#### Create Database and User (if necessary):
```sql
CREATE DATABASE TaxiRides;
CREATE USER postgres WITH ENCRYPTED PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE TaxiRides TO postgres;
```

### 3. Update Database Credentials
Modify `helper.py` and `insert_data.py` to use your PostgreSQL credentials:
```python
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'TaxiRides'
DB_USER = 'postgres'
DB_PASSWORD = 'your_password'
```

## Running the Project
### 1. Set Up the Database
Run the following command to create the database and tables:
```sh
python main.py
```

This will:
1. Drop and recreate the `TaxiRides` database.
2. Create necessary tables using `createTable_sqlStatement.py`.
3. Load taxi ride data from `uber_data.csv`.
4. Transform the data.
5. Insert the processed data into the database.

### 2. Running Queries
After the data is inserted, you can run sample queries using:
```sql
SELECT * FROM Trip LIMIT 10;
```
Refer to `sampleQueries.sql` for more examples.

## Logging
Logs are generated to track errors and processes. Check the console output for any issues.

## Troubleshooting
- Ensure PostgreSQL is running and accessible.
- Verify database credentials in `helper.py` and `insert_data.py`.
- Check for missing dependencies and install them using:
```sh
pip install pandas psycopg2 sqlalchemy
```

