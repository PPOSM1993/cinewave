from rest_framework import serializers
from .models import Genre, Format, Movie
from datetime import date


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = ['id', 'name']


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    formats = FormatSerializer(many=True, read_only=True)

    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        write_only=True,
        source='genres'
    )

    format_ids = serializers.PrimaryKeyRelatedField(
        queryset=Format.objects.all(),
        many=True,
        write_only=True,
        source='formats'
    )

    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'synopsis',
            'duration_minutes',
            'classification',
            'poster',
            'trailer_url',
            'director',
            'main_cast',
            'production_company',
            'original_language',
            'expected_audience',
            'is_scheduled',
            'release_date',
            'genres',
            'formats',
            'genre_ids',
            'format_ids',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        if attrs.get('duration_minutes', 0) < 30:
            raise serializers.ValidationError({
                "duration_minutes": "La duración mínima debe ser de 30 minutos."
            })

        release_date = attrs.get('release_date')
        if release_date and release_date > date.today().replace(year=date.today().year + 5):
            raise serializers.ValidationError({
                "release_date": "La fecha de estreno es demasiado lejana."
            })

        trailer = attrs.get('trailer_url', '')
        if trailer and not ('youtube.com' in trailer or 'vimeo.com' in trailer):
            raise serializers.ValidationError({
                "trailer_url": "El trailer debe ser un enlace de YouTube o Vimeo."
            })

        return attrs

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
