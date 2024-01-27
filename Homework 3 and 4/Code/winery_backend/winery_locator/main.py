import smtplib
from email.mime.text import MIMEText

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fuzzywuzzy import fuzz
from pydantic import BaseModel
from transliterate import translit


origins = [
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

# MicroService for map
@app.get("/coordinates_info")
async def get_all_coordinates():
    df = pd.read_csv("filtered.csv")
    # Rename the first column to 'ID'
    df.rename(columns={df.columns[0]: 'ID'}, inplace=True)
    # Selecting specific columns
    selected_columns = ['ID', 'Latitude', 'Longitude', 'Name']
    df_copy = df[selected_columns].copy()
    # Convert to JSON
    data = df_copy.to_json(orient="records")
    return {
        "message": "Connected to backend",
        "data": data
    }