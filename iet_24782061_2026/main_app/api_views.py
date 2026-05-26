from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraftOrReadOnly

class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer

    def get_permissions(self):
        """
        Meng-override method get_permissions untuk membatasi akses endpoint (Lab 10):
        - Aksi Edit (update, partial_update) dan Hapus (destroy) menggunakan permission kustom.
        - Aksi List, Detail, dan Create dapat diakses oleh semua pengguna yang telah login.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerAndDraftOrReadOnly()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """
        Meng-override get_queryset untuk implementasi penyaringan data (Sesuai Aturan Proyektor):
        - BARIS 6: Admin ==> exclude DRAFT (Admin hanya melihat laporan yang sudah dipublikasikan/submit).
        - BARIS 7-8: Citizen ==> Melihat semua laporan berstatus 'PUBLISHED' + Laporan milik dia sendiri (walau masih DRAFT).
        """
        user = self.request.user
        
        # Pengamanan jika user belum terautentikasi (fall-back)
        if not user.is_authenticated:
            return Report.objects.filter(status='PUBLISHED')

        # ATURAN 1 (Admin): Sembunyikan semua yang berstatus DRAFT
        if user.is_staff:
            return Report.objects.exclude(status='DRAFT')

        # ATURAN 2 (Citizen): Laporan PUBLISHED umum + Laporan buatan sendiri.
        # Menambahkan .distinct() untuk mencegah duplikasi atau persistensi cache evaluasi query di MySQL
        return (Report.objects.filter(status='PUBLISHED') | Report.objects.filter(reporter=user)).distinct()

    def perform_create(self, serializer):
        """
        Meng-override perform_create agar identitas pelapor (reporter) diambil otomatis 
        dari pengguna yang sedang login (self.request.user) via JWT Token.
        """
        serializer.save(reporter=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        Meng-override method update (Sesuai Aturan Baris 14 di Proyektor):
        - Admin ==> Cuma ngubah status aja (tidak boleh mengubah judul, deskripsi, dll).
        """
        instance = self.get_object()
        
        if request.user.is_staff:
            # Jika yang login adalah Admin, pastikan dia HANYA mengirimkan field 'status'
            if 'status' in request.data and len(request.data) == 1:
                instance.status = request.data['status']
                instance.save()
                return Response({"message": "Status laporan berhasil diperbarui oleh Admin!"}, status=status.HTTP_200_OK)
            
            return Response(
                {"detail": "Gagal! Admin hanya diizinkan untuk mengubah 'status' laporan saja."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Jika yang login adalah Citizen pemilik laporan, jalankan proses update normal (PUT/PATCH)
        return super().update(request, *args, **kwargs)

    # === UPDATE FIX: PENGHAPUSAN LANGSUNG DAN VALIDASI DB ===
    def destroy(self, request, *args, **kwargs):
        """
        Meng-override method destroy untuk memaksa objek terhapus langsung dari database
        dan memastikan database melakukan commit instan sebelum merespons Postman.
        """
        instance = self.get_object()
        
        # Eksekusi penghapusan objek secara instan menggunakan standard model delete
        instance.delete()
        
        return Response(
            {"message": "Sukses! Laporan berstatus DRAFT telah dihapus permanen dari database."}, 
            status=status.HTTP_200_OK
        )