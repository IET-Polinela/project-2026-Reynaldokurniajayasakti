from django.urls import path
from . import views # Mengambil fungsi dari views.py di folder yang sama [cite: 19]

urlpatterns = [
    path('', views.home, name='home'), # Menghubungkan URL kosong ke fungsi home [cite: 21]
]