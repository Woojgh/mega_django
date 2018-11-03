
"""
Disc-chat URL Configuration
"""
from django.urls import path, include
from .views import DiscordDashboard

urlpatterns = [
    path('', DiscordDashboard.as_view(), name='discord dashboard'),
]