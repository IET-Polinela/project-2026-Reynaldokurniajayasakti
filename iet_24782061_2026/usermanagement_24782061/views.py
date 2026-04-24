from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView # Tambahan untuk Feedback
# Tambahkan baris import di bawah ini:
from .forms import CitizenRegistrationForm 

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
