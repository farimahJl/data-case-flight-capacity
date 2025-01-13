import pandas as pd

def calculate_daily_capacity(origin, destination):
    """
    Calculate total volume and payload per day for flights between specified airports.
    
    Args:
        origin: Origin airport ICAO code
        destination: Destination airport ICAO code
    
    Returns:
        DataFrame with daily totals for volume and payload
    """
    # Read the capacity data
    df = pd.read_csv('capacity.csv')
    
    # Convert datetime to proper datetime type
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    # Extract date from datetime
    df['date'] = df['datetime'].dt.date
    
    # Filter for specific origin and destination
    mask = (df['origin_icao'] == origin) & (df['destination_icao'] == destination)
    filtered_df = df[mask].copy()
    
    # Group by date and calculate totals and counts
    daily_totals = filtered_df.groupby('date').agg({
        'volume': 'sum',
        'payload': 'sum',
        'flight_id': 'count'  # Count number of flights
    }).reset_index()
    
    # Rename count column
    daily_totals = daily_totals.rename(columns={'flight_id': 'num_flights'})
    
    if not daily_totals.empty:
        daily_totals['num_flights'] = daily_totals['num_flights'].astype(int)
    
    return daily_totals
