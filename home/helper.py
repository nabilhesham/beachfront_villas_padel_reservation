# Django imports
from datetime import time, timedelta, datetime

# App imports
from .models import Match, Reservation


def get_week_start():
    """
    Helper to get the start of the current week (Monday).
    """
    current_date = datetime.now()
    start_of_week = current_date - timedelta(days=current_date.weekday())
    return start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)


# Validate whether the match is on off period or not
def validate_time_slot(date, start_time):
    day_of_week = date.weekday()  # 0 = Monday, 6 = Sunday
    if day_of_week in [5, 6]:  # Saturday or Sunday
        if time(9, 0) <= start_time.time() < time(10, 0):
            return False
    return True


# Check busy hour
def is_busy_hour(start_time, end_time):
    busy_start = time(17, 0)  # 5 PM
    busy_end = time(20, 0)    # 8 PM

    # Extract the time part of the datetime objects
    start_time_only = start_time.time()
    end_time_only = end_time.time()

    return start_time_only >= busy_start and end_time_only <= busy_end


# validate match reservation
def validate_busy_hour_limit(user, player_type):
    # Include the user and their sub-users in the count
    # related_users = [user] + list(user.sub_users.all())
    related_users = []
    if user.is_master is False:
        user = user.parent
    related_users.append(user)

    # Count reservations for the user and their sub-users for the current week.
    start_of_week = get_week_start()
    end_of_week = start_of_week + timedelta(days=7)

    # Count reservations during busy hours
    busy_hour_reservations = Reservation.objects.filter(
        user__in=related_users,
        match__start_time__gte=start_of_week,
        match__start_time__lt=end_of_week,
        player_type=player_type,
        match__start_time__hour__gte=17,  # Busy hours start at 5 PM
        match__end_time__hour__lte=20,  # Busy hours end at 8 PM
    ).count()

    # Check limits
    if player_type == 'main' and busy_hour_reservations >= 2:
        return False
    if player_type == 'reserve' and busy_hour_reservations >= 2:
        return False
    return True
