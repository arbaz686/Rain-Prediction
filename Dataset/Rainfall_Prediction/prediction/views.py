from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import pickle
import subprocess

# Load the machine learning model when the Django app starts
model = pickle.load(open("prediction/models/cat.pkl", "rb"))

def home(request):
    return render(request, "index.html")

def predict(request):
    if request.method == "POST":
        # Retrieve input data from the form
        date = request.POST['date']
        day = float(pd.to_datetime(date, format="%Y-%m-%d").day)
        month = float(pd.to_datetime(date, format="%Y-%m-%d").month)
        minTemp = float(request.POST['mintemp'])
        maxTemp = float(request.POST['maxtemp'])
        rainfall = float(request.POST['rainfall'])
        
        evaporation_str = request.POST['evaporation']
        if evaporation_str == 'NA':
            evaporation = 0.0  # Set a default value for 'NA'
        else:
            evaporation = float(evaporation_str)
        
        sunshine_str = request.POST['sunshine']
        if sunshine_str == 'NA':
            sunshine = None  # Handle 'NA' as None or missing data
        else:
            sunshine = float(sunshine_str)
        
        windgustspeed_str = request.POST['windgustspeed']
        if windgustspeed_str == 'NA':
            windgustspeed = 0.0  # Set a default value for 'NA'
        else:
            windgustspeed = float(windgustspeed_str)
        
        windspeed9am_str = request.POST['windspeed9am']
        if windspeed9am_str == 'NA':
            windspeed9am = 0.0  # Set a default value for 'NA'
        else:
            windspeed9am = float(windspeed9am_str)
        
        windspeed3pm_str = request.POST['windspeed3pm']
        if windspeed3pm_str == 'NA':
            windspeed3pm = 0.0  # Set a default value for 'NA'
        else:
            windspeed3pm = float(windspeed3pm_str)
        
        humidity9am_str = request.POST['humidity9am']
        if humidity9am_str == 'NA':
            humidity9am = 0.0  # Set a default value for 'NA'
        else:
            humidity9am = float(humidity9am_str)
        
        humidity3pm_str = request.POST['humidity3pm']
        if humidity3pm_str == 'NA':
            humidity3pm = 0.0  # Set a default value for 'NA'
        else:
            humidity3pm = float(humidity3pm_str)
        
        pressure9am_str = request.POST['pressure9am']
        if pressure9am_str == 'NA':
            pressure9am = 0.0  # Set a default value for 'NA'
        else:
            pressure9am = float(pressure9am_str)
        
        pressure3pm_str = request.POST['pressure3pm']
        if pressure3pm_str == 'NA':
            pressure3pm = 0.0  # Set a default value for 'NA'
        else:
            pressure3pm = float(pressure3pm_str)
        
        temp9am_str = request.POST['temp9am']
        if temp9am_str == 'NA':
            temp9am = 0.0  # Set a default value for 'NA'
        else:
            temp9am = float(temp9am_str)
        
        temp3pm_str = request.POST['temp3pm']
        if temp3pm_str == 'NA':
            temp3pm = 0.0  # Set a default value for 'NA'
        else:
            temp3pm = float(temp3pm_str)
        
        cloud9am_str = request.POST['cloud9am']
        if cloud9am_str == 'NA':
            cloud9am = 0.0  # Set a default value for 'NA'
        else:
            cloud9am = float(cloud9am_str)
        
        cloud3pm_str = request.POST['cloud3pm']
        if cloud3pm_str == 'NA':
            cloud3pm = 0.0  # Set a default value for 'NA'
        else:
            cloud3pm = float(cloud3pm_str)
        
        location = int(request.POST['location'])
        
        winddir9am = int(request.POST['winddir9am'])
        winddir3pm = int(request.POST['winddir3pm'])
        windgustdir = int(request.POST['windgustdir'])
        raintoday = int(request.POST['raintoday'])
        
        # Create a list with the input data
        input_data = [
            minTemp, maxTemp, rainfall, evaporation, sunshine,
            windgustspeed, windspeed9am, windspeed3pm, humidity9am, humidity3pm,
            pressure9am, pressure3pm, temp9am, temp3pm, cloud9am, cloud3pm,
            location, winddir9am, winddir3pm, windgustdir, raintoday,
            day, month,
        ]

        # Make predictions using the model
        pred = model.predict([input_data])
        
        # Determine the output based on model predictions
        output = "after_sunny.html" if pred == 0 else "after_rainy.html"
        
        return render(request, output)
    
    return render(request, "predictor.html")

def run_notebook(request):
    try:
        subprocess.run(["jupyter", "nbconvert", "--to", "script", "RainPrediction2.ipynb"])
        subprocess.run(["python", "RainPrediction2.py"]) 
        
        result = "Notebook executed successfully"
    except Exception as e:
        result = f"Error executing the notebook: {str(e)}"
    
    return JsonResponse({"result": result})
