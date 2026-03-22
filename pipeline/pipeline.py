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

