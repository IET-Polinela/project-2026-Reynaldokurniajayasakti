from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from .models import Report
from .forms import ReportForm

<<<<<<< HEAD
# Tampilan Utama: Menampilkan Daftar Laporan + Form Input
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/home.html'
    context_object_name = 'reports'
    ordering = ['-created_at']

    # Agar form input muncul di atas daftar laporan (seperti di gambar UI-mu)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReportForm() 
        return context

# Proses Simpan: Menangani data yang dikirim dari form
class ReportCreateView(CreateView):
    model = Report
    form_class = ReportForm
    success_url = reverse_lazy('home') # Balik ke halaman utama setelah simpan

# View Pendukung CRUD (Syarat Lab 4) [cite: 172-175]
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'

class ReportUpdateView(UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/report_form.html'
    success_url = reverse_lazy('home')

class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'main_app/report_confirm_delete.html'
    success_url = reverse_lazy('home')

# View Khusus Update Status (Workflow) [cite: 181-189]
class ReportUpdateStatusView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')
        report.status = new_status
        report.save()
        return redirect('home')
=======
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
>>>>>>> ff11213bdda2ad49528308a98deb6e72e3fbd945
