from django.urls import path
from .views import calendar_view, match_data, get_or_create_match, get_matches

urlpatterns = [
    path('', calendar_view, name='calendar'),
    # path('match/', match_data, name='match_data'),
    path('matches/', get_matches, name='get_matches'),
    # path('get_matches/', get_matches, name='get_matches'),
]