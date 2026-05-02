from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from .models import Report
from .forms import ReportForm

# ==========================================================
# 1. HALAMAN UTAMA (HOME)
# ==========================================================

class HomeView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/home.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # PROTEKSI: Hanya Admin yang bisa menyimpan laporan (Create)
        if not self.request.user.is_admin:
            messages.error(
                self.request, 
                "Akses Ditolak: Citizen hanya dapat memantau, tidak dapat membuat laporan baru."
            )
            return redirect('home')
            
        messages.success(self.request, "Laporan berhasil dikirim!")
        return super().form_valid(form)


# ==========================================================
# 2. MANAJEMEN LAPORAN (LIST & DETAIL)
# ==========================================================

class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'
    ordering = ['-created_at']


class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'


# ==========================================================
# 3. OPERASI CRUD (HANYA ADMIN)
# ==========================================================

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


# ==========================================================
# 4. WORKFLOW & STATUS (HANYA ADMIN)
# ==========================================================

class ReportUpdateStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not request.user.is_admin:
            messages.error(request, "Akses Ditolak: Hanya Admin yang dapat mengubah status.")
            return redirect('report_list')

        report = get_object_or_404(Report, pk=pk)
        current_status = str(report.status).strip().upper() if report.status else ""

        # Logika Perubahan Status (Workflow)
        if current_status == 'REPORTED':
            report.status = 'VERIFIED'
            label = "Diverifikasi"
        elif current_status == 'VERIFIED':
            report.status = 'IN_PROGRESS'
            label = "Diproses"
        else:
            report.status = 'RESOLVED'
            label = "Selesai"

        report.save()
        messages.success(request, f"Laporan '{report.title}' berhasil {label}!")
        return redirect('report_list')


# ==========================================================
# 5. API ENDPOINTS (UNTUK JAVASCRIPT / LAB 7)
# ==========================================================

def report_search(request):
    """Fitur Live Search"""
    query = request.GET.get('q', '')
    reports = Report.objects.filter(title__icontains=query).values(
        'id', 'title', 'category', 'status'
    )[:10]
    return JsonResponse({'reports': list(reports)})


def report_detail_api(request, pk):
    """Fitur Detail Modal via AJAX"""
    report = get_object_or_404(Report, pk=pk)
    data = {
        'title': report.title,
        'category': report.category,
        'description': report.description,
        'location': report.location,
        'status': report.status,
    }
    return JsonResponse(data)