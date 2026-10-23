
# Voice-Enabled Intelligent Airport Operations and Passenger Management System

## Overview
A Python-based airport management dashboard connected to a MySQL database, designed to display airport records and assist passengers through voice and text queries.

## Technologies
- Python
- MySQL
- Streamlit
- Pandas
- SpeechRecognition
- Text-to-speech using pyttsx3

## Features
- Airport database connectivity
- Flight, passenger, aircraft, booking and payment record viewing
- Interactive dashboard
- Voice and text-based passenger enquiries

## Setup
1. Install Python and MySQL.
2. Create and populate the AirportDB database.
3. Install dependencies:

   `python -m pip install -r requirements.txt`

4. Configure the MySQL connection securely.
5. Run the dashboard:

   `python -m streamlit run app.py`

## Security
Do not commit passwords, private passenger information or production database credentials.
