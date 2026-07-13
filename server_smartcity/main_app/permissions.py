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
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff:
            return True

        if request.method == 'DELETE':
            return obj.status == 'DRAFT' and obj.reporter == request.user

        if obj.status == 'DRAFT' and obj.reporter == request.user:
            return True

        return False