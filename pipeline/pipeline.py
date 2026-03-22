import sys
import pandas as pd

print("Arguments", sys.argv) # parameterise pipeline with month

month = int(sys.argv[1])

df = pd.DataFrame({"day": [1,2], "num_passengers": [3,4]})
df["month"] = month

print(df.head())


df.to_parquet(f"output_{month}.parquet")

# parameters
print(f"Running pipeline for month={month}")

# create a docker image: docker build -t test:pandas .
# run the docker image: docker run -it --rm test:pandas 1

"""
docker run -it --rm \
  -e POSTGRES_USER="root" \ 
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \ # persist data in a docker volume called ny_taxi_postgres_data
  -p 5432:5432 \ # expose postgres port via port mapping, so we can connect to it from our local machine port_host_machine:port_docker_container
  postgres:18
"""

# connect to postgres from local machine using psql client:
