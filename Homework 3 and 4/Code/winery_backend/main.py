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


# main
class FormData(BaseModel):
    name: str
    email: str
    subject: str
    message: str


# main
def send_email(form_data: FormData):
    sender_email = "temporarywinery@gmail.com"
    sender_password = "mswh howm pvqd xnxv"
    body = f"""
    Name: {form_data.name}
    Email: {form_data.email}
    Subject: {form_data.subject}
    Message: {form_data.message}
    """
    msg = MIMEText(body)
    msg['Subject'] = form_data.subject
    msg['From'] = form_data.name
    msg['To'] = sender_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender_email, sender_password)
        smtp_server.sendmail(sender_email, sender_email, msg.as_string())
    print("Message sent!")


# main
@app.post("/submit-form")
async def submit_form(form_data: FormData):
    try:
        print("Trying to send email")
        print(form_data)
        send_email(form_data)
        return {"message": "Email sent successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")


# MicroService for mapdetails
@app.get("/get_all_data")
async def get_all_coordinates():
    df = pd.read_csv("filtered.csv")
    df_copy = df.copy()
    df_copy.rename(columns={df.columns[0]: 'ID'}, inplace=True)
    data = df_copy.to_json(orient="records")
    return {"message": "Connected to backend",
            "data": data}


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


@app.get("/get_data/{marker_id}")
async def get_data(marker_id: int):
    df = pd.read_csv("filtered.csv")
    df_copy = df.copy()
    df_copy.rename(columns={df_copy.columns[0]: 'ID'}, inplace=True)
    data = df_copy[df_copy['ID'] == marker_id].to_json(orient="records")
    return {"message": "Connected to backend",
            "data": data}   


# main app
@app.get("/get_all_cities")
async def get_all_cities():
    df = pd.read_csv("filtered.csv")
    unique_cities = df['City'].unique()
    df_copy = pd.DataFrame(unique_cities, columns=['City'])
    data = df_copy.to_json(orient="records")
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
