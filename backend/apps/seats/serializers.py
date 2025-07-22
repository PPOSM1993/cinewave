from rest_framework import serializers
from .models import Room, Seat


class RoomSerializer(serializers.ModelSerializer):
    total_seats = serializers.IntegerField(read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'name', 'capacity', 'type', 'total_seats']

    def validate_capacity(self, value):
        if value <= 0:
            raise serializers.ValidationError("La capacidad debe ser un número positivo.")
        return value


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = [
            'id',
            'room',
            'row',
            'number',
            'status',
            'is_vip',
            'is_accessible'
        ]

    def validate(self, attrs):
        room = attrs.get('room')
        row = attrs.get('row')
        number = attrs.get('number')

        if Seat.objects.filter(room=room, row=row, number=number).exists():
            raise serializers.ValidationError(
                f"Ya existe un asiento en fila {row} y número {number} en la sala seleccionada."
            )
        return attrs

    def validate_number(self, value):
        if value <= 0:
            raise serializers.ValidationError("El número del asiento debe ser mayor a 0.")
        return value

    def validate_row(self, value):
        if not value.strip():
            raise serializers.ValidationError("La fila no puede estar vacía.")
        return value
