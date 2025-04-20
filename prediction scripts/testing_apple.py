import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

# Load the saved model for prediction
model = load_model(r'..\models\crop_disease_model_apple.keras')

# Define the class names (ensure they match the order in which they were trained)
class_names = [
    'Apple_Scab', 
    'Apple_BlackRot', 
    'Apple_Cedar_apple_rust', 
    'Apple_Healthy'
]

# Define the disease information (Preventive Measures and Medications)
disease_info = {
    'Apple_Scab': {
        'Preventive Measures': "Rake and destroy fallen leaves, and prune the tree to promote airflow.",
        'Medications': "Apply fungicides such as captan or mancozeb at regular intervals."
    },
    'Apple_BlackRot': {
        'Preventive Measures': "Remove infected fruit and prune dead or cankered limbs. Avoid injuries to the tree.",
        'Medications': "Fungicides like benomyl or thiophanate-methyl can be used to treat infections."
    },
    'Apple_Cedar_apple_rust': {
        'Preventive Measures': "Remove nearby juniper trees, which host the rust, and ensure proper tree spacing.",
        'Medications': "Use fungicides such as myclobutanil to control the disease."
    },
    'Apple_Healthy': {
        'Preventive Measures': "Maintain regular tree inspections, proper pruning, and good irrigation practices.",
        'Medications': "No action needed."
    },
}

# Load and preprocess the test image
img_path = r'D:\Python programs\SIH\train\train\apple_final\Apple___Cedar_apple_rust\2ac8d689-f30a-4eee-a856-86c92f8dcbd2___FREC_C.Rust 3952.JPG'  # Update with the path to the apple image
img = cv.imread(img_path)
img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

# Resize the image to match the input size of the model (128x128)
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
