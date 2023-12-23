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


@app.get("/get_all_coordinates")
async def get_all_coordinates():
    df = pd.read_csv("filtered.csv")
    df_copy = df.copy()
    df_copy.drop(['City', 'Activities', 'Facebook', 'Instagram', 'Numbers', 'WebPage', 'Working Hours'], axis=1, inplace=True)
    df_copy.rename(columns={df.columns[0]: 'ID'}, inplace=True)

    # print(df_copy)
    # column = df_copy[0]
    data = df_copy.to_json(orient="records")
    return {"message": "Connected to backend",
            "data": data}


@app.get("/get_data/{marker_id}")
async def get_data(marker_id: int):
    df = pd.read_csv("filtered.csv")
    df_copy = df.copy()
    df_copy.rename(columns={df.columns[0]: 'ID'}, inplace=True)
    data = df_copy[df_copy['ID'] == marker_id].to_json(orient="records")
    return {"message": "Connected to backend",
            "data": data}


@app.get("/get_data/{selectedOption}")
async def get_data(selected_option: str):
    df = pd.read_csv("filtered.csv")
    df_copy = df.copy()
    data = df_copy[df_copy['City'] == selected_option].to_json(orient="records")
    return {"message": "Connected to backend",
            "data": data}


@app.get("/get_all_cities")
async def get_all_coordinates():
    df = pd.read_csv("filtered.csv")
    unique_cities = df['City'].unique()
    df_copy = pd.DataFrame(unique_cities, columns=['City'])
    data = df_copy.to_json(orient="records")
    return {"message": "Connected to backend",
            "data": data}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
