from django.shortcuts import render

def home(request):
    # Mengambil file home.html di dalam folder templates/main_app/ [cite: 30]
    return render(request, 'main_app/home.html')