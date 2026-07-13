from django.shortcuts import render, redirect
from .models import Report
from .forms import ReportForm

def home(request):
    # Logika Simpan Laporan (Create)
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReportForm()

    # Logika Ambil Data (Read)
    reports = Report.objects.all().order_by('-created_at')
    
    return render(request, 'main_app/home.html', {
        'form': form, 
        'reports': reports
    }