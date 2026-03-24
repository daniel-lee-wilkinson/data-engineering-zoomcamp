import pandas as pd
from sqlalchemy import create_engine
# docker compose up -d
# docker ps


# --- connection ---
engine = create_engine("postgresql://root:root@localhost:5432/ny_taxi")

# --- load parquet and push to postgres ---
pq_data = pd.read_parquet("/workspaces/data-engineering-zoomcamp/green_tripdata_2025-11.parquet")
pq_data.to_sql("green_taxi_trips", con=engine, if_exists="replace", index=False)
print("green_taxi_trips loaded")

# --- load csv and push to postgres ---
zones = pd.read_csv("/workspaces/data-engineering-zoomcamp/taxi_zone_lookup.csv")
zones.to_sql("taxi_zones", con=engine, if_exists="replace", index=False)
print("taxi_zones loaded")



# filter for trips with trips of lpep_pickup_datetime between 2025-11-01 and 2025-12-01 excluding 2025-12-01 how many trips had a trip_distance less htan or equal to 1 mile?
filtered_data = pq_data[
    (pq_data["lpep_pickup_datetime"] >= "2025-11-01") &
    (pq_data["lpep_pickup_datetime"] < "2025-12-01") &
    (pq_data["trip_distance"] <= 1)
]
num_trips = len(filtered_data)
print(f"Number of trips with trip_distance <= 1 mile in November 2025:{num_trips}")
# ANS = 8007

# Question 4: which was the pickup day with the longest trip distance where trip_distance is less than 100 miles, using pickup time for calculations
pq_data["pickup_day"] = pq_data["lpep_pickup_datetime"].dt.date
filtered_data = pq_data[pq_data["trip_distance"] < 100]
longest_trip = filtered_data.loc[filtered_data["trip_distance"].idxmax()]
pickup_day_longest_trip = longest_trip["pickup_day"]
print(f"Pickup day with the longest trip distance (trip_distance < 100 miles): {pickup_day_longest_trip}") 
# ANS = 2025-11-14


# Question 5: biggest pickup zone: which pickup zone had hte largest total_amount on 18th november 2025?
pq_data["pickup_date"] = pq_data["lpep_pickup_datetime"].dt.date
filtered_data = pq_data[pq_data["pickup_date"] == pd.to_datetime("2025-11-18").date()]
pickup_zone_totals = filtered_data.groupby("PULocationID")["total_amount"].sum()
biggest_pickup_zone = pickup_zone_totals.idxmax()
# print the PULocationID of the biggest pickup zone
print(f"Biggest pickup zone on 18th November 2025 (PULocationID): {biggest_pickup_zone}")
# --> 74


# cross reference the biggest pickup zone with the taxi zone lookup file to get the name of the zone
taxi_zone_lookup = pd.read_csv("/workspaces/data-engineering-zoomcamp/taxi_zone_lookup.csv")
biggest_pickup_zone_name = taxi_zone_lookup.loc[taxi_zone_lookup["LocationID"] == biggest_pickup_zone, "Zone"].values[0]
print(f"Biggest pickup zone on 18th November 2025: {biggest_pickup_zone_name}")
# ANS = East Harlem North


# QUESTION 6: largest trip: for the passengers pickd up in East Harlem North in November, which drop off zone had the largest tip?
east_harlem_north_id = taxi_zone_lookup.loc[taxi_zone_lookup["Zone"] == "East Harlem North", "LocationID"].values[0]
filtered_data = pq_data[pq_data["PULocationID"] == east_harlem_north_id]
largest_tip_trip = filtered_data.loc[filtered_data["tip_amount"].idxmax()]
largest_tip_dropoff_zone_id = largest_tip_trip["DOLocationID"]
largest_tip_dropoff_zone_name = taxi_zone_lookup.loc[taxi_zone_lookup["LocationID"] == largest_tip_dropoff_zone_id, "Zone"].values[0]
print(f"Drop off zone with the largest tip for passengers picked up in East Harlem North in November 2025: {largest_tip_dropoff_zone_name}")
# ANS = Yorkville West

