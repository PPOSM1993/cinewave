from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    seat_number = serializers.CharField(source='seat.number', read_only=True)
    room_name = serializers.CharField(source='room.name', read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id',
            'ticket_code',
            'qr_code',
            'user',
            'movie',
            'movie_title',
            'room',
            'room_name',
            'seat',
            'seat_number',
            'show_date',
            'show_time',
            'purchase_datetime',
            'price',
            'status',
        ]
        read_only_fields = ['ticket_code', 'qr_code', 'purchase_datetime']

    def validate(self, data):
        user = self.context['request'].user
        movie = data.get('movie')
        room = data.get('room')
        seat = data.get('seat')
        show_date = data.get('show_date')
        show_time = data.get('show_time')

        # Validar que la butaca pertenezca a la sala
        if seat.room != room:
            raise serializers.ValidationError("La butaca seleccionada no pertenece a la sala indicada.")

        # Validar que el mismo usuario no tenga un ticket duplicado en esa función
        if Ticket.objects.filter(
            user=user,
            seat=seat,
            show_date=show_date,
            show_time=show_time,
            status='active'
        ).exists():
            raise serializers.ValidationError("Ya tienes un ticket activo para esa butaca, fecha y hora.")

        return data
