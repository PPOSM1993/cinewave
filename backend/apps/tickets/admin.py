from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_code', 'user', 'movie', 'show_date', 'show_time', 'status', 'price')
    list_filter = ('status', 'show_date', 'movie')
    search_fields = ('ticket_code', 'user__username', 'movie__title')
    ordering = ('-purchase_datetime',)
    readonly_fields = ('ticket_code', 'qr_code', 'purchase_datetime')

    fieldsets = (
        ('Información General', {
            'fields': ('ticket_code', 'user', 'movie', 'room', 'seat')
        }),
        ('Función', {
            'fields': ('show_date', 'show_time', 'price', 'status')
        }),
        ('Código QR', {
            'fields': ('qr_code',)
        }),
        ('Auditoría', {
            'fields': ('purchase_datetime',)
        }),
    )
