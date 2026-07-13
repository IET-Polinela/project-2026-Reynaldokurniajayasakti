from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination  # <-- TAMBAHAN LAB 12: Import Pagination
from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraftOrReadOnly
<<<<<<< HEAD
=======
from drf_spectacular.utils import extend_schema
>>>>>>> 31e81c5f218d5b12b030daaa72bfae2929b3dbf7

# =====================================================================
# TAMBAHAN LAB 12: Konfigurasi Server-Side Pagination (page_size = 10)
# =====================================================================
class ReportPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    pagination_class = ReportPagination  # <-- TAMBAHAN LAB 12: Daftarkan Paginasi Kustom

    def get_permissions(self):
        """
        Meng-override method get_permissions untuk membatasi akses endpoint (Lab 10):
        - Aksi Edit (update, partial_update) dan Hapus (destroy) menggunakan permission kustom.
        - Aksi List, Detail, dan Create dapat diakses oleh semua pengguna yang telah login.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerAndDraftOrReadOnly()]
        return [permissions.IsAuthenticated()]

    # =====================================================================
    # PERUBAHAN LAB 12: Server-Side Filtering & Sorting
    # =====================================================================
    def get_queryset(self):
        """
        Meng-override get_queryset untuk implementasi optimasi API (Lab 12):
        - Sorting: Otomatis mengurutkan data dari pembaruan terbaru (-updated_at).
        - Server Side Filtering: Memisahkan state data via parameter kueri URL (?tab=...)
        """
        user = self.request.user
        
        # Pengamanan jika user belum terautentikasi (fall-back)
        if not user.is_authenticated:
            return Report.objects.filter(status='PUBLISHED').order_by('-updated_at')

        # Ambil parameter ?tab= dari URL query string (default ke 'feed' jika kosong)
        tab = self.request.query_params.get('tab', 'feed')

        # Aturan Sorting Lab 12: Pastikan data dasar terurut dari yang terbaru berdasarkan waktu diperbarui
        base_queryset = Report.objects.all().order_by('-updated_at')

        # OPSI 1: Jika ?tab=my_reports -> Kembalikan HANYA laporan milik user yang sedang login
        if tab == 'my_reports':
            return base_queryset.filter(reporter=user)
        
        # OPSI 2: Jika ?tab=feed -> Kembalikan linimasa sosial publik (Feed Kota)
        elif tab == 'feed':
            # Aturan Admin: Sembunyikan semua yang berstatus DRAFT
            if user.is_staff:
                return base_queryset.exclude(status='DRAFT')
            
            # Aturan Citizen: Laporan warga lain yang BUKAN DRAFT + Laporan milik sendiri (termasuk drafnya)
            return (base_queryset.exclude(status='DRAFT').exclude(reporter=user) | base_queryset.filter(reporter=user)).distinct()

        return base_queryset

    def perform_create(self, serializer):
        """
        Meng-override perform_create agar identitas pelapor (reporter) diambil otomatis 
        dari pengguna yang sedang login (self.request.user) via JWT Token.
        """
        serializer.save(reporter=self.request.user)

    def update(self, request, *args, **kwargs):
<<<<<<< HEAD
        """
        Meng-override method update (Sesuai Aturan Baris 14 di Proyektor):
        - Admin ==> Cuma ngubah status aja (tidak boleh mengubah judul, deskripsi, dll).
        """
        instance = self.get_object()
        
        if request.user.is_staff:
            # Jika yang login adalah Admin, pastikan dia HANYA mengirimkan field 'status'
=======
        instance = self.get_object()

        if request.user.is_staff:
>>>>>>> 31e81c5f218d5b12b030daaa72bfae2929b3dbf7
            if 'status' in request.data and len(request.data) == 1:
                instance.status = request.data['status']
                instance.save()
                return Response({"message": "Status laporan berhasil diperbarui oleh Admin!"}, status=status.HTTP_200_OK)
<<<<<<< HEAD
            
=======

>>>>>>> 31e81c5f218d5b12b030daaa72bfae2929b3dbf7
            return Response(
                {"detail": "Gagal! Admin hanya diizinkan untuk mengubah 'status' laporan saja."},
                status=status.HTTP_400_BAD_REQUEST
            )
<<<<<<< HEAD
            
        # Jika yang login adalah Citizen pemilik laporan, jalankan proses update normal (PUT/PATCH)
        return super().update(request, *args, **kwargs)

    # === UPDATE FIX: PENGHAPUSAN LANGSUNG DAN VALIDASI DB ===
=======

        if instance.status == 'DRAFT' and instance.reporter == request.user and request.data.get('status') == 'REPORTED':
            instance.status = 'REPORTED'
            instance.save()
            return Response({"message": "Laporan berhasil diajukan!"}, status=status.HTTP_200_OK)

        return super().update(request, *args, **kwargs)

    # === UPDATE FIX: PENGHAPUSAN LANGSUNG DAN VALIDASI DB ===
    @extend_schema(exclude=True) 
>>>>>>> 31e81c5f218d5b12b030daaa72bfae2929b3dbf7
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
<<<<<<< HEAD
        )
=======
        )

>>>>>>> 31e81c5f218d5b12b030daaa72bfae2929b3dbf7
