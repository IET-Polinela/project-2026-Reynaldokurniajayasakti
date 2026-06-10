# main_app/admin.py
from django.contrib import admin
from .models import User # Sesuaikan dengan nama model user kamu

class UserAdmin(admin.ModelAdmin):
    # Kolom yang akan muncul di daftar user admin panel
    list_display = ('username', 'email', 'is_admin', 'is_staff', 'is_active')
    list_filter = ('is_admin', 'is_staff')

admin.site.register(User, UserAdmin)