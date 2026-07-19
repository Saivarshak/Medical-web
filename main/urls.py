from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload, name='upload'),
    path('analysis/', views.analysis, name='analysis'),
    path('medical-report/', views.medical_report, name='medical_report'),
    path('hospitals/', views.hospitals, name='hospitals'),
    path('emergency/', views.emergency, name='emergency'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('history/', views.history, name='history'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('admin-panel/', views.admin_view, name='admin'),
    path('api/hospitals/', views.get_nearest_hospitals, name='api_hospitals'),
]
