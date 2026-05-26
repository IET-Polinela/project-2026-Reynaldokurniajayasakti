from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    # Menggunakan SerializerMethodField untuk menyembunyikan identitas asli pelapor demi privasi (Lab 10)
    reporter = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id', 'title', 'category', 'description', 
            'location', 'status', 'reporter', 
            'created_at', 'updated_at'
        ]

    def get_reporter(self, obj):
        """
        Mengubah data keluaran field reporter menjadi string statis.
        Hal ini memastikan data privasi Citizen aman saat diakses via endpoint publik.
        """
        return "Warga Anonim"