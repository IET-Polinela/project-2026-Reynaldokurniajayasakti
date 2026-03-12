from django.contrib import admin
from django.urls import path, include # Pastikan 'include' sudah diimpor [cite: 23]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),      # Mengarahkan halaman utama ke main_app 
    path('about/', include('about.urls')),    # Mengarahkan /about/ ke app about [cite: 38]
    path('contacts/', include('contacts.urls')), # Mengarahkan /contacts/ ke app contacts [cite: 38]
]