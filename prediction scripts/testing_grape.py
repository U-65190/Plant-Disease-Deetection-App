import cv2 as cv
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import os

# Load the saved model for prediction
model = load_model(r'..\models\crop_disease_model_grape.keras')

# Define the class names for grape diseases (ensure they match the order in which they were trained)
class_names = [
    'Grape_Black_rot', 
    'Grape_Esca_(Black_Measles)', 
    'Grape_Healthy', 
    'Grape_Leaf_blight_(Isariopsis_Leaf_Spot)'
]

# Define the disease information (Preventive Measures and Medications)
disease_info = {
    'Grape_Black_rot': {
        'Preventive Measures': "Prune infected parts, avoid overhead watering, and practice good field sanitation.",
        'Medications': "Use fungicides like mancozeb or myclobutanil."
    },
    'Grape_Esca_(Black_Measles)': {
        'Preventive Measures': "Avoid planting in infected soils and practice good vineyard hygiene.",
        'Medications': "No known cure, manage symptoms through proper pruning and canopy management."
    },
    'Grape_Leaf_blight_(Isariopsis_Leaf_Spot)': {
        'Preventive Measures': "Remove and destroy infected leaves. Avoid overhead irrigation.",
        'Medications': "Fungicide sprays such as copper-based compounds can help control the spread."
    },
    'Grape_Healthy': {
        'Preventive Measures': "Maintain good vineyard management practices, proper irrigation, and pest control.",
        'Medications': "No action needed."
    }
}

# Define your location (latitude and longitude for a vineyard location)
latitude = 37.7749  # Example: San Francisco latitude
longitude = -122.4194  # Example: San Francisco longitude

# Fetch weather data
def fetch_weather_data(latitude, longitude):
    api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=Asia/Tokyo"
    response = requests.get(api_url)
    if response.status_code == 200:
        weather_data = response.json()
        daily_data = weather_data['daily']
        temperatures_max = daily_data.get('temperature_2m_max', [])
        temperatures_min = daily_data.get('temperature_2m_min', [])
        precipitations = daily_data.get('precipitation_sum', [])
        times = daily_data.get('time', [])
        
        weather_df = pd.DataFrame({
            'time': times,
            'temperature_max': temperatures_max,
            'temperature_min': temperatures_min,
            'precipitation': precipitations
        })
        
        return weather_df
    else:
        raise RuntimeError(f"Failed to fetch weather data. Status code: {response.status_code}")

# Analyze weather impact
def analyze_weather_impact(weather_df):
    max_temp = weather_df['temperature_max'].mean()
    if max_temp > 30:
        return "High temperatures may stress the vines and increase disease risk."
    elif max_temp > 20:
        return "Optimal temperature range for the grapevines."
    else:
        return "Low temperatures may slow down vine growth."

# Load and preprocess the test image (grape)
img_path = r'D:\Python programs\SIH\train\train\grape_final\Grape___Black_rot\3b646501-0c1f-4f1b-889e-26a4a31d03f7___FAM_B.Rot 5084.JPG'  # Update with the path to the grape image

# Check if the image file exists
if not os.path.exists(img_path):
    raise FileNotFoundError(f"Image file not found: {img_path}")

img = cv.imread(img_path)

# Check if the image was loaded successfully
if img is None:
    raise ValueError(f"Failed to load image. The file may be corrupted or not a valid image format: {img_path}")

img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
img_resized = cv.resize(img, (180, 180))  # Resize to match model input
img_array = np.array([img_resized]) / 255.0  # Normalize the image

# Display the image
plt.imshow(img_resized)
plt.axis('off')
plt.show()

# Make the prediction
prediction = model.predict(img_array)
print(f"Model Prediction Output: {prediction}")

# Check if the prediction output size matches the number of classes
if len(prediction[0]) != len(class_names):
    print(f"Warning: The number of predicted classes ({len(prediction[0])}) does not match the number of defined class names ({len(class_names)}).")
else:
    index = np.argmax(prediction)
    predicted_label = class_names[index]
    print(f'Prediction: {predicted_label}')

    # Fetch and display preventive measures and medications
    if predicted_label in disease_info:
        preventive_measures = disease_info[predicted_label]['Preventive Measures']
        medications = disease_info[predicted_label]['Medications']
        
        print(f"Preventive Measures: {preventive_measures}")
        print(f"Medications: {medications}")
    else:
        print(f"No information available for this disease. Predicted label: {predicted_label}")

    # Fetch and analyze weather data
    weather_df = fetch_weather_data(latitude, longitude)
    weather_impact = analyze_weather_impact(weather_df)
    print(f"Weather Impact: {weather_impact}")
