import pandas as pd
import streamlit as st
import pickle
import numpy as np

# Load the new data and model
data = pd.read_csv('cleaned_data.csv')
pipe = pickle.load(open('LinearModel.pkl', 'rb'))

# Updated prediction function with additional features
def predict_price(sqft, bath, balcony, location, bhk, age, parking, floor_level, furnishing, distance, property_type, security):
    # Convert categorical inputs to the appropriate format
    parking = 1 if parking == 'Yes' else 0
    security = 1 if security == 'Yes' else 0
    
    # Create a DataFrame for the input data
    input_data = pd.DataFrame([[sqft, bath, balcony, location, bhk, age, parking, floor_level, furnishing, distance, property_type, security]], 
                              columns=['total_sqft', 'bath', 'balcony', 'site_location', 'bhk', 'age', 'parking', 'floor_level', 'furnishing', 'distance', 'property_type', 'security'])
    
    # Make the prediction
    prediction = pipe.predict(input_data)[0] * 1e5
    return np.round(prediction, 2)

# Streamlit app setup
st.markdown("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: green;
            color: #333;
        }
        .title {
            text-align: center;
            color: #4CAF50;
            font-size: 100px;
            margin-top: 20px;
        }
        .subtitle_1 {
            text-align: center;
            color:#555
            font-size: 50px
        }
            
        .subtitle {
            text-align: center;
            color: #555;
            font-size: 20px;
        }
        .container {
            background-color: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-top: 30px;
            margin-bottom: 30px;
        }
        .button {
            background-color: #4CAF50;
            color: white;
            padding: 12px 24px;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }
        .button:hover {
            background-color: #45a049;
        }
        footer {
            text-align: center;
            font-size: 12px;
            color: #777;
            padding: 20px;
            background-color: #f1f1f1;
            position: fixed;
            bottom: 0;
            width: 100%;
        }
    </style>
    <div class="title">FutureNest</div>
    <div class="subtitle_1"><h2>Pune House Price Predictor</h2></div>
    <div class="subtitle">Predict the price of houses in Pune based on various features</div><br><br>
""", unsafe_allow_html=True)

# Get unique locations and other categorical variables from the data
locations = sorted(data['site_location'].unique())
furnishing_options = ['Unfurnished', 'Semi-Furnished', 'Furnished']
property_type_options = ['Apartment', 'Villa', 'Independent House']
floor_level_options = ['Ground', 'Middle', 'Top']
security_options = ['Yes', 'No']

# Input components in columns
col1, col2, col3 = st.columns(3)

with col1:
    location = st.selectbox("Select Location", locations)
    bhk = st.number_input("Enter BHK", min_value=1, max_value=10, step=1)

with col2:
    sqft = st.number_input("Enter total house area in sqft", min_value=100, max_value=10000, step=1)
    bath = st.number_input("Enter number of bathroom(s)", min_value=1, max_value=10, step=1)

with col3:
    balcony = st.number_input("Enter number of balcony(ies)", min_value=0, max_value=5, step=1)
    age = st.number_input("Enter the age of the property (in years)", min_value=1, max_value=100, step=1)

# Additional inputs
parking = st.selectbox("Is parking available?", ['Yes', 'No'])
floor_level = st.selectbox("Select Floor Level", floor_level_options)
furnishing = st.selectbox("Furnishing Status", furnishing_options)
distance = st.number_input("Enter distance to nearest key location (in km)", min_value=0.1, max_value=100.0, step=0.1)
property_type = st.selectbox("Select Property Type", property_type_options)
security = st.selectbox("Is the property in a gated community or has security?", security_options)

# Container for the prediction button
with st.container():
    if st.button("🔮 Predict Price", key="predict_button", help="Click to predict the price of the house"):
        if location and bhk and sqft and bath and balcony and age and distance:
            prediction = predict_price(
                sqft, bath, balcony, location, bhk, age,
                parking, floor_level, furnishing, distance, property_type, security
            )
            st.write(f"### Predicted Price: ₹{prediction}")
        else:
            st.warning("Please fill in all the required input fields.")

# Footer
st.markdown("""
    <footer>
        <p>Developed by FutureNest &copy; 2024 | All Rights Reserved</p>
    </footer>
""", unsafe_allow_html=True)
