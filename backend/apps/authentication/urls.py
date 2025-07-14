from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileDetailView.as_view(), name='profile'),
    path('activate/<uidb64>/<token>/', ConfirmEmailView.as_view(), name='confirm-email'),
    path('resend-activation/', ResendActivationEmailView.as_view(), name='resend-activation'),
    path('check-availability/', CheckAvailabilityView.as_view(), name='check-availability'),
    path('request-reset-password/', RequestPasswordResetView.as_view(), name='request-reset-password'),
    path('reset-password-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
