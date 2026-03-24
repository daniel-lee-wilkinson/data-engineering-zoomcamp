# Module 1: homework docker & sql

## QUESTION 1. Run docker with the python:3.13 image. Use an entrypoint bash to interact with the container. What's the version of pip in the image?

This homework covers the foundational infrastructure layer of a data engineering workflow. It demonstrates containerisation with Docker and Docker Compose to run PostgreSQL and pgAdmin as isolated services, data ingestion from parquet and CSV sources into a relational database, and analytical querying using both pandas and PostgreSQL SQL. The same analytical questions are answered in both tools deliberately, illustrating how pandas operations (filtering, groupby, idxmax) map directly to SQL equivalents (WHERE, GROUP BY, ORDER BY, JOIN). The homework concludes with Terraform, covering the provisioning of cloud infrastructure (a GCS bucket and BigQuery dataset) on GCP using infrastructure-as-code.

```python
docker run -it --entrypoint=bash python:3.13.11-slim
pip -V
```

-- > pip 25.3

## QUESTION 2. In the given docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?
ANS:\
hostname = db \
port = 5432


## Prepare the data:

1. green taxi trips data for November 2025: 

```console
wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet
```

2. dataset with zones

```console
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
```

# QUESTION 3: Counting short trips
**PANDAS:**
```python
import pandas as pd

filtered_data = pq_data[
    (pq_data["lpep_pickup_datetime"] >= "2025-11-01") &
    (pq_data["lpep_pickup_datetime"] < "2025-12-01") &
    (pq_data["trip_distance"] <= 1)
]
num_trips = len(filtered_data)
print(f"Number of trips with trip_distance <= 1 mile in November 2025:{num_trips}")
```
**POSTGRESQL:**
```sql
SELECT COUNT(trip_distance) 
FROM green_taxi_trips 
WHERE lpep_pickup_datetime >= '2025-11-01' 
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 1;
```

ANS = 8007


# QUESTION 4: which was the pickup day with the longest trip distance where trip_distance is less than 100 miles, using pickup time for calculations
**PANDAS:**
```python
pq_data["pickup_day"] = pq_data["lpep_pickup_datetime"].dt.date
filtered_data = pq_data[pq_data["trip_distance"] < 100]
longest_trip = filtered_data.loc[filtered_data["trip_distance"].idxmax()]
pickup_day_longest_trip = longest_trip["pickup_day"]
print(f"Pickup day with the longest trip distance (trip_distance < 100 miles): {pickup_day_longest_trip}") 
```
**POSTGRESQL:**
```sql
SELECT DATE(lpep_pickup_datetime) AS pickup_day, MAX(trip_distance) AS longest_distance
FROM green_taxi_trips
WHERE trip_distance < 100
GROUP BY pickup_day
ORDER BY longest_distance DESC
LIMIT 1;
```

ANS = 2025-11-14


# QUESTION 5: biggest pickup zone: which pickup zone had the largest total_amount on 18th november 2025?
**PANDAS:**
```python
pq_data["pickup_date"] = pq_data["lpep_pickup_datetime"].dt.date
filtered_data = pq_data[pq_data["pickup_date"] == pd.to_datetime("2025-11-18").date()]
pickup_zone_totals = filtered_data.groupby("PULocationID")["total_amount"].sum()
biggest_pickup_zone = pickup_zone_totals.idxmax()
# print the PULocationID of the biggest pickup zone
print(f"Biggest pickup zone on 18th November 2025 (PULocationID): {biggest_pickup_zone}")
```
--> 74


-->  cross reference the biggest pickup zone with the taxi zone lookup file to get the name of the zone:
```python
taxi_zone_lookup = pd.read_csv("/workspaces/data-engineering-zoomcamp/taxi_zone_lookup.csv")
biggest_pickup_zone_name = taxi_zone_lookup.loc[taxi_zone_lookup["LocationID"] == biggest_pickup_zone, "Zone"].values[0]
print(f"Biggest pickup zone on 18th November 2025: {biggest_pickup_zone_name}")
```
**POSTGRESQL:**
```sql
SELECT z."Zone", SUM(t.total_amount) AS total_amount
FROM green_taxi_trips t
JOIN taxi_zones z ON t."PULocationID" = z."LocationID"
WHERE DATE(t.lpep_pickup_datetime) = '2025-11-18'
GROUP BY z."Zone"
ORDER BY total_amount DESC
LIMIT 1;
```

--> ANS = East Harlem North

# QUESTION 6: largest trip - for the passengers picked up in East Harlem North in November, which drop off zone had the largest tip?
**PANDAS:**
```python
east_harlem_north_id = taxi_zone_lookup.loc[taxi_zone_lookup["Zone"] == "East Harlem North", "LocationID"].values[0]
filtered_data = pq_data[pq_data["PULocationID"] == east_harlem_north_id]
largest_tip_trip = filtered_data.loc[filtered_data["tip_amount"].idxmax()]
largest_tip_dropoff_zone_id = largest_tip_trip["DOLocationID"]
largest_tip_dropoff_zone_name = taxi_zone_lookup.loc[taxi_zone_lookup["LocationID"] == largest_tip_dropoff_zone_id, "Zone"].values[0]
print(f"Drop off zone with the largest tip for passengers picked up in East Harlem North in November 2025: {largest_tip_dropoff_zone_name}")
```
**POSTGRESQL:**
```sql
SELECT z_drop."Zone" AS dropoff_zone, MAX(t.tip_amount) AS largest_tip
FROM green_taxi_trips t
JOIN taxi_zones z_pick ON t."PULocationID" = z_pick."LocationID"
JOIN taxi_zones z_drop ON t."DOLocationID" = z_drop."LocationID"
WHERE z_pick."Zone" = 'East Harlem North'
  AND DATE(t.lpep_pickup_datetime) >= '2025-11-01'
  AND DATE(t.lpep_pickup_datetime) < '2025-12-01'
GROUP BY z_drop."Zone"
ORDER BY largest_tip DESC
LIMIT 1;
```

ANS = Yorkville West

# QUESTION 7: Terraform Workflow

```python
terraform init
terraform plan
terraform apply -auto-approve
```

steps: terraform init, terraform apply -auto-approve, terraform destroy