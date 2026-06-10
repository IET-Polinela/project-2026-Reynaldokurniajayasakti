from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CitizenRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email'] # Tambahkan field lain jika perlu

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = False  # Memastikan setiap yang daftar lewat sini adalah Citizen
        if commit:
            user.save()
        return user