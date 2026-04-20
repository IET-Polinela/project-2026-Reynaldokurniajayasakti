from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Report
from .forms import ReportForm

# 1. Halaman Home (Sambutan & Form Lapor)
class HomeView(CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/home.html' # Tambahkan main_app/
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil dikirim!")
        return super().form_valid(form)

# 2. Halaman Daftar Laporan (Tabel)
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/report_list.html' # Tambahkan main_app/
    context_object_name = 'reports'
    ordering = ['-created_at']

# 3. View Pendukung CRUD lainnya
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html' # Tambahkan main_app/

class ReportUpdateView(UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/add_report.html' # Sesuai nama file di folder kamu
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.info(self.request, "Laporan berhasil diperbarui!")
        return super().form_valid(form)

class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'main_app/report_confirm_delete.html' 
    success_url = reverse_lazy('report_list')

# 4. View Workflow Status
class ReportUpdateStatusView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        
        # Logika perubahan status otomatis (Workflow)
        if report.status == 'REPORTED':
            report.status = 'VERIFIED'
            status_label = "Diverifikasi"
        elif report.status == 'VERIFIED':
            report.status = 'IN_PROGRESS'
            status_label = "Diproses"
        elif report.status == 'IN_PROGRESS':
            report.status = 'RESOLVED'
            status_label = "Selesai"
        else:
            status_label = report.status

        report.save()
        messages.success(request, f"Laporan berhasil {status_label}!")
        return redirect('report_list')