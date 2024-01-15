from django.urls import path
from . import views

app_name = 'prediction'

urlpatterns = [
    path("", views.home, name="home"),  # URL for the home page, e.g., http://localhost:8000/
    path("predict", views.predict, name="predict"),  # URL for the prediction page, e.g., http://localhost:8000/predict/
]
