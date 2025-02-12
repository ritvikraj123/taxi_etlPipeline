import pandas as pd
import logging

# Initialize the logger
logging.basicConfig(level=logging.INFO)

def transform_data(df):
    """
    Transforms the taxi rides data for insertion into database tables.
    """
    # Log the initial DataFrame shape and columns
    logging.info(f"Initial DataFrame shape: {df.shape}")
    logging.info(f"Initial DataFrame columns: {df.columns.tolist()}")

    # Normalize column names by stripping whitespace and converting to lowercase
    df.columns = df.columns.str.strip().str.lower()  # Normalize the column names
    logging.info(f"Normalized DataFrame columns: {df.columns.tolist()}")

    # Handle datetime transformations
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'], errors='coerce')
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'], errors='coerce')

    # Log any NaT values in datetime columns
    if df['tpep_pickup_datetime'].isnull().any():
        logging.warning("There are NaT values in 'tpep_pickup_datetime'")
    if df['tpep_dropoff_datetime'].isnull().any():
        logging.warning("There are NaT values in 'tpep_dropoff_datetime'")

    # Create datetime_dim
    datetime_dim = df[['tpep_pickup_datetime', 'tpep_dropoff_datetime']].drop_duplicates().reset_index(drop=True)
    datetime_dim['pick_hour'] = datetime_dim['tpep_pickup_datetime'].dt.hour
    datetime_dim['pick_day'] = datetime_dim['tpep_pickup_datetime'].dt.day
    datetime_dim['pick_month'] = datetime_dim['tpep_pickup_datetime'].dt.month
    datetime_dim['pick_year'] = datetime_dim['tpep_pickup_datetime'].dt.year
    datetime_dim['pick_weekday'] = datetime_dim['tpep_pickup_datetime'].dt.weekday
    datetime_dim['drop_hour'] = datetime_dim['tpep_dropoff_datetime'].dt.hour
    datetime_dim['drop_day'] = datetime_dim['tpep_dropoff_datetime'].dt.day
    datetime_dim['drop_month'] = datetime_dim['tpep_dropoff_datetime'].dt.month
    datetime_dim['drop_year'] = datetime_dim['tpep_dropoff_datetime'].dt.year
    datetime_dim['drop_weekday'] = datetime_dim['tpep_dropoff_datetime'].dt.weekday
    datetime_dim['datetime_id'] = datetime_dim.index

    # Log the shape of datetime_dim
    logging.info(f"datetime_dim shape: {datetime_dim.shape}")

    # Reorder columns
    datetime_dim = datetime_dim[['datetime_id', 'tpep_pickup_datetime', 'pick_hour', 'pick_day', 
                                  'pick_month', 'pick_year', 'pick_weekday', 'tpep_dropoff_datetime', 
                                  'drop_hour', 'drop_day', 'drop_month', 'drop_year', 'drop_weekday']]

    # Passenger count dimension
    passenger_count_dim = df[['passenger_count']].drop_duplicates().reset_index(drop=True)
    passenger_count_dim['passenger_count_id'] = passenger_count_dim.index

    # Log the shape of passenger_count_dim
    logging.info(f"passenger_count_dim shape: {passenger_count_dim.shape}")

    # Trip distance dimension
    trip_distance_dim = df[['trip_distance']].drop_duplicates().reset_index(drop=True)
    trip_distance_dim['trip_distance_id'] = trip_distance_dim.index

    # Log the shape of trip_distance_dim
    logging.info(f"trip_distance_dim shape: {trip_distance_dim.shape}")

    # Rate code mapping and dimension
    rate_code_type = {
        1: "Standard rate", 2: "JFK", 3: "Newark", 4: "Nassau or Westchester",
        5: "Negotiated fare", 6: "Group ride"
    }
    rate_code_dim = df[['ratecodeid']].drop_duplicates().reset_index(drop=True)  # Change RatecodeID to ratecodeid
    rate_code_dim['rate_code_id'] = rate_code_dim.index
    rate_code_dim['rate_code_name'] = rate_code_dim['ratecodeid'].map(rate_code_type)

    # Log the shape of rate_code_dim
    logging.info(f"rate_code_dim shape: {rate_code_dim.shape}")

    # Pickup and dropoff location dimensions
    required_pickup_columns = ['pickup_longitude', 'pickup_latitude']
    required_dropoff_columns = ['dropoff_longitude', 'dropoff_latitude']

    # Check for required pickup location columns
    if all(col in df.columns for col in required_pickup_columns):
        pickup_location_dim = df[required_pickup_columns].drop_duplicates().reset_index(drop=True)
        pickup_location_dim['pickup_location_id'] = pickup_location_dim.index
        logging.info(f"pickup_location_dim shape: {pickup_location_dim.shape}")
    else:
        missing_pickup = set(required_pickup_columns) - set(df.columns)
        logging.error(f"Missing pickup location columns: {missing_pickup}")
        pickup_location_dim = pd.DataFrame(columns=['pickup_location_id', 'pickup_longitude', 'pickup_latitude'])

    # Check for required dropoff location columns
    if all(col in df.columns for col in required_dropoff_columns):
        dropoff_location_dim = df[required_dropoff_columns].drop_duplicates().reset_index(drop=True)
        dropoff_location_dim['dropoff_location_id'] = dropoff_location_dim.index
        logging.info(f"dropoff_location_dim shape: {dropoff_location_dim.shape}")
    else:
        missing_dropoff = set(required_dropoff_columns) - set(df.columns)
        logging.error(f"Missing dropoff location columns: {missing_dropoff}")
        dropoff_location_dim = pd.DataFrame(columns=['dropoff_location_id', 'dropoff_longitude', 'dropoff_latitude'])

    # Payment type mapping and dimension
    payment_type_name = {
        1: "Credit card", 2: "Cash", 3: "No charge", 4: "Dispute", 5: "Unknown", 6: "Voided trip"
    }
    payment_type_dim = df[['payment_type']].drop_duplicates().reset_index(drop=True)
    payment_type_dim['payment_type_id'] = payment_type_dim.index
    payment_type_dim['payment_type_name'] = payment_type_dim['payment_type'].map(payment_type_name)

    # Log the shape of payment_type_dim
    logging.info(f"payment_type_dim shape: {payment_type_dim.shape}")

    # Fact table
    trip_table = df.merge(passenger_count_dim, on='passenger_count') \
                   .merge(trip_distance_dim, on='trip_distance') \
                   .merge(rate_code_dim, on='ratecodeid') \
                   .merge(pickup_location_dim, on=['pickup_longitude', 'pickup_latitude']) \
                   .merge(dropoff_location_dim, on=['dropoff_longitude', 'dropoff_latitude']) \
                   .merge(datetime_dim, on=['tpep_pickup_datetime', 'tpep_dropoff_datetime']) \
                   .merge(payment_type_dim, on='payment_type') \
                   [['vendorid', 'datetime_id', 'passenger_count_id', 'trip_distance_id', 
                     'rate_code_id', 'store_and_fwd_flag', 'pickup_location_id', 'dropoff_location_id',
                     'payment_type_id', 'fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount', 
                     'improvement_surcharge', 'total_amount']]

    # Log the shape of the fact table
    logging.info(f"trip_table shape: {trip_table.shape}")

    return {
        "datetime_dim": datetime_dim,
        "passenger_count_dim": passenger_count_dim,
        "trip_distance_dim": trip_distance_dim,
        "rate_code_dim": rate_code_dim,
        "pickup_location_dim": pickup_location_dim,
        "dropoff_location_dim": dropoff_location_dim,
        "payment_type_dim": payment_type_dim,
        "trip_table": trip_table
    }
