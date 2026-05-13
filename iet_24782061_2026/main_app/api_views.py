from rest_framework import viewsets, permissions
from .models import Report
from .serializers import ReportSerializer

class ReportViewSet(viewsets.ModelViewSet):
    # Mengizinkan akses tanpa autentikasi untuk keperluan praktikum
    permission_classes = [permissions.AllowAny]
    
    # Menentukan sumber data (semua objek Report)
    queryset = Report.objects.all()
    
    # Menentukan serializer yang digunakan untuk konversi data
    serializer_class = ReportSerializer