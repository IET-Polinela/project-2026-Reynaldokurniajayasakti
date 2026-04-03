from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Jika kamu pakai satu halaman saja, baris di bawah ini sebenarnya tidak wajib, 
    # tapi biarkan saja agar error attribute tadi hilang.
    path('add/', views.add_report, name='add_report'), 
]