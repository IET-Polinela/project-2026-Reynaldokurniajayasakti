from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    # Field dari Lab 10 untuk menyembunyikan identitas asli pelapor demi privasi
    reporter = serializers.SerializerMethodField()
    
    # Tambahan Lab 12: Field kustom untuk memeriksa apakah user yang login adalah pelapor asli (Figure 2)
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id', 'title', 'category', 'description', 
            'location', 'status', 'reporter', 'is_owner', # Pastikan is_owner terdaftar di sini
            'created_at', 'updated_at'
        ]

    def get_reporter(self, obj):
        """
        Mengubah data keluaran field reporter menjadi string statis.
        Hal ini memastikan data privasi Citizen aman saat diakses via endpoint publik.
        """
        return "Warga Anonim"

    def get_is_owner(self, obj):
        """
        Tambahan Lab 12: Memeriksa jika request.user merupakan pelapor asli (Figure 2)
        """
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            return obj.reporter == request.user
        return False