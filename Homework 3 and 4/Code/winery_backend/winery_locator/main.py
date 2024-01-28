import traceback

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from geopy.geocoders import Nominatim
from typing import List

origins = [
    "http://localhost:8000",
    "http://localhost:5173",  # Replace with your frontend URL
    "http://127.0.0.1:5173",  # Optionally, include localhost
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a geolocator using OpenStreetMap Nominatim
geolocator = Nominatim(user_agent="WineWeb")


# Function to get coordinates from address
def get_coordinates(row):
    try:
        # Check if latitude and longitude are empty
        if pd.isna(row['Latitude']) or pd.isna(row['Longitude']):
            location = geolocator.geocode(row['Address'])
            print("Getting location")
            if location:
                row['Latitude'] = location.latitude
                row['Longitude'] = location.longitude
                print(location.latitude, location.longitude)
    except Exception as e:
        print(f"Error geocoding address '{row['Address']}': {e}")
    return row


@app.get("/coordinates_info")
async def get_all_coordinates():
    try:
        df = pd.read_csv("filtered.csv")
        # Rename the first column to 'ID'
        df.rename(columns={df.columns[0]: 'ID'}, inplace=True)
        # Selecting specific columns
        selected_columns = ['ID', 'Latitude', 'Longitude', 'Name', 'Address']
        df_copy = df[selected_columns].copy()
        # Apply the function to each row
        df_copy = df_copy.apply(get_coordinates, axis=1)
        data = df_copy.to_json(orient="records")
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")




class WineryIds(BaseModel):
    winery_ids: List[int]


@app.post("/check_location")
async def check_location(ids: WineryIds):
    try:

        df = pd.read_csv("filtered.csv")
        df.rename(columns={df.columns[0]: 'ID'}, inplace=True)
        # Filter DataFrame based on the provided winery IDs
        selected_columns = ['ID', 'Latitude', 'Longitude', 'Name', 'Address']
        filtered_data = df[df['ID'].isin(ids.winery_ids)][selected_columns].copy()
        # Apply the function to get coordinates for each row
        filtered_data = filtered_data.apply(get_coordinates, axis=1)
        data = filtered_data.to_json(orient="records")
        return {"data": data}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

