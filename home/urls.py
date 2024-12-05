from django.urls import path
# from .views import calendar_view, match_data, get_or_create_match, get_matches
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('change-password/', views.change_password, name='change-password'),
    path('logout/', views.logout_view, name='logout'),


    path('', views.home_view, name='home'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('matches/', views.get_matches, name='get_matches'),
]