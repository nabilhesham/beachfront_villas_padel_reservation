# Django Imports
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import time
import psycopg2
from django.db import connection
from django.db.utils import OperationalError
import os
import django

# App Imports
from home.models import Match, Reservation

class Command(BaseCommand):
    help = 'Reset all matches and reservations at the start of each week'

    def check_db_connection(self):
        """Attempt to connect to the database and retry if needed."""
        retries = 5
        for i in range(retries):
            try:
                connection.ensure_connection()  # Check if the DB connection is available
                self.stdout.write(self.style.SUCCESS('Database connection established.'))
                return True
            except OperationalError as e:
                self.stderr.write(self.style.ERROR(f'Database is not ready yet: {e}'))
                if i < retries - 1:
                    self.stdout.write(self.style.WARNING(f'Retrying to connect to the database... ({i + 1}/{retries})'))
                    time.sleep(5)  # Wait 5 seconds before retrying
                else:
                    self.stderr.write(self.style.ERROR('Failed to connect to the database after retries. Exiting.'))
                    return False


    def handle(self, *args, **kwargs):
        try:
            self.stdout.write(self.style.SUCCESS(f'Running Reset Weekly Data'))
            if not self.check_db_connection():
                return  # Exit early if the database is not ready

            today = datetime.now().date()
            self.stdout.write(self.style.SUCCESS(f'today: {today}'))
            # Calculate the Monday of the current week
            start_of_week = today - timedelta(days=today.weekday())
            self.stdout.write(self.style.SUCCESS(f'start_of_week: {start_of_week}'))


            # Delete all reservations
            # Reservation.objects.all().delete()
            reservations = Reservation.objects.filter(
                match__start_time__date__lt=start_of_week
            )
            reservations.delete()
            self.stdout.write(self.style.SUCCESS(f'{reservations.count()} reservations have been cleared.'))

            # Delete all matches
            # Match.objects.all().delete()
            matches = Match.objects.filter(
                start_time__date__lt=start_of_week
            )
            matches.delete()
            self.stdout.write(self.style.SUCCESS(f'{matches.count()} matches have been cleared.'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error during reset DB: {str(e)}'))
