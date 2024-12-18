# Django Imports
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta

# App Imports
from home.models.match import Match, Reservation

class Command(BaseCommand):
    help = 'Reset all matches and reservations at the start of each week'

    def handle(self, *args, **kwargs):
        try:
            today = datetime.now().date()
            last_monday = today - timedelta(days=today.weekday())  # Get last Monday


            # Delete all reservations
            # Reservation.objects.all().delete()
            Reservation.objects.filter(
                match__start_time__date__lt=last_monday
            ).delete()
            self.stdout.write(self.style.SUCCESS('All reservations have been cleared.'))

            # Delete all matches
            # Match.objects.all().delete()
            Match.objects.filter(
                start_time__date__lt=last_monday
            ).delete()
            self.stdout.write(self.style.SUCCESS('All matches have been cleared.'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error during reset: {str(e)}'))
