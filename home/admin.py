from django.contrib import admin
from .models import CustomUser, Match, Reservation


# class MatchAdmin(admin.ModelAdmin):
#     list_display = ('start_time', 'end_time', 'main_players_count', 'reserve_players_count')
#
#     def main_players_count(self, obj):
#         return obj.main_players.count()
#
#     def reserve_players_count(self, obj):
#         return obj.reserve_players.count()
#
# class ReservationAdmin(admin.ModelAdmin):
#     list_display = ('user', 'match', 'player_type', 'timestamp')
#
#
# admin.site.register(Match, MatchAdmin)
# admin.site.register(Reservation, ReservationAdmin)

admin.site.register(CustomUser)
admin.site.register(Match)
admin.site.register(Reservation)
