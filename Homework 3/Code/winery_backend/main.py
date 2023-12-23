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


@app.get("/get_filtered_data/{encoded_city}/{occupation}")
async def get_filtered_data(encoded_city: str, occupation: str):
    try:
        # Decode the city
        selected_city = translit(encoded_city, 'mk')
        # Read your CSV data
        df = pd.read_csv("filtered.csv")
        df_copy = df.copy()
        df_copy.rename(columns={df_copy.columns[0]: 'ID'}, inplace=True)
        # Filter data based on both city and occupation
        if occupation == 'vizba':
            filtered_data = df_copy[(df_copy['City'] == selected_city)
                                    & (df_copy["Activities"].str.contains('винотеки (винарници)', regex=False))]
        elif occupation == 'vinarija':
            filtered_data = df_copy[(df_copy['City'] == selected_city)
                                    & (df_copy["Activities"].str.contains("винарски визби", regex=False))]
        else:
            # Handle other occupations or no occupation selected
            filtered_data = df_copy[df_copy['City'] == selected_city]

        # Convert the filtered data to JSON
        data = filtered_data.to_json(orient="records")

        return {"message": "Connected to backend", "data": data}
    except Exception as e:
        return {"message": f"Error: {str(e)}"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
