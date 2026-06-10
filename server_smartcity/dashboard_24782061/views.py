from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from main_app.models import Report
from django.db.models import Count

class DashboardView(TemplateView):
    template_name = 'dashboard_24782061/dashboard.html'

def dashboard_data(request):
    # 1. Distribusi Status (untuk Pie/Doughnut Chart)
    status_counts = Report.objects.values('status').annotate(total=Count('status'))
    # Format: {'status': 'RESOLVED', 'total': 150}
    
    # 2. Distribusi Kategori (untuk Bar Chart)
    category_counts = Report.objects.values('category').annotate(total=Count('category'))
    
    # 3. Data untuk Tabel (5 Terakhir)
    recent_reported = list(Report.objects.filter(status='REPORTED').order_by('-id')[:5].values('title', 'category', 'status'))
    recent_resolved = list(Report.objects.filter(status='RESOLVED').order_by('-id')[:5].values('title', 'category', 'status'))

    data = {
        'status_labels': [item['status'] for item in status_counts],
        'status_data': [item['total'] for item in status_counts],
        'category_labels': [item['category'] for item in category_counts],
        'category_data': [item['total'] for item in category_counts],
        'recent_reported': recent_reported,
        'recent_resolved': recent_resolved,
    }
    
    return JsonResponse(data)