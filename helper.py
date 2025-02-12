import psycopg2
import logging
from createTable_sqlStatement import create_table_sql  # Updated import statement

def init_logger():
    logging.basicConfig(level=logging.INFO)
    logging.info('Start of program and logger')

def postgres_connection(database=None):
    conn = None
    try:
        logging.info('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database=database,
            user='postgres',
            password='yash9494'
        )
        logging.info('Connection successful')
        return conn
    except Exception as error:
        logging.error(f"Error connecting to the database: {error}")
        return None

def drop_database(database_name):
    conn = None
    try:
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            user='postgres',
            password='yash9494'
        )
        conn.autocommit = True  # Enable autocommit mode for dropping a database
        cur = conn.cursor()
        logging.info(f'Dropping database "{database_name}" if it exists...')
        cur.execute(f"DROP DATABASE IF EXISTS {database_name};")
        logging.info(f'Database "{database_name}" dropped successfully (if it existed).')
    except Exception as error:
        logging.error(f"Error dropping database: {error}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def create_database(database_name):
    drop_database(database_name)  # Drop the old database if it exists

    conn = None
    try:
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            user='postgres',
            password='yash9494'
        )
        conn.autocommit = True  # Enable autocommit mode for creating a database
        cur = conn.cursor()
        logging.info(f'Creating database "{database_name}"...')
        cur.execute(f"CREATE DATABASE {database_name};")
        logging.info(f'Database "{database_name}" created successfully.')
    except Exception as error:
        logging.error(f"Error creating database: {error}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def create_tables(conn):
    try:
        cur = conn.cursor()
        logging.info('Creating tables in the database...')
        
        # Execute the create table SQL statements
        cur.execute(create_table_sql)  # Updated to match the SQL string variable name
        logging.info('Executed create table query.')
        
        # Commit the changes
        conn.commit()
        logging.info('Tables created successfully.')
        
        # Close the cursor
        cur.close()
    except Exception as error:
        logging.error(f"Error creating tables: {error}")

def close_connection(conn):
    if conn is not None:
        conn.close()
        logging.info('Database connection closed.')
