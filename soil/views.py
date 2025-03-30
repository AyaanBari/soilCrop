import pickle
import numpy as np
from django.shortcuts import render, get_object_or_404
from .models import Crop
from .data import crops_data  # Ensure this is correct
from . import weather  # Import weather.py to fetch climate data
from joblib import load
from django.http import JsonResponse
from django.conf import settings
import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

# Load the trained ML Model
with open("./soil/model1.pkl", "rb") as f:
    model1 = pickle.load(f)

def home(request):
    """Renders the landing page."""
    return render(request, 'landing.html')

def form_view(request):
    """Handles form submission and fetches weather data for the given state."""
    if request.method == "POST":
        state = request.POST.get('state')
        district = request.POST.get('district')

        # Fetch weather data (Rain, Temperature, Humidity)
        weather_data = weather.temp(state)
        rain = int(weather_data[0][0])  # Rainfall data
        temp = int(weather_data[1][0])  # Temperature data
        humd = int(weather_data[2][0])  # Humidity data

        return render(request, "form.html", {"rain": rain, "humd": humd, "temp": temp})

    return render(request, "form.html")

def recommend(request):
    """Processes user input, predicts the best crop, and displays relevant information."""
    if request.method == 'POST':
        # Retrieve form data
        N = request.POST.get("N")
        P = request.POST.get("P")
        K = request.POST.get("K")
        temperature = request.POST.get("Temp")
        humidity = request.POST.get("Humd")
        PH = request.POST.get("Ph")
        rainfall = request.POST.get("rnfall")

        # Convert input to NumPy array for model prediction
        new_input = np.asarray([[N, P, K, temperature, humidity, PH, rainfall]]).astype(np.float32)
        crop_id = float(model1.predict(new_input)[0])   # Predict crop ID

        # Crop index mapping
        crop_idx = {
            20: 'rice', 11: 'maize', 3: 'chickpea', 9: 'kidneybeans', 18: 'pigeonpeas',
            13: 'mothbeans', 14: 'mungbean', 2: 'blackgram', 10: 'lentil', 19: 'pomegranate',
            1: 'banana', 12: 'mango', 7: 'grapes', 21: 'watermelon', 15: 'muskmelon',
            0: 'apple', 16: 'orange', 17: 'papaya', 4: 'coconut', 6: 'cotton',
            8: 'jute', 5: 'coffee'
        }

        # Get the crop name from the predicted crop ID
        crop_name = crop_idx.get(crop_id, "UNKNOWN").lower().strip()
        filename = crop_idx.get(crop_id, "UNKNOWN").upper().strip()
        print(filename)

        # Fetch crop details from the database
        crop = crops_data.get(crop_name)
        if not crop:
            return JsonResponse({"error": f"Crop '{crop_name}' data not found"}, status=404)

        # Prepare context for rendering
        context = {
            "filename": filename,
            "crop": crop.get("NAME", "N/A"),
            "description": crop.get("DESCRIPTION", "No description available"),
            "types": crop.get("TYPE", "N/A"),
            "disease": crop.get("DISEASES", "N/A"),
            "companion": crop.get("COMPANION", "N/A"),
            "pests": crop.get("PESTS", "N/A"),
            "fertilizer": crop.get("FERTILIZER", "N/A"),
            "tips": crop.get("TIPS", "N/A"),
            "spacing": crop.get("SPACING", "N/A"),
            "watering": crop.get("WATERING", "N/A"),
            "storage": crop.get("STORAGE", "N/A"),
        }

        return render(request, "output.html", context)




def retry(request):
    """Renders the landing page for retrying."""
    return render(request, 'landing.html')
