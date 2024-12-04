from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Match(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f'Match from {self.start_time} to {self.end_time}'


    @property
    def main_players(self):
        return self.reservations.filter(player_type='main')

    @property
    def main_players_count(self):
        return self.reservations.filter(player_type='main').count()


    @property
    def reserve_players(self):
        return self.reservations.filter(player_type='reserve')

    @property
    def reserve_players_count(self):
        return self.reservations.filter(player_type='reserve').count()

    @property
    def is_main_players_full(self):
        return self.main_players_count >= 4

    @property
    def is_reserve_players_full(self):
        return self.reserve_players_count >= 4


class Reservation(models.Model):
    PLAYER_TYPE_CHOICES = (
        ('main', 'Main Player'),
        ('reserve', 'Reserve Player'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="reservations")
    player_type = models.CharField(max_length=10, choices=PLAYER_TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'match')  # A user can only reserve once per match

    def clean(self):
        # Check that main players do not exceed 4
        if self.player_type == 'main' and self.match.main_players_count >= 4:
            raise ValidationError("Main players for this match are already full.")

        # Check that reserve players do not exceed 4
        if self.player_type == 'reserve' and self.match.reserve_players_count >= 4:
            raise ValidationError("Reserve players for this match are already full.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} reserved for {self.match}'
