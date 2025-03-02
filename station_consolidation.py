import pandas as pd
import sys
import os

# Define file names
input_file = "madison_1990_2025_source.csv"
output_file = "station_consolidation.csv"

# Get the script's current directory as base path
base_path = os.path.dirname(os.path.abspath(__file__))

# Paths for input and output
input_path = os.path.join(base_path, input_file)
output_path = os.path.join(base_path, output_file)

# Alternative paths for fallback (laptop and desktop)
laptop_path = r"C:\Users\ejnic\Documents\BONWRAnalysis"
desktop_path = r"C:\Users\ejnic.DESKTOP-L48NN8O\OneDrive - Indiana University\Documents\BONWRAnalysis"

# Try loading weather data
weather = None
for file_path in (input_path, os.path.join(laptop_path, input_file), os.path.join(desktop_path, input_file)):
    try:
        weather = pd.read_csv(file_path, low_memory=False)
        print(f"Successfully loaded weather data from {file_path}, rows: {len(weather)}")
        break
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error loading {file_path}: {str(e)}")

# Stop if all fail
if weather is None:
    print("Failed to load weather data from all paths. Exiting.")
    sys.exit(1)

# Consolidate TMIN, TMAX, PRCP, and SNOW medians by date
weather['DATE'] = pd.to_datetime(weather['DATE'])
daily_avg = weather.groupby('DATE')[['TMIN', 'TMAX', 'PRCP', 'SNOW']].median().reset_index()

# Save to CSV
daily_avg.to_csv(output_path, index=False)
print(f"Saved daily medians to {output_path}, rows: {len(daily_avg)}")
print(daily_avg.head())