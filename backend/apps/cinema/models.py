from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Género'
        verbose_name_plural = 'Géneros'

    def __str__(self):
        return self.name


class Format(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Ej: 2D, 3D, IMAX

    class Meta:
        verbose_name = 'Formato'
        verbose_name_plural = 'Formatos'

    def __str__(self):
        return self.name


class Movie(models.Model):
    CLASSIFICATION_CHOICES = [
        ('TE', 'Todo espectador'),
        ('7+', 'Mayores de 7 años'),
        ('14+', 'Mayores de 14 años'),
        ('18+', 'Mayores de 18 años'),
    ]

    title = models.CharField(max_length=200)
    synopsis = models.TextField()
    duration_minutes = models.PositiveIntegerField()
    classification = models.CharField(max_length=10, choices=CLASSIFICATION_CHOICES)
    poster = models.ImageField(upload_to='movies/posters/', blank=True, null=True)
    trailer_url = models.URLField(blank=True, null=True)
    director = models.CharField(max_length=200, blank=True, null=True)
    main_cast = models.TextField(blank=True, null=True, help_text='Lista separada por comas o JSON con actores.')
    production_company = models.CharField(max_length=200, blank=True, null=True)
    original_language = models.CharField(max_length=100, blank=True, null=True)
    expected_audience = models.PositiveIntegerField(blank=True, null=True, help_text='Número estimado de asistentes.')
    is_scheduled = models.BooleanField(default=True, help_text='Marca si será exhibida próximamente.')
    release_date = models.DateField()

    genres = models.ManyToManyField(Genre, related_name='movies')
    formats = models.ManyToManyField(Format, related_name='movies')

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Película'
        verbose_name_plural = 'Películas'
        ordering = ['-release_date']

    def __str__(self):
        return self.title
