from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin 
from .models import Report
from .forms import ReportForm

# 1. Halaman Home
class HomeView(LoginRequiredMixin, CreateView): 
    model = Report
    form_class = ReportForm
    template_name = 'main_app/home.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        # Citizen diizinkan masuk ke halaman Home (render template)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # PROTEKSI: Jika bukan admin, jangan simpan laporan
        if not self.request.user.is_admin:
            messages.error(self.request, "Akses Ditolak: Citizen hanya diizinkan memantau, tidak dapat membuat laporan baru.")
            return redirect('home')
            
        messages.success(self.request, "Laporan berhasil dikirim!")
        return super().form_valid(form)

# 2. Halaman Daftar Laporan
class ReportListView(LoginRequiredMixin, ListView): 
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'
    ordering = ['-created_at']

# 3. View CRUD dengan Proteksi Otorisasi (Hanya Admin)
class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'

class ReportUpdateView(LoginRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, "Akses Ditolak: Hanya Admin yang dapat mengedit laporan.")
            return redirect('report_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.info(self.request, "Laporan berhasil diperbarui!")
        return super().form_valid(form)

class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = Report
    template_name = 'main_app/report_confirm_delete.html' 
    success_url = reverse_lazy('report_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, "Akses Ditolak: Hanya Admin yang dapat menghapus laporan.")
            return redirect('report_list')
        return super().dispatch(request, *args, **kwargs)

# 4. View Workflow Status (Hanya Admin)
class ReportUpdateStatusView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, "Akses Ditolak: Hanya Admin yang dapat mengubah status.")
            return redirect('report_list')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
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