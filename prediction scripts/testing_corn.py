import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
import requests

def fetch_weather_forecast(latitude, longitude):
    # API URL for weather data (adjust as needed)
    api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=Asia/Kolkata"

    # Fetch weather data
    response = requests.get(api_url)
    data = response.json()

    # Extract daily temperatures and precipitation
    daily_max_temps = data['daily']['temperature_2m_max']
    daily_min_temps = data['daily']['temperature_2m_min']
    daily_precipitation = data['daily']['precipitation_sum']

    # Calculate the 7-day averages
    avg_temp = np.mean([(max_temp + min_temp) / 2 for max_temp, min_temp in zip(daily_max_temps, daily_min_temps)])
    avg_precip = np.mean(daily_precipitation)

    return avg_temp, avg_precip

def check_corn_cercospora_leaf_spot_occurrence(avg_temp, avg_precip):
    # Define temperature and precipitation bounds for Cercospora leaf spot
    t, T = 20, 30  # Temperature range
    p, P = 0.2, 0.6  # Precipitation bounds

    # Check if conditions favor the occurrence of Cercospora leaf spot
    check_disease_occurrence(t, T, p, P, avg_temp, avg_precip, "Cercospora leaf spot Gray leaf spot")

def check_corn_common_rust_occurrence(avg_temp, avg_precip):
    # Define temperature and precipitation bounds for Common rust
    t, T = 18, 28  # Temperature range
    p, P = 0.3, 0.8  # Precipitation bounds

    # Check if conditions favor the occurrence of Common rust
    check_disease_occurrence(t, T, p, P, avg_temp, avg_precip, "Common rust")

def check_corn_northern_leaf_blight_occurrence(avg_temp, avg_precip):
    # Define temperature and precipitation bounds for Northern Leaf Blight
    t, T = 22, 32  # Temperature range
    p, P = 0.4, 0.9  # Precipitation bounds

    # Check if conditions favor the occurrence of Northern Leaf Blight
    check_disease_occurrence(t, T, p, P, avg_temp, avg_precip, "Northern Leaf Blight")

def check_disease_occurrence(t, T, p, P, avg_temp, avg_precip, disease_name):
    # Check temperature range
    if t < avg_temp < T:
        # Check precipitation conditions
        if avg_precip < P or avg_precip > p or p < avg_precip < P:
            print(f"There is a chance of an occurrence of {disease_name}")
            print(f"Prevention: Take necessary actions to prevent {disease_name}.")
        else:
            print(f"No significant chance of {disease_name} based on precipitation data.")
    else:
        print(f"No significant chance of {disease_name} based on temperature data.")

# Load the saved model for prediction
model = load_model(r'..\models\crop_disease_model_corn1.keras')

# Define the class names (ensure they match the order in which they were trained)
class_names = [
    'Corn_Cercospora_Gray_leaf_spot',
    'Corn_Common_rust',
    'Corn_Northern_Leaf_Blight',
    'Corn_Healthy'
]

# Define the disease information (Preventive Measures and Medications)
disease_info = {
    'Corn_Cercospora_Gray_leaf_spot': {
        'Preventive Measures': "Rotate crops and apply fungicides like strobilurins or triazoles to reduce Gray Leaf Spot.",
        'Medications': "Apply fungicides at the early onset of symptoms."
    },
    'Corn_Common_rust': {
        'Preventive Measures': "Plant resistant hybrids and practice crop rotation to prevent Common Rust.",
        'Medications': "Use fungicides like azoxystrobin or propiconazole."
    },
    'Corn_Northern_Leaf_Blight': {
        'Preventive Measures': "Use resistant hybrids, rotate crops, and manage plant debris to prevent Northern Leaf Blight.",
        'Medications': "Apply fungicides like pyraclostrobin or mancozeb."
    },
    'Corn_Healthy': {
        'Preventive Measures': "Maintain healthy crop management practices such as crop rotation, irrigation, and weed control.",
        'Medications': "No action needed."
    }
}

# Load and preprocess the test image
img_path = r'D:\Python programs\SIH\train\train\corn final\Corn_(maize)___Common_rust_\RS_Rust 1587.JPG'  # Update with the path to the corn image
img = cv.imread(img_path)
img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

# Resize the image to match the input size of the model (180x180)
img_resized = cv.resize(img, (180, 180))

# Normalize the image
img_array = np.array([img_resized]) / 255.0  # Scale pixel values to [0, 1]

# Display the image
plt.imshow(img_resized)
plt.axis('off')  # Hide the axes for a better display
plt.show()

# Make the prediction
prediction = model.predict(img_array)
index = np.argmax(prediction)

# Get the predicted label
predicted_label = class_names[index]
print(f'Prediction: {predicted_label}')

# Fetch and display preventive measures and medications
if predicted_label in disease_info:
    preventive_measures = disease_info[predicted_label]['Preventive Measures']
    medications = disease_info[predicted_label]['Medications']

    print(f"Preventive Measures: {preventive_measures}")
    print(f"Medications: {medications}")
else:
    print("No information available for this disease.")

# Example usage with New Delhi coordinates
latitude = 28.6139
longitude = 77.2090
avg_temp, avg_precip = fetch_weather_forecast(latitude, longitude)

# Check for disease occurrence based on forecasted values
check_corn_cercospora_leaf_spot_occurrence(avg_temp, avg_precip)
check_corn_common_rust_occurrence(avg_temp, avg_precip)
check_corn_northern_leaf_blight_occurrence(avg_temp, avg_precip)
