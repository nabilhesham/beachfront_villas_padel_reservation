from django.urls import path
# from .views import calendar_view, match_data, get_or_create_match, get_matches
from . import views

urlpatterns = [
    # Auth URLs
    path('login/', views.login_view, name='login'),
    path('change-password/', views.change_password, name='change-password'),
    path('logout/', views.logout_view, name='logout'),

    # Sub Users URLs
    path('add-sub-user/', views.add_sub_user, name='add-sub-user'),
    path('delete-sub-user/<int:sub_user_id>/', views.delete_sub_user, name='delete-sub-user'),

    # Views URLs
    path('', views.home_view, name='home'),
    path('under-construction/', views.under_construction_view, name='under-construction'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('user-profile/', views.user_profile_view, name='user-profile'),
    path('rules/', views.rules_view, name='rules'),

    # Data URLs
    path('api/user-profile/', views.user_profile_data, name='user-profile-data'),
    path('api/matches/', views.get_matches, name='get-matches'),
    path('api/toggle-player-reservation/', views.toggle_player_reservation, name='toggle-player-reservation'),

]