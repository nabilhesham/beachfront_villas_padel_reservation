# Django imports
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta, datetime
from django.utils.dateparse import parse_datetime

# App imports
from .models import Match, Reservation




############################# views ##########################################
def home_view(request):
    return render(request, 'base.html')

def calendar_view(request):
    return render(request, 'calendar.html')






############################# Data ##########################################
def match_data(request):
    today = timezone.now()
    future_date = today + timedelta(days=2)
    matches = Match.objects.filter(start_time__date__gte=today.date(), start_time__date__lte=future_date.date())

    match_data = []
    for match in matches:
        main_count = match.main_players_count
        reserve_count = match.reserve_players_count
        status = 'green' if main_count < 4 else 'yellow' if main_count == 4 and reserve_count < 4 else 'red'

        match_data.append({
            "id": match.id,
            "start_time": match.start_time.isoformat(),
            "end_time": match.end_time.isoformat(),
            # "main_count": main_count,
            # "reserve_count": reserve_count,
            'main_players': [user.username for user in match.main_players.all()],
            'reserve_players': [user.username for user in match.reserve_players.all()],
            "status": status
        })
    # match_data = [
    #     {
    #         "id": 1,
    #         "start": "2024-11-16T18:00:00",
    #         "end": "2024-11-16T19:00:00",
    #         "main_count": 0,
    #         "reserve_count": 0,
    #         "status": "green"
    #     }
    # ]
    return JsonResponse(match_data, safe=False)


def get_matches(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S')
        end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S')

        # Set minutes, seconds, and microseconds to zero
        start_date = start_date.replace(minute=0, second=0, microsecond=0)
        end_date = end_date.replace(minute=0, second=0, microsecond=0)

    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    matches = []
    matches_sql = Match.objects.filter(start_time__gte=start_date, end_time__lte=end_date)
    current_time = start_date

    while current_time < end_date:
        end_time = current_time + timedelta(hours=1)
        match = matches_sql.filter(start_time=current_time, end_time=end_time).first()
        if not match:
            matches.append({
                'start_time': current_time,
                'end_time': end_time,
                'main_players': [],
                'reserve_players': [],
            })
        else:
            print(match)
            matches.append({
                'start_time': match.start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'end_time': match.end_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'main_players': [user.username for user in match.main_players.all()],
                'reserve_players': [user.username for user in match.reserve_players.all()],
            })

        current_time = end_time

    return JsonResponse({'matches': matches})


def get_or_create_match(request, date):
    # Convert the string date (YYYY-MM-DD) to a naive datetime object (without time zone)
    match_date = datetime.strptime(date, "%Y-%m-%d").date()  # Naive date (no timezone)

    # Try to find an existing match for that day
    match = Match.objects.filter(start_time__date=match_date).first()

    if not match:
        # If no match exists, create a new one with default values
        start_time = datetime.combine(match_date, datetime.min.time())  # Naive datetime
        end_time = start_time + timedelta(hours=1)  # 1 hour match duration (default)

        match = Match.objects.create(
            start_time=start_time,
            end_time=end_time
        )

        # Optionally add default players or other fields to this new match
        match.save()

    # Return match details as JSON
    return JsonResponse({
        'start_time': match.start_time.isoformat(),
        'end_time': match.end_time.isoformat(),
        'main_players': [user.username for user in match.main_players.all()],
        'reserve_players': [user.username for user in match.reserve_players.all()],
        'id': match.id,
    })