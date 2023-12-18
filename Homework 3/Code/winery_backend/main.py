from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/get_data")
async def get_data():
    df = pd.read_csv("filtered.csv")
    data = df.to_json(orient="records")
    return {"message": "Connected to backend",
            "data": data}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
