# Django imports
from datetime import time, timedelta, datetime
from django.contrib.auth import get_user_model


# App imports
from .models import Match, Reservation
from .variables import *

User = get_user_model()

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
    if day_of_week in no_match_days_list:
        if no_match_days_start_hour <= start_time.time() < no_match_days_end_hour:
            return False
    if no_match_all_week_start_hour <= start_time.time() < no_match_all_week_end_hour:
        return False
    return True


# Check busy hour
def is_busy_hour(start_time, end_time):
    # Extract the time part of the datetime objects
    start_time_only = start_time.time()
    end_time_only = end_time.time()

    return start_time_only >= busy_hour_start and end_time_only <= busy_hour_end


# validate if related players are main players in the same match
def validate_reserve_reservation(match, user):
    validated = True

    # get list of related users
    user_list = []
    if user.is_master is True:
        sub_users_sql = User.objects.filter(parent=user)
        for sub_user in sub_users_sql:
            user_list.append(sub_user)
    else:
        user_list.append(user.parent)

    # main players reservations for the match
    match_main_reservations = Reservation.objects.filter(
        match=match,
        user__in=user_list,
        player_type="main"
    )

    # check if any related player is main player in the match
    if len(match_main_reservations) > 0:
        validated = False

    return validated


# validate match reservation
def validate_busy_hour_limit(user, player_type):
    # Count reservations for the user and their sub-users for the current week.
    start_of_week = get_week_start()
    end_of_week = start_of_week + timedelta(days=7)

    # Count reservations during busy hours for user
    busy_hour_reservations = Reservation.objects.filter(
        user=user,
        match__start_time__gte=start_of_week,
        match__start_time__lt=end_of_week,
        player_type=player_type,
        match__start_time__hour__gte=busy_hour_start_hour,
        match__end_time__hour__lte=busy_hour_end_hour,
    ).count()

    # Check limits of user
    if player_type == 'main' and busy_hour_reservations >= allowed_user_busy_hour_main_reservations:
        return False
    if player_type == 'reserve' and busy_hour_reservations >= allowed_user_busy_hour_reserve_reservations:
        return False

    if user.is_master is False:
        # if user is sub count parent reservations
        user = user.parent
        # Count reservations during busy hours for user
        parent_busy_hour_reservations = Reservation.objects.filter(
            user=user,
            match__start_time__gte=start_of_week,
            match__start_time__lt=end_of_week,
            player_type=player_type,
            match__start_time__hour__gte=busy_hour_start_hour,
            match__end_time__hour__lte=busy_hour_end_hour,
        ).count()

        # Check limits of user
        if player_type == 'main' and busy_hour_reservations + parent_busy_hour_reservations >= allowed_total_busy_hour_main_reservations:
            return False
        if player_type == 'reserve' and busy_hour_reservations + parent_busy_hour_reservations >= allowed_total_busy_hour_reserve_reservations:
            return False
    else:
        # if user is parent count children reservations
        sub_users_sql = User.objects.filter(parent=user)
        children_busy_hour_reservations = 0
        for sub_user in sub_users_sql:
            # Count reservations during busy hours for user
            children_busy_hour_reservations += Reservation.objects.filter(
                user=sub_user,
                match__start_time__gte=start_of_week,
                match__start_time__lt=end_of_week,
                player_type=player_type,
                match__start_time__hour__gte=17,  # Busy hours start at 5 PM
                match__end_time__hour__lte=20,  # Busy hours end at 8 PM
            ).count()

        # Check limits of user
        if player_type == 'main' and busy_hour_reservations + children_busy_hour_reservations >= allowed_total_busy_hour_main_reservations:
            return False
        if player_type == 'reserve' and busy_hour_reservations + children_busy_hour_reservations >= allowed_total_busy_hour_reserve_reservations:
            return False

    return True
