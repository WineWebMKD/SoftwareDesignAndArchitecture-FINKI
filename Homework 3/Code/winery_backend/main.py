import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from transliterate import translit, get_available_language_codes

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
    data = df_copy.to_json(orient="records")
    return {"message": "Connected to backend",
            "data": data}


@app.get("/get_data/{marker_id}")
async def get_data(marker_id: int):
    df = pd.read_csv("filtered.csv")
    df_copy = df.copy()
    df_copy.rename(columns={df_copy.columns[0]: 'ID'}, inplace=True)
    data = df_copy[df_copy['ID'] == marker_id].to_json(orient="records")
    return {"message": "Connected to backend",
            "data": data}


@app.get("/get_result/{encoded_city}")
async def get_result(encoded_city: str):
    print(encoded_city)
    print(get_available_language_codes())
    decoded_city = translit(encoded_city, 'mk')
    df = pd.read_csv("filtered.csv")
    df_copy = df.copy()
    df_copy.rename(columns={df_copy.columns[0]: 'ID'}, inplace=True)
    data = df_copy[df_copy["City"] == decoded_city].to_json(orient="records")
    return {"message": "Connected to backend",
            "data": data, "city": decoded_city}


@app.get("/get_occupation/{occupation}")
async def get_occupation(occupation: str):
    print(occupation)
    df = pd.read_csv("filtered.csv")
    df_copy = df.copy()
    df_copy.rename(columns={df_copy.columns[0]: 'ID'}, inplace=True)
    if occupation == 'vinarija':
        data = df_copy[df_copy["Activities"].str.contains('винотеки (винарници)', regex=False)].to_json(orient="records")
    else:
        data = df_copy[df_copy["Activities"].str.contains("винарски визби", regex=False)].to_json(orient="records")
    return {"message": "Connected to backend",
            "data": data, "occupation": occupation}


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
