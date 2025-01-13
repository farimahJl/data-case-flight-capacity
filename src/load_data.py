import pandas as pd
import json
from pathlib import Path

def load_airplane_details():
    """Load airplane details from JSONL file into a DataFrame."""
    # Read JSONL file line by line
    with open('data/airplane_details.jsonl', 'r') as f:
        data = [json.loads(line) for line in f]
    
    # Convert to DataFrame and fill missing volume values with 0
    df = pd.DataFrame(data)

    return df

def load_flight_events():
    """Load all flight events from CSV files into a single DataFrame."""
    # Get all CSV files in the flight_events directory
    flight_events_dir = Path('data/flight_events')
    csv_files = list(flight_events_dir.glob('*.csv'))
    
    # Read and combine all CSV files
    dfs = []
    for file in csv_files:
        # Read CSV with semicolon delimiter
        df = pd.read_csv(file, sep=';')
        # Convert time column to datetime
        df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
        dfs.append(df)
    
    # Concatenate all DataFrames
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Sort by datetime
    return combined_df.sort_values('datetime')

def main():
    # Load both datasets
    airplane_df = load_airplane_details()
    flights_df = load_flight_events()
    
    # Print basic information about the DataFrames
    print("\nAirplane Details DataFrame Info:")
    print(airplane_df.info())
    print("\nFirst few rows of Airplane Details:")
    print(airplane_df.head())
    
    print("\nFlight Events DataFrame Info:")
    print(flights_df.info())
    print("\nFirst few rows of Flight Events:")
    print(flights_df.head())

if __name__ == "__main__":
    main()
