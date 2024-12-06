from django.urls import path
# from .views import calendar_view, match_data, get_or_create_match, get_matches
from . import views

urlpatterns = [
    # Auth URLs
    path('login/', views.login_view, name='login'),
    path('change-password/', views.change_password, name='change-password'),
    path('logout/', views.logout_view, name='logout'),


    # Views URLs
    path('', views.home_view, name='home'),
    path('under-construction/', views.under_construction_view, name='under-construction'),
    path('calendar/', views.calendar_view, name='calendar'),

    # Data URLs
    path('api/matches/', views.get_matches, name='get-matches'),
    path('api/toggle-player-reservation/', views.toggle_player_reservation, name='toggle-player-reservation'),

]