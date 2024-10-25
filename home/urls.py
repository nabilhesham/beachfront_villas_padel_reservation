# home/urls.py
from django.urls import path
from .views import under_development

urlpatterns = [
    path('', under_development, name='under_development'),
]
