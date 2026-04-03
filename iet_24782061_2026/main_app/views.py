from django.shortcuts import render, redirect
from .models import Report
from .forms import ReportForm

def home(request):
    # Logika Simpan (Create)
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReportForm()

    # Logika Tampilkan (Read)
    reports = Report.objects.all().order_by('-created_at')
    
    # Render ke home.html (gabungan Lab 2 & Lab 3)
    return render(request, 'main_app/home.html', {
        'form': form, 
        'reports': reports
    })

# Opsional: Jika kamu tetap ingin path /add/ sendiri, biarkan fungsi ini ada
def add_report(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReportForm()
    return render(request, 'main_app/home.html', {'form': form})