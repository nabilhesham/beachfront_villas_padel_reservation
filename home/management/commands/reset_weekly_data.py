# Django Imports
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from django.db import connection

# App Imports
from home.models import Match, Reservation

class Command(BaseCommand):
    help = 'Reset all matches and reservations at the start of each week'

    def handle(self, *args, **kwargs):
        try:
            self.stdout.write(self.style.SUCCESS(f'Running Reset Weekly Data'))

            # Check database connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                self.stdout.write(self.style.SUCCESS(f"Available tables: {tables}"))


            today = datetime.now().date()
            self.stdout.write(self.style.SUCCESS(f'today: {today}'))
            last_monday = today - timedelta(days=today.weekday())  # Get last Monday
            self.stdout.write(self.style.SUCCESS(f'last_monday: {last_monday}'))


            # Delete all reservations
            # Reservation.objects.all().delete()
            reservations = Reservation.objects.filter(
                match__start_time__date__lt=last_monday
            )
            reservations.delete()
            self.stdout.write(self.style.SUCCESS(f'{reservations.count()} reservations have been cleared.'))

            # Delete all matches
            # Match.objects.all().delete()
            matches = Match.objects.filter(
                start_time__date__lt=last_monday
            )
            matches.delete()
            self.stdout.write(self.style.SUCCESS(f'{matches.count()} matches have been cleared.'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error during reset DB: {str(e)}'))
