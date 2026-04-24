from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from usermanagement_24782061 import views as user_views 
# Import tambahan untuk MyLoginView dan MyLogoutView
from usermanagement_24782061.views import MyLoginView, MyLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- AUTHENTICATION & REGISTRATION SYSTEM (LAB 6) ---
    # Menggunakan MyLoginView dan MyLogoutView agar muncul pesan "Selamat Datang" dan "Berhasil Keluar"
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    
    path('register/', user_views.register, name='register'),
    # ----------------------------------------------------

    path('', include('main_app.urls')),           
    path('about/', include('about.urls')),        
    path('contacts/', include('contacts.urls')),  
]