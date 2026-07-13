# main_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    
    # Ganti 'list/' menjadi 'reports/' agar sesuai dengan yang kamu ketik di browser
    path('reports/', views.ReportListView.as_view(), name='report_list'), 
    
    path('add/', views.HomeView.as_view(), name='report_create'), 
    path('report/<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('report/<int:pk>/edit/', views.ReportUpdateView.as_view(), name='report_edit'),
    path('report/<int:pk>/delete/', views.ReportDeleteView.as_view(), name='report_delete'),
    path('report/<int:pk>/status/', views.ReportUpdateStatusView.as_view(), name='update_status'),

    # URL Tambahan untuk Fetch API (Lab 7)
    path('search/', views.report_search, name='report_search'),
    path('api/detail/<int:pk>/', views.report_detail_api, name='report_detail_api'),
]