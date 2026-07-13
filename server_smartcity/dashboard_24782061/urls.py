from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard_home'),
    path('api/stats/', views.dashboard_data, name='dashboard_api'),
]