from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView 
from .forms import CitizenRegistrationForm 

# --- IMPORT TAMBAHAN UNTUK REST API REGISTER (LAB SESSION 10) ---
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer

def register(request):
    if request.method == 'POST':
        form = CitizenRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Akun berhasil dibuat untuk {username}! Silakan login.')
            return redirect('login')
    else:
        form = CitizenRegistrationForm()
    return render(request, 'usermanagement_24782061/register.html', {'form': form})

# --- TAMBAHAN UNTUK FEEDBACK LOGIN & LOGOUT (NO 5) ---
class MyLoginView(LoginView):
    template_name = 'usermanagement_24782061/login.html'
    
    def form_valid(self, form):
        messages.success(self.request, f"Selamat datang {form.get_user().username}!")
        return super().form_valid(form)

class MyLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Anda telah berhasil keluar dari sistem.")
        return super().dispatch(request, *args, **kwargs)


# --- TAMBAHAN ENDPOINT REST API REGISTER CITIZEN (LAB SESSION 10) ---
class RegisterView(generics.CreateAPIView):
    """
    Endpoint API untuk Registrasi Akun Citizen via Postman/Frontend (Lab 10).
    Akses dibuka untuk umum (AllowAny) agar calon pengguna baru bisa mendaftar.
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(
                {"message": "Registrasi Akun Citizen Berhasil!"}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)