import pandas as pd
import sys
import os

# Define file names
input_file = "daily_tmin_tmax.csv"
output_file = "last_frost.csv"

# Get the script's current directory as base path
base_path = os.path.dirname(os.path.abspath(__file__))

# Paths for input and output relative to current directory
input_path = os.path.join(base_path, input_file)
output_path = os.path.join(base_path, output_file)

# Try loading the daily averages data
daily_avg = None
try:
    # Load with low_memory=False to avoid potential DtypeWarning
    daily_avg = pd.read_csv(input_path, low_memory=False)
    print(f"Successfully loaded daily averages from {input_path}, rows: {len(daily_avg)}")
except FileNotFoundError:
    print(f"File not found: {input_path}. Please run station_consolidation.py first.")
    sys.exit(1)
except Exception as e:
    print(f"Error loading {input_path}: {str(e)}")
    sys.exit(1)

# Process frost dates
daily_avg['DATE'] = pd.to_datetime(daily_avg['DATE'])
daily_avg['year'] = daily_avg['DATE'].dt.year
daily_avg['month'] = daily_avg['DATE'].dt.month
daily_avg['day'] = daily_avg['DATE'].dt.day

# Filter for March 1 to May 31 (frost season)
frost_season = daily_avg[
    (daily_avg['month'] >= 3) & 
    (daily_avg['month'] < 6)
]
print(f"Frost season filtered, rows: {len(frost_season)}")

# Find frost days based on TMIN <= 32°F
frost_days = frost_season[frost_season['TMIN'] <= 32]
print(f"Frost days found, rows: {len(frost_days)}")

# Get the last frost date per year
if not frost_days.empty:
    last_frost = frost_days.groupby('year')[['DATE']].max().reset_index()
    last_frost.columns = ['year', 'last_frost_date']
    print(f"Last frost dates calculated, rows: {len(last_frost)}")
else:
    print("No frost days found (TMIN <= 32°F) in March-May period.")
    last_frost = pd.DataFrame(columns=['year', 'last_frost_date'])

# Save to CSV
last_frost.to_csv(output_path, index=False)
print(f"Saved last frost dates to {output_path}")
print(last_frost.head())