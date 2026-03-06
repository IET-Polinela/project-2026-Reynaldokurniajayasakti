from django.contrib import admin
from django.urls import path
from django.http import HttpResponse # Import ini diperlukan untuk mengirim teks ke browser

# Fungsi View sederhana
def welcome_view(request):
    return HttpResponse("Selamat Datang")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('welcome/', welcome_view), # Menambahkan path /welcome
]