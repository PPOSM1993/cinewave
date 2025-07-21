from django.contrib import admin
from .models import Genre, Format, Movie


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Format)
class FormatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'classification', 'release_date', 'is_scheduled', 'is_active')
    list_filter = ('classification', 'is_scheduled', 'is_active', 'release_date')
    search_fields = ('title', 'director', 'production_company')
    autocomplete_fields = ('genres', 'formats')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Información Principal', {
            'fields': ('title', 'synopsis', 'duration_minutes', 'classification', 'poster', 'trailer_url')
        }),
        ('Detalles Técnicos', {
            'fields': ('director', 'main_cast', 'production_company', 'original_language')
        }),
        ('Datos Comerciales', {
            'fields': ('expected_audience', 'is_scheduled', 'release_date')
        }),
        ('Clasificación y Formato', {
            'fields': ('genres', 'formats')
        }),
        ('Estado y Tiempos', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )
