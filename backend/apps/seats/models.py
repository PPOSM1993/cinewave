from django.db import models

class Room(models.Model):
    ROOM_TYPES = (
        ('2D', '2D'),
        ('3D', '3D'),
        ('IMAX', 'IMAX'),
        ('4DX', '4DX'),
    )

    name = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()
    type = models.CharField(max_length=10, choices=ROOM_TYPES, default='2D')

    def __str__(self):
        return f"{self.name} ({self.type})"

    def total_seats(self):
        return self.seats.count()


class Seat(models.Model):
    STATUS_CHOICES = (
        ('available', 'Disponible'),
        ('reserved', 'Reservado'),
        ('sold', 'Vendido'),
        ('maintenance', 'En mantenimiento'),
    )

    room = models.ForeignKey(Room, related_name='seats', on_delete=models.CASCADE)
    row = models.CharField(max_length=5)
    number = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    is_vip = models.BooleanField(default=False)
    is_accessible = models.BooleanField(default=False)

    class Meta:
        unique_together = ('room', 'row', 'number')
        ordering = ['row', 'number']

    def __str__(self):
        vip = "VIP" if self.is_vip else ""
        accessible = "Accesible" if self.is_accessible else ""
        extra = f" ({vip} {accessible})".strip()
        return f"Fila {self.row} - Asiento {self.number}{extra}"
