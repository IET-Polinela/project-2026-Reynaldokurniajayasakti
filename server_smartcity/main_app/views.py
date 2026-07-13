from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
<<<<<<< HEAD
from django.http import JsonResponse
=======
from django.http import JsonResponse, HttpResponseRedirect
>>>>>>> 31e81c5f218d5b12b030daaa72bfae2929b3dbf7
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ReportForm
from .models import Report

# ==========================================================
# 1. HALAMAN UTAMA (HOME)
# ==========================================================


<<<<<<< HEAD
class HomeView(LoginRequiredMixin, CreateView):
=======
class HomeView(CreateView):
>>>>>>> 31e81c5f218d5b12b030daaa72bfae2929b3dbf7
    model = Report
    form_class = ReportForm
    template_name = "main_app/home.html"
    success_url = reverse_lazy("home")

<<<<<<< HEAD
    def form_valid(self, form):
        # PROTEKSI: Hanya Admin yang bisa menyimpan laporan via standard view
=======
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            self.object = None
            return self.render_to_response(self.get_context_data())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            messages.error(self.request, "Silakan login terlebih dahulu.")
            return redirect("home")

>>>>>>> 31e81c5f218d5b12b030daaa72bfae2929b3dbf7
        if not self.request.user.is_admin:
            messages.error(
                self.request,
                "Akses Ditolak: Citizen hanya dapat memantau, tidak dapat membuat laporan baru.",
            )
            return redirect("home")

        messages.success(self.request, "Laporan berhasil dikirim!")
        return super().form_valid(form)


# ==========================================================
# 2. MANAJEMEN LAPORAN (LIST & DETAIL)
# ==========================================================


class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = "main_app/report_list.html"
    context_object_name = "reports"
    ordering = ["-created_at"]

<<<<<<< HEAD
    def get_queryset(self):
        # Optimasi select_related untuk mempercepat pembacaan data foreign key relasional
=======
    def dispatch(self, request, *args, **kwargs):
        forced_user = getattr(request, "_force_auth_user", None)
        if forced_user and getattr(forced_user, "is_authenticated", False):
            request.user = forced_user

        if not getattr(request.user, "is_authenticated", False):
            return redirect("login")
        if not getattr(request.user, "is_admin", False):
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
>>>>>>> 31e81c5f218d5b12b030daaa72bfae2929b3dbf7
        return super().get_queryset().select_related("reporter")


class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = "main_app/report_detail.html"

<<<<<<< HEAD
=======
    def dispatch(self, request, *args, **kwargs):
        forced_user = getattr(request, "_force_auth_user", None)
        if forced_user and getattr(forced_user, "is_authenticated", False):
            request.user = forced_user

        if not getattr(request.user, "is_authenticated", False):
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)

>>>>>>> 31e81c5f218d5b12b030daaa72bfae2929b3dbf7

# ==========================================================
# 3. OPERASI CRUD (HANYA ADMIN)
# ==========================================================


class ReportUpdateView(LoginRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = "main_app/add_report.html"
    success_url = reverse_lazy("report_list")

    def dispatch(self, request, *args, **kwargs):
<<<<<<< HEAD
        if not request.user.is_admin:
=======
        forced_user = getattr(request, "_force_auth_user", None)
        if forced_user and getattr(forced_user, "is_authenticated", False):
            request.user = forced_user

        if not getattr(request.user, "is_authenticated", False):
            return redirect("login")
        if not getattr(request.user, "is_admin", False):
>>>>>>> 31e81c5f218d5b12b030daaa72bfae2929b3dbf7
            messages.error(
                request, "Akses Ditolak: Hanya Admin yang dapat mengedit laporan."
            )
            return redirect("report_list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.info(self.request, "Laporan berhasil diperbarui!")
        return super().form_valid(form)


class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = Report
    template_name = "main_app/report_confirm_delete.html"
    success_url = reverse_lazy("report_list")

    def dispatch(self, request, *args, **kwargs):
<<<<<<< HEAD
        if not request.user.is_admin:
=======
        forced_user = getattr(request, "_force_auth_user", None)
        if forced_user and getattr(forced_user, "is_authenticated", False):
            request.user = forced_user

        if not getattr(request.user, "is_authenticated", False):
            return redirect("login")
        if not getattr(request.user, "is_admin", False):
>>>>>>> 31e81c5f218d5b12b030daaa72bfae2929b3dbf7
            messages.error(
                request, "Akses Ditolak: Hanya Admin yang dapat menghapus laporan."
            )
            return redirect("report_list")
        return super().dispatch(request, *args, **kwargs)


# ==========================================================
# 4. WORKFLOW & STATUS (HANYA ADMIN)
# ==========================================================


class ReportUpdateStatusView(LoginRequiredMixin, View):

    def post(self, request, pk):
        if not request.user.is_admin:
            messages.error(
                request, "Akses Ditolak: Hanya Admin yang dapat mengubah status."
            )
            return redirect("report_list")

        report = get_object_or_404(Report, pk=pk)
        current_status = (
            str(report.status).strip().upper() if report.status else ""
        )

<<<<<<< HEAD
        # Logika Perubahan Status (Workflow)
        if current_status == "REPORTED":
            report.status = "VERIFIED"
            label = "Diverifikasi"
        elif current_status == "VERIFIED":
            report.status = "IN_PROGRESS"
            label = "Diproses"
=======
        allowed_transitions = {
            "REPORTED": "VERIFIED",
            "VERIFIED": "IN_PROGRESS",
            "IN_PROGRESS": "RESOLVED",
        }

        if current_status in allowed_transitions:
            report.status = allowed_transitions[current_status]
            label = "Diverifikasi" if current_status == "REPORTED" else "Diproses" if current_status == "VERIFIED" else "Selesai"
>>>>>>> 31e81c5f218d5b12b030daaa72bfae2929b3dbf7
        else:
            report.status = "RESOLVED"
            label = "Selesai"

        report.save()
        messages.success(
            request, f"Laporan '{report.title}' berhasil {label}!"
        )
        return redirect("report_list")


# ==========================================================
# 5. API ENDPOINTS (UNTUK SPA / JAVASCRIPT APP)
# ==========================================================


def report_api_list(request):
    """Endpoint Utama /api/report/ untuk melayani SPA Antarmuka Dashboard (js/app.js)

    Mendukung filter tab, paginasi data, dan bypass global statistik sidebar.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    tab = request.GET.get("tab", "feed")
    disable_pagination = request.GET.get("disable_pagination", "false") == "true"

    # 1. Penyaringan Queryset Berdasarkan Tab + Optimasi kueri Join DB (select_related)
    if disable_pagination:
        # Jika dipanggil loadSummaryStats() sidebar, ambil semua data khusus milik user aktif 
        # (termasuk status DRAFT) tanpa terikat aturan tab agar rekap hitungan akurat
        queryset = Report.objects.filter(reporter=request.user).select_related("reporter")
    elif tab == "my_reports":
        queryset = Report.objects.filter(reporter=request.user).order_by("-updated_at").select_related("reporter")
    else:
        queryset = Report.objects.exclude(status="DRAFT").order_by("-created_at").select_related("reporter")

    # 2. Pemetaan data objek Django ke struktur List JSON
    reports_list = []
    for report in queryset:
        reports_list.append(
            {
                "id": report.id,
                "title": report.title,
                "category": report.category,
                "reporter": (
                    report.reporter.username
                    if hasattr(report.reporter, "username")
                    else str(report.reporter)
                ),
                "updated_at": (
                    report.updated_at.isoformat() if report.updated_at else None
                ),
                "description": report.description,
                "location": report.location,
                "status": str(report.status).upper(),
                "is_owner": report.reporter == request.user,
            }
        )

    # 3. KONDISI BYPASS PAGINASI: Jika dipanggil oleh loadSummaryStats() sidebar
    if disable_pagination:
        return JsonResponse(reports_list, safe=False)

    # 4. KONDISI PAGINASI NORMAL (Default): Digunakan untuk Feed utama kartu laporan
    page_number = request.GET.get("page", 1)
    paginator = Paginator(reports_list, 10)  # Batasi 10 item per halaman

    try:
        page_obj = paginator.get_page(page_number)
        data_res = {"count": paginator.count, "results": list(page_obj)}
    except Exception:
        data_res = {"count": 0, "results": []}

    return JsonResponse(data_res)


def report_search(request):
    """Fitur Live Search"""
    query = request.GET.get("q", "")
    # Batasi field pencarian menggunakan .values() demi menghemat RAM server
    reports = Report.objects.filter(title__icontains=query).values(
        "id", "title", "category", "status"
    )[:10]
    return JsonResponse({"reports": list(reports)})


def report_detail_api(request, pk):
    """Fitur Detail Modal via AJAX"""
    report = get_object_or_404(Report, pk=pk)
    data = {
        "title": report.title,
        "category": report.category,
        "description": report.description,
        "location": report.location,
        "status": str(report.status).upper(),
    }
    return JsonResponse(data)