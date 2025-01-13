from load_data import load_flight_events, load_airplane_details
import pandas as pd

def process_airplane_details():
    """
    Process airplane details data:
    - Select specific columns
    - Rename code_icao to equipment
    """
    # Load airplane details
    df = load_airplane_details()

    df['volume'] = df['volume'].fillna(0)
    df['payload'] = df['payload'].fillna(0)

    # Select and rename columns
    columns_to_keep = ['code_icao', 'volume', 'payload']
    df_final = df[columns_to_keep].copy()
    df_final = df_final.rename(columns={'code_icao': 'equipment'})
    
    return df_final

def process_flight_events():
    """
    Process flight events data:
    - Remove records without origin/destination airports
    - Group by flight_id and keep first row
    - Select specific columns
    """
    # Load all flight events
    df = load_flight_events()
    
    # Remove records without origin or destination airports
    df_clean = df.dropna(subset=['origin_icao', 'destination_icao', 'equipment'])
    
    # Group by flight_id and keep first row
    df_grouped = df_clean.groupby('flight_id').first().reset_index()
    
    # Select specified columns
    columns_to_keep = ['flight_id', 'datetime', 'origin_icao', 'destination_icao', 'equipment']
    df_final = df_grouped[columns_to_keep]
    
    return df_final

def create_combined_dataset():
    """
    Create a combined dataset by joining flight events with airplane details.
    """
    # Get processed datasets
    flights_df = process_flight_events()
    airplanes_df = process_airplane_details()
    
    # Join datasets on equipment column
    combined_df = flights_df.merge(airplanes_df, on='equipment', how='left')

    df_clean = combined_df.dropna(subset=['volume', 'payload'])
    
    return df_clean

def save_to_csv(df, filename="data/capacity.csv"):
    """
    Save the combined dataset to a CSV file.
    
    Args:
        df: DataFrame to save
        filename: Name of the output file (default: capacity.csv)
    """
    df.to_csv(filename, index=False)
    print(f"\nDataset saved to {filename}")

def main():
    # Create combined dataset
    combined_df = create_combined_dataset()
    
    # Print information about the combined DataFrame
    print("\nCombined Dataset Info:")
    print(combined_df.info())
    print("\nFirst few rows of Combined Dataset:")
    print(combined_df.head())
    print(f"\nNumber of flights: {len(combined_df)}")
    print(f"\nNumber of flights with matching aircraft details: {combined_df['volume'].notna().sum()}")
    
    # Save to CSV
    save_to_csv(combined_df)

if __name__ == "__main__":
    main()
