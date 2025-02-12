# createTable  = """
# -- Create the PassengerCount table
# CREATE TABLE PassengerCount (
#     Passenger_count_id SERIAL PRIMARY KEY,
#     Passenger_count INT NOT NULL
# );

# -- Create the TripDistance table
# CREATE TABLE TripDistance (
#     Trip_distance_id SERIAL PRIMARY KEY,
#     Trip_distance DECIMAL(10, 2) NOT NULL
# );

# -- Create the RateCode table
# CREATE TABLE RateCode (
#     RateCodeID INT PRIMARY KEY,
#     Rate_code_description VARCHAR(255) NOT NULL
# );

# -- Create the PaymentType table
# CREATE TABLE PaymentType (
#     Payment_type_id INT PRIMARY KEY,
#     Payment_type_description VARCHAR(255) NOT NULL
# );

# -- Create the PickupLocation table
# CREATE TABLE PickupLocation (
#     PULocationID INT PRIMARY KEY,
#     Pickup_location_description VARCHAR(255) NOT NULL
# );

# -- Create the DropoffLocation table
# CREATE TABLE DropoffLocation (
#     DOLocationID INT PRIMARY KEY,
#     Dropoff_location_description VARCHAR(255) NOT NULL
# );

# -- Create the DateTime table
# CREATE TABLE DateTime (
#     DateTime_id SERIAL PRIMARY KEY,
#     lpep_pickup_datetime TIMESTAMP NOT NULL,
#     lpep_dropoff_datetime TIMESTAMP NOT NULL
# );

# -- Create the Trip table
# CREATE TABLE Trip (
#     trip_id SERIAL PRIMARY KEY,
#     VendorID INT NOT NULL,
#     Store_and_fwd_flag CHAR(1) NOT NULL,
#     Fare_amount DECIMAL(10, 2) NOT NULL,
#     Extra DECIMAL(10, 2) NOT NULL,
#     MTA_tax DECIMAL(10, 2) NOT NULL,
#     Improvement_surcharge DECIMAL(10, 2) NOT NULL,
#     Tip_amount DECIMAL(10, 2) NOT NULL,
#     Tolls_amount DECIMAL(10, 2) NOT NULL,
#     Total_amount DECIMAL(10, 2) NOT NULL,
#     Trip_type INT NOT NULL,
#     Passenger_count_id INT REFERENCES PassengerCount(Passenger_count_id),
#     Trip_distance_id INT REFERENCES TripDistance(Trip_distance_id),
#     RateCodeID INT REFERENCES RateCode(RateCodeID),
#     Payment_type_id INT REFERENCES PaymentType(Payment_type_id),
#     PULocationID INT REFERENCES PickupLocation(PULocationID),
#     DOLocationID INT REFERENCES DropoffLocation(DOLocationID),
#     DateTime_id INT REFERENCES DateTime(DateTime_id)
# );"""

create_table_sql = """
-- Create the DateTime table to match datetime_dim
CREATE TABLE IF NOT EXISTS DateTime (
    DateTime_id SERIAL PRIMARY KEY,
    tpep_pickup_datetime TIMESTAMP NOT NULL,
    pick_hour INT NOT NULL,
    pick_day INT NOT NULL,
    pick_month INT NOT NULL,
    pick_year INT NOT NULL,
    pick_weekday INT NOT NULL,
    tpep_dropoff_datetime TIMESTAMP NOT NULL,
    drop_hour INT NOT NULL,
    drop_day INT NOT NULL,
    drop_month INT NOT NULL,
    drop_year INT NOT NULL,
    drop_weekday INT NOT NULL
);

-- Create the PassengerCount table to match passenger_count_dim
CREATE TABLE IF NOT EXISTS PassengerCount (
    Passenger_count_id SERIAL PRIMARY KEY,
    Passenger_count INT NOT NULL
);

-- Create the TripDistance table to match trip_distance_dim
CREATE TABLE IF NOT EXISTS TripDistance (
    Trip_distance_id SERIAL PRIMARY KEY,
    Trip_distance DECIMAL(10, 2) NOT NULL
);

-- Create the RateCode table to match rate_code_dim
CREATE TABLE IF NOT EXISTS RateCode (
    Rate_code_id SERIAL PRIMARY KEY,
    RatecodeID INT NOT NULL,
    rate_code_name VARCHAR(255) NOT NULL
);

-- Create the PickupLocation table to match pickup_location_dim
CREATE TABLE IF NOT EXISTS PickupLocation (
    pickup_location_id SERIAL PRIMARY KEY,
    pickup_latitude DECIMAL(9, 6) NOT NULL,
    pickup_longitude DECIMAL(9, 6) NOT NULL
);

-- Create the DropoffLocation table to match dropoff_location_dim
CREATE TABLE IF NOT EXISTS DropoffLocation (
    dropoff_location_id SERIAL PRIMARY KEY,
    dropoff_latitude DECIMAL(9, 6) NOT NULL,
    dropoff_longitude DECIMAL(9, 6) NOT NULL
);

-- Create the PaymentType table to match payment_type_dim
CREATE TABLE IF NOT EXISTS PaymentType (
    payment_type_id SERIAL PRIMARY KEY,
    payment_type INT NOT NULL,
    payment_type_name VARCHAR(255) NOT NULL
);

-- Create the Trip fact table to match fact_table
CREATE TABLE IF NOT EXISTS Trip (
    trip_id SERIAL PRIMARY KEY,
    VendorID INT NOT NULL,
    datetime_id INT REFERENCES DateTime(DateTime_id),
    passenger_count_id INT REFERENCES PassengerCount(Passenger_count_id),
    trip_distance_id INT REFERENCES TripDistance(Trip_distance_id),
    rate_code_id INT REFERENCES RateCode(rate_code_id),
    store_and_fwd_flag CHAR(1) NOT NULL,
    pickup_location_id INT REFERENCES PickupLocation(pickup_location_id),
    dropoff_location_id INT REFERENCES DropoffLocation(dropoff_location_id),
    payment_type_id INT REFERENCES PaymentType(payment_type_id),
    fare_amount DECIMAL(10, 2) NOT NULL,
    extra DECIMAL(10, 2) NOT NULL,
    mta_tax DECIMAL(10, 2) NOT NULL,
    tip_amount DECIMAL(10, 2) NOT NULL,
    tolls_amount DECIMAL(10, 2) NOT NULL,
    improvement_surcharge DECIMAL(10, 2) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL
);
"""
