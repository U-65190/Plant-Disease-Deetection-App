
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
import requests

def fetch_weather_forecast(latitude, longitude):
    # API URL for New Delhi timezone (adjust as needed)
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

def check_cherry_powdery_mildew_occurrence(avg_temp, avg_precip):
    # Define temperature and precipitation bounds for Cherry Powdery Mildew
    t, T = 15, 25  # Temperature range
    p, P = 0.1, 0.4  # Precipitation bounds

    # Check if conditions favor the occurrence of Cherry Powdery Mildew
    check_disease_occurrence(t, T, p, P, avg_temp, avg_precip, "Cherry Powdery Mildew")

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
model = load_model(r'..\models\crop_disease_model_cherry.keras')

# Define the class names (ensure they match the order in which they were trained)
class_names = [
    'Cherry_Powdery_Mildew',
    'Cherry_Healthy'
]

# Define the disease information (Preventive Measures and Medications)
disease_info = {
    'Cherry_Powdery_Mildew': {
        'Preventive Measures': "Ensure proper pruning and apply sulfur-based fungicides to prevent Powdery Mildew.",
        'Medications': "Apply fungicides like myclobutanil or potassium bicarbonate to treat infections."
    },
    'Cherry_Healthy': {
        'Preventive Measures': "Maintain good orchard hygiene and inspect regularly for disease symptoms.",
        'Medications': "No action needed."
    }
}

# Load and preprocess the test image
img_path = r'D:\Python programs\SIH\train\train\cherry_final\Cherry_(including_sour)___Powdery_mildew\0fe7c76c-cc34-4b75-b254-45c62cbab52a___FREC_Pwd.M 4783.JPG'  # Update with the path to the cherry image
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
check_cherry_powdery_mildew_occurrence(avg_temp, avg_precip)
