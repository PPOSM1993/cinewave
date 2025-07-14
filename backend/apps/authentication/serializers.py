from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


# ========================
# SERIALIZER: REGISTRO
# ========================

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True, required=True,
        style={'input_type': 'password'},
        label="Confirmar contraseña"
    )

    class Meta:
        model = User
        fields = [
            'email', 'username', 'first_name', 'last_name',
            'rut', 'phone', 'birth_date', 'accepted_terms',
            'password', 'password2'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        if not attrs.get("accepted_terms"):
            raise serializers.ValidationError({"accepted_terms": "Debes aceptar los términos y condiciones."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


# ========================
# SERIALIZER: LOGIN CUSTOM
# ========================

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        identifier = attrs.get("username")  # Puede ser email, username o rut
        password = attrs.get("password")

        user = None
        for field in ['email', 'username', 'rut']:
            try:
                user = User.objects.get(**{field: identifier})
                break
            except User.DoesNotExist:
                continue

        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Usuario o contraseña incorrectos.")
        if not user.is_active:
            raise serializers.ValidationError("El usuario está inactivo.")

        # JWT requiere username, pero validamos por cualquier campo
        data = super().validate({'username': user.email, 'password': password})
        data['user'] = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "rut": user.rut,
            "role": user.role,
        }
        return data


# ========================
# SERIALIZER: PERFIL
# ========================

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'rut', 'phone', 'birth_date', 'accepted_terms',
            'is_active', 'is_staff', 'date_joined', 'role'
        ]
        read_only_fields = ['is_active', 'is_staff', 'date_joined', 'role']


# ========================
# SERIALIZER: ACTUALIZAR PERFIL
# ========================

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'birth_date']


# ========================
# SERIALIZER: CAMBIO CONTRASEÑA
# ========================

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({"old_password": "Contraseña actual incorrecta."})
        return attrs
