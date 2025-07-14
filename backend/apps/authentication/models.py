from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.utils import timezone


# =====================
# MANAGER PERSONALIZADO
# =====================

class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, rut=None, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un email.')
        if not username:
            raise ValueError('El usuario debe tener un username.')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            rut=rut,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, rut=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('accepted_terms', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('El superusuario debe tener is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, username, first_name, last_name, rut, password, **extra_fields)


# ===========================
# VALIDACIONES PERSONALIZADAS
# ===========================

rut_validator = RegexValidator(
    regex=r'^(\d{7,8})-([\dkK])$',
    message='El RUT debe tener el formato 12345678-5.'
)

phone_validator = RegexValidator(
    regex=r'^(?:\+?56)?(?:9\d{8})$',
    message='El teléfono debe ser un número válido chileno.'
)

# ==============
# MODELO USUARIO
# ==============

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('client', 'Cliente'),
        ('cashier', 'Cajero'),
        ('ticket_checker', 'Boletero'),
        ('staff', 'Personal'),
        ('admin', 'Administrador'),
    )

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    rut = models.CharField(max_length=20, unique=True, null=True, blank=True, validators=[rut_validator])
    phone = models.CharField(max_length=15, blank=True, null=True, validators=[phone_validator])
    birth_date = models.DateField(blank=True, null=True)
    accepted_terms = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')

    objects = UserManager()

    USERNAME_FIELD = 'username'  # Puedes cambiar a 'email' si prefieres
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username
