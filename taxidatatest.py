import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# 1. LOAD DATA
# -------------------------------
file_path = "Taxi_Trips_-_2022_20260216.csv"  # make sure file is in same folder
df = pd.read_csv(file_path)

print("Dataset loaded successfully.")
print("Shape:", df.shape)
print("\nColumns:\n", df.columns)

# -------------------------------
# 2. IDENTIFY COLUMN NAMES
# -------------------------------
# Try to auto-detect relevant columns
distance_col = None
fare_col = None

for col in df.columns:
    col_lower = col.lower()
    if "mile" in col_lower or "distance" in col_lower:
        distance_col = col
    if "fare" in col_lower or "total" in col_lower:
        fare_col = col

print("\nDetected Columns:")
print("Distance column:", distance_col)
print("Fare column:", fare_col)

# If detection fails, manually set:
# distance_col = "Trip Miles"
# fare_col = "Fare"

# -------------------------------
# 3. CLEAN DATA
# -------------------------------
# Convert to numeric
df[distance_col] = pd.to_numeric(df[distance_col], errors='coerce')
df[fare_col] = pd.to_numeric(df[fare_col], errors='coerce')

# Drop missing values
df_clean = df.dropna(subset=[distance_col, fare_col])

print("\nAfter cleaning:", df_clean.shape)

# -------------------------------
# 4. CHECK INCONSISTENCIES
# -------------------------------

# Case 1: distance = 0 but fare > 0
zero_distance_with_fare = df_clean[
    (df_clean[distance_col] == 0) & (df_clean[fare_col] > 0)
]

# Case 2: fare = 0 but distance > 0
zero_fare_with_distance = df_clean[
    (df_clean[fare_col] == 0) & (df_clean[distance_col] > 0)
]

print("\n-------------------------------")
print("INCONSISTENCY CHECK")
print("-------------------------------")

print("\n1. distance = 0 but fare > 0 → count:", len(zero_distance_with_fare))
print(zero_distance_with_fare[[distance_col, fare_col]].head())

print("\n2. fare = 0 but distance > 0 → count:", len(zero_fare_with_distance))
print(zero_fare_with_distance[[distance_col, fare_col]].head())

# -------------------------------
# 5. OPTIONAL: SAVE THESE ROWS
# -------------------------------
zero_distance_with_fare.to_csv("zero_distance_with_fare.csv", index=False)
zero_fare_with_distance.to_csv("zero_fare_with_distance.csv", index=False)

# -------------------------------
# 6. SCATTER PLOT
# -------------------------------
plt.figure(figsize=(8, 6))

# Normal data
plt.scatter(
    df_clean[distance_col],
    df_clean[fare_col],
    alpha=0.3
)

# Highlight anomalies
plt.scatter(
    zero_distance_with_fare[distance_col],
    zero_distance_with_fare[fare_col],
    marker='x',
    label='0 distance, fare > 0'
)

plt.scatter(
    zero_fare_with_distance[distance_col],
    zero_fare_with_distance[fare_col],
    marker='o',
    label='distance > 0, fare = 0'
)

plt.xlabel("Distance (Miles)")
plt.ylabel("Fare")
plt.title("Distance vs Fare Scatter Plot")

plt.legend()
plt.grid(True)
plt.show()