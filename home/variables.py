from datetime import time

# Sub Users
allowed_sub_users_count = 4

# No Match Variables
no_match_days_list = [5, 6]   # Saturday or Sunday
no_match_days_start_hour = time(9, 0)   # 9 AM
no_match_days_end_hour = time(10, 0)   # 10 AM

no_match_all_week_start_hour = time(13, 0)   # 1 PM
no_match_all_week_end_hour = time(15, 0)   # 3 PM

# Busy Hours Variables
busy_hour_start_hour = 17   # Busy hours start at 5 PM
busy_hour_start = time(busy_hour_start_hour, 0)
busy_hour_end_hour = 20     # Busy hours end at 8 PM
busy_hour_end = time(busy_hour_end_hour, 0)

allowed_user_busy_hour_main_reservations = 2
allowed_user_busy_hour_reserve_reservations = 2
allowed_total_busy_hour_main_reservations = 4
allowed_total_busy_hour_reserve_reservations = 4

# Calendar Variables
hours_to_display_data_in_calendar = 48
days_to_display_in_calendar = 3
minutes_before_match_reservation_close = 240
minutes_to_refresh_calendar_data = 5