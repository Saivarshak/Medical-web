from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ScanHistory, Alert
import json
import uuid
from datetime import datetime

def index(request):
    return render(request, 'main/index.html')

def login_view(request):
    return render(request, 'main/login.html')

def register_view(request):
    return render(request, 'main/register.html')

def dashboard(request):
    return render(request, 'main/dashboard.html')

def upload(request):
    return render(request, 'main/upload.html')

def analysis(request):
    return render(request, 'main/analysis.html')

def medical_report(request):
    return render(request, 'main/medical-report.html')

def hospitals(request):
    return render(request, 'main/hospitals.html')

def emergency(request):
    return render(request, 'main/emergency.html')

def chatbot(request):
    return render(request, 'main/chatbot.html')

def history(request):
    return render(request, 'main/history.html')

def profile(request):
    return render(request, 'main/profile.html')

def settings_view(request):
    return render(request, 'main/settings.html')

def admin_view(request):
    return render(request, 'main/admin.html')

# API-like views for AJAX
def get_nearest_hospitals(request):
    # Mock data as in FastAPI
    hospitals = [
        {"name": "City General Emergency Hospital", "address": "24 Care Street, Central District", "latitude": 17.385, "longitude": 78.4867, "distance_km": 1.4},
        {"name": "Rapid Trauma & Critical Care", "address": "8 LifeLine Road, Medical Zone", "latitude": 17.3921, "longitude": 78.4812, "distance_km": 2.1},
    ]
    return JsonResponse({"hospitals": hospitals})
