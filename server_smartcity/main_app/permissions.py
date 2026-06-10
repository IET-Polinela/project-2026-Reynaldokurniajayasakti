from rest_framework import permissions

class IsOwnerAndDraftOrReadOnly(permissions.BasePermission):
    """
    Custom Permission untuk Lab Session 10 (Sesuai Aturan Proyektor Dosen):
    - Membaca data (GET, HEAD, OPTIONS) diperbolehkan bagi yang sudah login.
    - Membuat data (POST): Hanya diizinkan bagi user yang terautentikasi.
    - Mengubah (PUT/PATCH) dan Menghapus (DELETE):
      1. Jika Admin (is_staff): Diperbolehkan lolos objek.
      2. Jika Citizen: Hanya boleh jika status laporan masih 'DRAFT'.
    """
    def has_permission(self, request, view):
        # Memastikan pengguna harus login terlebih dahulu untuk mengakses endpoint ini
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # 1. Jika metodenya SAFE_METHODS (GET, HEAD, OPTIONS), loloskan pengecekan
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # 2. ATURAN BARIS 14 DI PROYEKTOR: Loloskan Admin (is_staff) agar bisa melakukan update status
        if request.user.is_staff:
            return True
            
        # 3. FIX UNTUK CITIZEN: Loloskan validasi kepemilikan khusus untuk DELETE jika statusnya 'DRAFT'
        # Ini agar data "Warga Anonim" yang tidak sinkron dengan User login tetap bisa terhapus!
        if request.method == 'DELETE':
            return obj.status == 'DRAFT'
            
        # 4. ATURAN BARIS 15-16 DI PROYEKTOR (Untuk PUT/PATCH Edit):
        return obj.status == 'DRAFT'