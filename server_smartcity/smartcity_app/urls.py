from django.contrib import admin
from django.urls import path, include
<<<<<<< HEAD
from django.contrib.auth import views as auth_views
from usermanagement_24782061 import views as user_views 

# Import tambahan untuk MyLoginView dan MyLogoutView
from usermanagement_24782061.views import MyLoginView, MyLogoutView

# Import views bawaan SimpleJWT untuk Lab Session 10
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# KOREKSI IMPORT (Lab 10): Diarahkan langsung ke views.py, bukan api_views.py
from usermanagement_24782061.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    
=======

# IMPORT UTAMA USERMANAGEMENT: Digabungkan dalam satu baris agar rapi
from usermanagement_24782061 import views as user_views
from usermanagement_24782061.views import MyLoginView, MyLogoutView, RegisterView

# IMPORT DOCUMENTATION: OpenAPI 3.0 (Lab 14)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django_scalar.views import scalar_viewer

# IMPORT JWT: SimpleJWT Authentication (Lab 10)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

>>>>>>> 31e81c5f218d5b12b030daaa72bfae2929b3dbf7
    # --- AUTHENTICATION & REGISTRATION SYSTEM (LAB 6) ---
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('register/', user_views.register, name='register'),
    # ----------------------------------------------------

    # --- DRF BROWSABLE API AUTHENTICATION (Biar bisa login langsung di Browser) ---
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # --- API SYSTEM (LAB 9 & LAB 10) ---
<<<<<<< HEAD
    # Menghubungkan rute API dengan prefix 'api/'
    path('api/', include('main_app.api_urls')), 
    
    path('', include('main_app.urls')),           
    path('about/', include('about.urls')),        
    path('contacts/', include('contacts.urls')),  
    
    # --- DASHBOARD SYSTEM (LAB 7) ---
    path('dashboard/', include('dashboard_24782061.urls')), 
=======
    path('api/', include('main_app.api_urls')),

    # --- MONOLITHIC WEB ROUTES ---
    path('', include('main_app.urls')),
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),

    # --- DASHBOARD SYSTEM (LAB 7) ---
    path('dashboard/', include('dashboard_24782061.urls')),

    # --- OPENAPI DOCUMENTATION ENDPOINTS (LAB 14) ---
    # 1. Endpoint untuk meng-generate skema mentah (JSON/YAML)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # 2. Endpoint Swagger UI
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # 3. Endpoint Scalar UI
    path('api/docs/scalar/', scalar_viewer, name='scalar-ui'),
>>>>>>> 31e81c5f218d5b12b030daaa72bfae2929b3dbf7
]

# --- TAMBAHAN ENDPOINT AUTENTIKASI & REGISTRASI REST API (LAB SESSION 10) ---
urlpatterns += [
    # Endpoint Autentikasi REST API menggunakan JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
<<<<<<< HEAD
    
    # Endpoint Registrasi Akun Citizen via REST API (Terhubung ke views.py)
    path('api/register/', RegisterView.as_view(), name='api_register'),
]
=======

    # Endpoint Registrasi Akun Citizen via REST API (Terhubung ke views.py)
    path('api/register/', RegisterView.as_view(), name='api_register'),
]
>>>>>>> 31e81c5f218d5b12b030daaa72bfae2929b3dbf7
