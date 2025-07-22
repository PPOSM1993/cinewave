from django.db import models
from django.utils.crypto import get_random_string
from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files import File
from django.core.validators import MinValueValidator

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('used', 'Usado'),
        ('cancelled', 'Cancelado'),
    ]

    ticket_code = models.CharField(max_length=12, unique=True, editable=False, db_index=True)
    qr_code = models.ImageField(upload_to='tickets/qrcodes/', blank=True, null=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    movie = models.ForeignKey('cinema.Movie', on_delete=models.CASCADE, related_name='tickets')
    room = models.ForeignKey('seats.Room', on_delete=models.CASCADE, related_name='tickets')
    seat = models.ForeignKey('seats.Seat', on_delete=models.CASCADE, related_name='tickets')

    show_date = models.DateField(db_index=True)
    show_time = models.TimeField()

    purchase_datetime = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def save(self, *args, **kwargs):
        if not self.ticket_code:
            self.ticket_code = get_random_string(length=12).upper()
        super().save(*args, **kwargs)  # Guarda primero

        if not self.qr_code:
            self.generate_qr_code()
            super().save(update_fields=['qr_code'])  # Actualiza solo el campo qr_code


    def generate_qr_code(self):
        qr_data = f'{self.ticket_code}'
        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer)
        self.qr_code.save(f'{self.ticket_code}.png', File(buffer), save=False)
        self.save()

    def __str__(self):
        return f'Ticket {self.ticket_code} - {self.user.username}'

