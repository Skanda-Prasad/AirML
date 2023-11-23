import streamlit as st
import pandas as pd
import os
import xgboost as xgb
import joblib
#from sklearn.externals import joblib
from pathlib import Path
from datetime import datetime
import numpy as np
from scipy import sparse
import streamlit as st
import pymysql
import warnings

connection = pymysql.connect(host="localhost", user="dbms", password="1234", database="dbms_project")
cursor = connection.cursor()
session_state = st.session_state
privileges = session_state.get('privileges')

# Create a Streamlit app
warnings.filterwarnings("ignore", category=UserWarning, module="numpy")

# Set the Streamlit option
st.set_option('deprecation.showfileUploaderEncoding', False)

# Create a dictionary for admin users
admin_data = {
    "skanda": "prasad",
    "shreyas": "sayerhs",
    "isham": "sinha"
}

# Create a folder for datasets if it doesn't exist
datasets_folder = Path("datasets")
datasets_folder.mkdir(exist_ok=True)

# Load the trained XGBoost model
model = xgb.XGBClassifier()
model.load_model('xgb.bin')

# Function to check if a user is an admin
def is_admin(username):
    return username in admin_data

# Function to check if a user exists
def user_exists(username):
    query = f"SELECT * FROM employee WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone() is not None or username in admin_data

# Function to check if a user entered the correct password
def check_password(username, password):
    query = f"SELECT * FROM employee WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    
    if is_admin(username):
        return admin_data.get(username) == password
    elif user:
        return user[1] == password  # Assuming password is in the second column
    else:
        return False

# Function to load the dataset files
def load_datasets():
    return [f.name for f in datasets_folder.iterdir() if f.is_file()]

# Function to download a dataset file
def download_dataset(file_name):
    src = datasets_folder / file_name
    dst = Path("/home/skanda/Downloads") / file_name
    dst.write_text(src.read_text())
    return dst

# Function to mark a dataset file as complete
def mark_as_complete(file_name):
    (datasets_folder / file_name).unlink()

# ... (existing code)

# Streamlit UI
def main():
    st.title("Aircraft Safety Testing")
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    # Page Navigation
    if st.session_state.authenticated:
        st.sidebar.title("Navigation")
        pages = ["Test Your Aeroplane", "Upload Dataset", "Log Out"]
        if is_admin(st.session_state.username):
            pages.insert(1, "Manage Datasets")
        choice = st.sidebar.radio("Go to", pages)

        if choice == "Log Out":
            # Clear user or admin query parameters to simulate logout
            st.experimental_set_query_params(user=None, admin=None)
            st.session_state.authenticated = False
            st.success("Logged out successfully!")
            st.stop()  # Stop the current execution to redirect to the login page

        # ... (existing code)

        elif choice == "Test Your Aeroplane":
            st.header("Test Your Aeroplane")
            
            # Form for input values
            time_in_cycles = st.number_input("Time in Cycles", min_value=0, step=1)
            fan_inlet_temp = st.number_input("Fan Inlet Temperature", min_value=0)
            compressor_inlet_temp = st.number_input("Compressor Inlet Temperature", min_value=0)
            hp_turbine_inlet_temp = st.number_input("HP Turbine Inlet Temperature", min_value=0)
            compressor_inlet_pressure = st.number_input("Compressor Inlet Pressure", min_value=0)
            fan_speed = st.number_input("Fan Speed", min_value=0)
            core_speed = st.number_input("Core Speed", min_value=0)
            compressor_outlet_pressure = st.number_input("Compressor Outlet Pressure", min_value=0)
            fuel_air_ratio = st.number_input("Fuel-Air Ratio", min_value=0)
            fan_speed_ratio = st.number_input("Fan Speed Ratio", min_value=0)
            bypass_ratio = st.number_input("Bypass Ratio", min_value=0)
            hot_bleed = st.number_input("Hot Bleed", min_value=0)
            fuel_flow = st.number_input("Fuel Flow", min_value=0)
            engine_air_flow = st.number_input("Engine Air Flow", min_value=0)
            
            if st.button("Test"):
                # Collect input values into a list
                input_data = [[time_in_cycles, fan_inlet_temp, compressor_inlet_temp, hp_turbine_inlet_temp,
                               compressor_inlet_pressure, fan_speed, core_speed, compressor_outlet_pressure,
                               fuel_air_ratio, fan_speed_ratio, bypass_ratio, hot_bleed, fuel_flow, engine_air_flow]]

                try:
                    # Model testing
                    prediction = model.predict(input_data)
                    if prediction[0] == 0:
                        st.warning("Aircraft Not Safe!")
                    elif prediction[0] == 1:
                        st.success("Aircraft Safe!")
                except Exception as e:
                    # Suppress the specific error
                    if "cannot access local variable 'input_data'" not in str(e):
                        st.error(f"Error predicting with the XGBoost model: {e}")

        elif choice == "Upload Dataset":
            st.header("Upload Dataset")
            st.text("Don't Use Aircrafts with Turbofan Engine? Add Data logs of your aircraft and we will build a custom model for you")
            uploaded_file = st.file_uploader("Choose a file", type="csv")

            if uploaded_file is not None:
                file_path = datasets_folder / uploaded_file.name
                file_path.write_text(uploaded_file.getvalue().decode())
                st.success("File Uploaded Successfully!")

        elif choice == "Manage Datasets" and is_admin(st.session_state.username):
            st.header("Manage Datasets")
            files = load_datasets()
            selected_file = st.selectbox("Select a file", files, index=0)

            if st.button("Download"):
                download_path = download_dataset(selected_file)
                st.success(f"Download Successful! File saved at {download_path}")

            if st.button("Mark as Complete"):
                mark_as_complete(selected_file)
                st.success("Dataset marked as complete!")

    else:  # User not authenticated, show login/sign-up forms
        st.header("Login/Sign Up")

        # Signup Form
        with st.form(key='signup_form'):
            st.header("Sign Up")
            signup_username = st.text_input("New Username")
            signup_password = st.text_input("New Password", type="password", key="signup_password")

            signup_button_clicked = st.form_submit_button("Create Account")
            
            if signup_button_clicked:
                if signup_username and signup_password:
                    # Check if the username already exists
                    if user_exists(signup_username):
                        st.error("Username already exists. Please choose a different username.")
                    else:                        
                        # Insert the new user into the employee table
                        insert_query = f"INSERT INTO employee (username, password) VALUES ('{signup_username}', '{signup_password}')"
                        cursor.execute(insert_query)
                        connection.commit()  # Commit the changes to the database
                        st.session_state.authenticated = True
                        st.session_state.username = signup_username
                        st.success("Account created successfully! You are now logged in.")
                else:
                    st.warning("Please enter both a username and password to sign up.")

        # Login Form
        with st.form(key='login_form'):
            st.header("Log In")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")


            if st.form_submit_button("Login"):
            	if user_exists(username) and check_password(username, password):
            	    st.session_state.authenticated = True
            	    st.session_state.username = username
            	    st.success("Login Successful!")
            	    st.stop()
            	else:
            	    st.error("Invalid Username or Password")

        # Admin Login Form
        if st.checkbox("Admin Login"):
            admin_username = st.text_input("Admin Username")
            admin_password = st.text_input("Admin Password", type="password")

            if st.button("Admin Login"):
                if is_admin(admin_username) and check_password(admin_username, admin_password):
                    st.session_state.authenticated = True
                    st.session_state.username = admin_username
                    st.success("Admin Login Successful!")
                    st.stop()
                else:
                    st.error("Invalid Admin Username or Password")

if __name__ == "__main__":
    main()

cursor.close()
connection.close()

