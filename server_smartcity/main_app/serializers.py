from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
<<<<<<< HEAD
    # Field dari Lab 10 untuk menyembunyikan identitas asli pelapor demi privasi
    reporter = serializers.SerializerMethodField()
    
    # Tambahan Lab 12: Field kustom untuk memeriksa apakah user yang login adalah pelapor asli (Figure 2)
=======
    reporter = serializers.SerializerMethodField()
    reporter_name = serializers.SerializerMethodField()
>>>>>>> 31e81c5f218d5b12b030daaa72bfae2929b3dbf7
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id', 'title', 'category', 'description', 
<<<<<<< HEAD
            'location', 'status', 'reporter', 'is_owner', # Pastikan is_owner terdaftar di sini
=======
            'location', 'status', 'reporter', 'reporter_name', 'is_owner',
>>>>>>> 31e81c5f218d5b12b030daaa72bfae2929b3dbf7
            'created_at', 'updated_at'
        ]

    def get_reporter(self, obj):
<<<<<<< HEAD
        """
        Mengubah data keluaran field reporter menjadi string statis.
        Hal ini memastikan data privasi Citizen aman saat diakses via endpoint publik.
        """
        return "Warga Anonim"

    def get_is_owner(self, obj):
        """
        Tambahan Lab 12: Memeriksa jika request.user merupakan pelapor asli (Figure 2)
        """
=======
        return "Warga Anonim"

    def get_reporter_name(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated and obj.reporter == request.user:
            return obj.reporter.username if obj.reporter else 'Warga Anonim'
        return "Warga Anonim"

    def get_is_owner(self, obj):
>>>>>>> 31e81c5f218d5b12b030daaa72bfae2929b3dbf7
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            return obj.reporter == request.user
        return False