"""
Disc-chat URL Configuration
"""
from django.urls import path, include
from .views import profile_view

urlpatterns = [
    path('', profile_view.as_view(), name='profile'),
]