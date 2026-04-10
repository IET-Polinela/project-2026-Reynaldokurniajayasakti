from django.urls import path
from . import views

urlpatterns = [
    # Halaman Utama (Daftar Laporan)
    path('', views.ReportListView.as_view(), name='home'),
    
    # Proses Simpan Laporan
    path('add/', views.ReportCreateView.as_view(), name='add_report'),
    
    # Detail, Edit, dan Delete
    path('report/<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('report/<int:pk>/edit/', views.ReportUpdateView.as_view(), name='report_edit'),
    path('report/<int:pk>/delete/', views.ReportDeleteView.as_view(), name='report_delete'),
    
    # Workflow Status [cite: 190]
    path('report/<int:pk>/status/', views.ReportUpdateStatusView.as_view(), name='update_status'),
]