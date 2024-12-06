# Django imports
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta, datetime
from django.utils.dateparse import parse_datetime
from django.contrib.auth import authenticate, login, update_session_auth_hash,logout
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

# general Imports
import json

# App imports
from .models import Match, Reservation
from .decorators import custom_login_required

############################# Auth Views ##########################################

def login_view(request):
    if request.user.is_authenticated:
        if request.user.default_password is False:
            return redirect('home')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                # Check if this is the first time the user is logging in
                login(request, user)
                if user.default_password:
                    messages.success(request, f"first time login please change your password!")
                    return redirect('change-password')
                messages.success(request, f"Welcome, {user.username}")
                return redirect('home')  # Redirect to home page after successful login
        else:
            # Add a non-field error if form is invalid
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'auth/login.html', {'form': form, 'user': request.user})


def change_password(request):
    if request.method == 'POST':
        # Here you would handle the logic to change the user's password
        # e.g., using `password_change` or `set_password` method
        new_password = request.POST.get('password')
        user = request.user
        user.set_password(new_password)
        user.default_password = False  # Set this to False once password is updated
        user.save()
        messages.success(request, "Your password has been updated.")
        return redirect('login')  # Redirect to login page after password change
    return render(request, 'auth/change_password.html', {'user': request.user})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


############################# App Views ##########################################

@custom_login_required
def home_view(request):
    return redirect('calendar')

def under_construction_view(request):
    return render(request, 'under_construction.html')

@custom_login_required
def calendar_view(request):
    return render(request, 'calendar.html', {'user': request.user})

############################# Data ##########################################

@custom_login_required
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
                'main_players': list(match.main_players.values_list('user__username', flat=True)),
                'reserve_players': list(match.reserve_players.values_list('user__username', flat=True)),
            })

        current_time = end_time

    return JsonResponse({'matches': matches})



@custom_login_required
def toggle_player_reservation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        match_start = data.get('match_start')
        match_end = data.get('match_end')
        player_type = data.get('player_type')
        user = request.user

        try:
            match_start = datetime.strptime(match_start, '%Y-%m-%dT%H:%M:%S')
            match_end = datetime.strptime(match_end, '%Y-%m-%dT%H:%M:%S')

            # Set minutes, seconds, and microseconds to zero
            match_start = match_start.replace(minute=0, second=0, microsecond=0)
            match_end = match_end.replace(minute=0, second=0, microsecond=0)

        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)


        # Find or create the match
        match, created = Match.objects.get_or_create(start_time=match_start, end_time=match_end)

        try:
            # Check if the user already has a reservation
            reservation = Reservation.objects.filter(user=user, match=match).first()
            if reservation:
                if reservation.player_type == player_type:
                    reservation.delete()  # Remove reservation
                else:
                    reservation.player_type = player_type
                    reservation.save()
            else:
                # Create a new reservation
                Reservation.objects.create(user=user, match=match, player_type=player_type)

            # Return updated player lists
            return JsonResponse({
                'main_players': list(match.main_players.values_list('user__username', flat=True)),
                'reserve_players': list(match.reserve_players.values_list('user__username', flat=True)),
            })

        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
