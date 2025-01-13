from fastapi import FastAPI, Query
from .calculate_capacity import calculate_daily_capacity
from typing import Dict, List, Union
import json

app = FastAPI(title="Flight Capacity API")

@app.get("/capacity")
async def get_capacity(
    origin: str = Query(..., description="Origin airport ICAO code"),
    destination: str = Query(..., description="Destination airport ICAO code")
) -> Dict[str, Union[Dict[str, str], List[Dict[str, Union[str, float, int]]], Dict[str, Union[float, int]]]]:
    """
    Get daily capacity totals for flights between two airports.
    
    Args:
        origin: Origin airport ICAO code
        destination: Destination airport ICAO code
        
    Returns:
        JSON with route information, daily totals, and summary statistics
    """
    # Get daily totals
    daily_totals = calculate_daily_capacity(origin, destination)
    
    if daily_totals.empty:
        # Handle case where no flights exist
        daily_records = []
        summary_stats = {
            "average_daily_volume": 0,
            "average_daily_payload": 0,
            "average_daily_flights": 0,
            "total_flights": 0,
            "days_with_flights": 0,
            "total_days": 0
        }
    else:
        # Convert to JSON-compatible format and handle NaN values
        daily_totals['date'] = daily_totals['date'].astype(str)
        daily_totals = daily_totals.fillna(0)  # Fill NaN values with 0
        daily_records = daily_totals.to_dict(orient='records')
        
        # Create summary statistics with NaN handling
        summary_stats = {
            "average_daily_volume": round(daily_totals['volume'].fillna(0).mean(), 2),
            "average_daily_payload": round(daily_totals['payload'].fillna(0).mean(), 2),
            "average_daily_flights": round(daily_totals['num_flights'].fillna(0).mean(), 1),
            "total_flights": int(daily_totals['num_flights'].fillna(0).sum()),
            "days_with_flights": int((daily_totals['num_flights'] > 0).sum()),
            "total_days": len(daily_totals)
        }
    
    # Create response with proper JSON formatting
    from fastapi.responses import JSONResponse
    return JSONResponse(content={
        "route": {
            "origin": origin,
            "destination": destination
        },
        "daily_totals": daily_records,
        "summary": summary_stats
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
