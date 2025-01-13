import pandas as pd
import matplotlib.pyplot as plt


def create_plot(date="2022-10-06"):
    # Create a DataFrame
    df = pd.read_csv("data/capacity.csv")

    # Convert datetime to pandas datetime format
    df['datetime'] = pd.to_datetime(df['datetime'])

    # Filter data for the specific day (e.g., 2025-01-12)
    filtered_df = df[df['datetime'].dt.date == pd.to_datetime(date).date()]

    # Aggregate by origin and destination airports
    capacity_by_route = filtered_df.groupby(['origin_icao', 'destination_icao']).agg(
        total_volume=('volume', 'sum'),
        total_payload=('payload', 'sum')
    ).reset_index()

    # Aggregate by destination airports for top 10 analysis
    top_destinations = filtered_df.groupby('destination_icao').agg(
        total_volume=('volume', 'sum')
    ).reset_index().sort_values(by='total_volume', ascending=False).head(10)

    # Display the reports
    print("Capacity by Route:")
    print(capacity_by_route)

    print("\nTop 10 Destinations by Volume:")
    print(top_destinations)

    # Save the reports to CSV
    capacity_by_route.to_csv('capacity_by_route.csv', index=False)
    top_destinations.to_csv('top_10_destinations.csv', index=False)

    print("Reports saved as 'capacity_by_route.csv' and 'top_10_destinations.csv'")


    # Aggregate by origin airport to calculate total payload capacity
    payload_by_origin = filtered_df.groupby('origin_icao').agg(
        total_payload=('payload', 'sum')
    ).reset_index().sort_values(by='total_payload', ascending=False)

    # Display the report
    print("Total Payload Capacity by Origin Airport:")
    print(payload_by_origin)

    # Save the report to CSV
    payload_by_origin.to_csv('payload_by_origin_airport.csv', index=False)
    print("Report saved as 'payload_by_origin_airport.csv'")

    # Get the top 20 origin airports by total payload capacity
    top_20_payload_by_origin = payload_by_origin.head(20)

    # Visualization: Bar Chart for Top 20
    plt.figure(figsize=(12, 8))
    plt.bar(top_20_payload_by_origin['origin_icao'], top_20_payload_by_origin['total_payload'], color='orange')

    # Add labels and title
    plt.title(f'Top 20 Origin Airports by Total Payload Capacity ({date})', fontsize=14)
    plt.xlabel('Origin Airport (ICAO)', fontsize=12)
    plt.ylabel('Total Payload (kg)', fontsize=12)
    plt.xticks(fontsize=10, rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Show the plot
    plt.tight_layout()
    plt.show()




    # # Bar chart for total payload by route
    # plt.figure(figsize=(10, 6))
    # routes = capacity_by_route.apply(lambda row: f"{row['origin_icao']} → {row['destination_icao']}", axis=1)
    # plt.bar(routes, capacity_by_route['total_payload'], color='skyblue')

    # # Add labels and title
    # plt.title('Total Payload Capacity by Route (2025-01-12)', fontsize=14)
    # plt.xlabel('Route', fontsize=12)
    # plt.ylabel('Total Payload (kg)', fontsize=12)
    # plt.xticks(rotation=45, fontsize=10)
    # plt.grid(axis='y', linestyle='--', alpha=0.7)

    # # Show the plot
    # plt.tight_layout()
    # plt.show()


create_plot(date="2022-10-05")