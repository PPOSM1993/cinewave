from django.contrib import admin
from .models import Room, Seat


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'capacity', 'total_seats')
    search_fields = ('name',)
    list_filter = ('type',)

    def total_seats(self, obj):
        return obj.total_seats()
    total_seats.short_description = 'Butacas totales'


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('room', 'row', 'number', 'status', 'is_vip', 'is_accessible')
    list_filter = ('room', 'status', 'is_vip', 'is_accessible')
    search_fields = ('row', 'number')
    ordering = ('room', 'row', 'number')
