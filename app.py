import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Function to authenticate and connect to Google Sheets using Streamlit Secrets
def authenticate_google_sheets():
    # Load credentials from Streamlit Secrets
    secrets = st.secrets["google_sheets"]
    
    # Prepare the credentials for authentication
    credentials = {
        "type": "service_account",
        "project_id": secrets["project_id"],
        "private_key_id": secrets["private_key_id"],
        "private_key": secrets["private_key"].replace("\\n", "\n"),
        "client_email": secrets["client_email"],
        "client_id": secrets["client_id"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": secrets["client_x509_cert_url"]
    }
    
    # Convert the credentials to a format suitable for gspread
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, 
                                                             ["https://www.googleapis.com/auth/spreadsheets", 
                                                              "https://www.googleapis.com/auth/drive.file"])
    client = gspread.authorize(creds)
    return client

# Function to update the Google Sheet with form data
def update_google_sheet(data):
    # Use Streamlit Secrets to get the spreadsheet ID
    spreadsheet_id = st.secrets["google_sheets"]["spreadsheet_id"]
    
    # Open the Google Sheet by ID
    sheet = client.open_by_key(spreadsheet_id).sheet1  # Assuming sheet1 is the target sheet
    sheet.append_row(data)  # Add the form data as a new row

# Streamlit form for input
st.title('Game Data Submission Form')
with st.form(key='game_form'):
    # Form fields (similar to your previous code)
    name = st.text_input("Enter the name of the game")
    country = st.text_input("Enter the country of origin")
    date = st.date_input("Enter the release date")
    description = st.text_area("Enter a brief description of the game")
    
    platforms1 = st.text_input("Enter Platform 1")
    platforms2 = st.text_input("Enter Platform 2")
    platforms3 = st.text_input("Enter Platform 3")
    platforms4 = st.text_input("Enter Platform 4")
    
    genres = st.text_input("Enter the genre(s) of the game")
    studio = st.text_input("Enter the studio")
    publisher = st.text_input("Enter the publisher")
    programmer = st.text_input("Enter the programmer")

    source1 = st.text_input("Enter Source 1")
    source2 = st.text_input("Enter Source 2")

    lat = st.number_input("Enter Latitude", format="%.6f")
    long = st.number_input("Enter Longitude", format="%.6f")
    
    category = st.text_input("Enter category of the game")
    address = st.text_input("Enter address")
    sgg = st.text_input("Enter SGG (if applicable)")
    duration = st.text_input("Enter the duration of the interview")
    interviewer = st.text_input("Enter the interviewer's name")
    interview_type = st.selectbox("Type of interview", ["Written", "Oral", "Recorded"])

    submit_button = st.form_submit_button("Submit")

    if submit_button:
        if name and country and date and description:
            # Authenticate and update the Google Sheet
            client = authenticate_google_sheets()
            form_data = [
                name, country, date.strftime('%Y-%m-%d'), description,
                platforms1, platforms2, platforms3, platforms4,
                genres, studio, publisher, programmer,
                source1, source2, lat, long,
                category, address, sgg, duration,
                interviewer, interview_type
            ]
            update_google_sheet(form_data)
            st.success("Data successfully submitted!")
        else:
            st.error("Please fill in all required fields.")
