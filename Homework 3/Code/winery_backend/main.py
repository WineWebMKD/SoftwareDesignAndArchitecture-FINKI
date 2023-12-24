import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fuzzywuzzy import fuzz
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


@app.get("/get_all_data")
async def get_all_coordinates():
    df = pd.read_csv("filtered.csv")
    df_copy = df.copy()
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
async def get_all_cities():
    df = pd.read_csv("filtered.csv")
    unique_cities = df['City'].unique()
    df_copy = pd.DataFrame(unique_cities, columns=['City'])
    data = df_copy.to_json(orient="records")
    return {"message": "Connected to backend",
            "data": data}


@app.get("/get_input_data/{encoded_input}")
async def get_input_data(encoded_input: str):
    # Decode the city
    decoded_input = translit(encoded_input, 'mk')
    # Read your CSV data
    df = pd.read_csv("filtered.csv")
    df_copy = df.copy()
    df_copy.rename(columns={df_copy.columns[0]: 'ID'}, inplace=True)
    filtered_data = df_copy[
        (df_copy['Name'].str.contains(decoded_input, case=False)) |
        (df_copy['Address'].str.contains(decoded_input, case=False)) |
        (df_copy.apply(lambda row: fuzz.partial_ratio(decoded_input, row['Name']), axis=1) > 70) |
        (df_copy.apply(lambda row: fuzz.partial_ratio(decoded_input, row['Address']), axis=1) > 70)
        ]
    data = filtered_data.to_json(orient="records")
    return {"message": "Connected to backend",
            "data": data}


@app.get("/get_filtered_data/{encoded_city}/{occupation}/{encoded_input}")
async def get_filtered_data(encoded_city: str, occupation: str, encoded_input: str):
    # Decode the city
    selected_city = translit(encoded_city, 'mk')
    # Read your CSV data
    df = pd.read_csv("filtered.csv")
    df_copy = df.copy()
    df_copy.rename(columns={df_copy.columns[0]: 'ID'}, inplace=True)
    # Filter data based on city, occupation and input
    if occupation == 'vizba':
        filtered_data = df_copy[(df_copy['City'] == selected_city)
                                & (df_copy["Activities"].str.contains('винотеки (винарници)', regex=False))]
    elif occupation == 'vinarija':
        filtered_data = df_copy[(df_copy['City'] == selected_city)
                                & (df_copy["Activities"].str.contains("винарски визби", regex=False))]
    else:
        # Handle other occupations or no occupation selected
        filtered_data = df_copy[df_copy['City'] == selected_city]

    if encoded_input != "No input":
        decoded_input = translit(encoded_input, 'mk')
        input_filter = filtered_data[
            (df_copy['Name'].str.contains(decoded_input, case=False)) |
            (df_copy['Address'].str.contains(decoded_input, case=False)) |
            (df_copy.apply(lambda row: fuzz.partial_ratio(decoded_input, row['Name']), axis=1) > 70) |
            (df_copy.apply(lambda row: fuzz.partial_ratio(decoded_input, row['Address']), axis=1) > 70)
            ]
        data = input_filter.to_json(orient="records")
    else:
        data = filtered_data.to_json(orient="records")
        
    return {"message": "Connected to backend",
            "data": data}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
