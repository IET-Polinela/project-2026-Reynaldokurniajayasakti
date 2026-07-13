from rest_framework.routers import DefaultRouter
from .api_views import ReportViewSet

# Inisialisasi DefaultRouter
router = DefaultRouter()

# Registrasi ViewSet ke router dengan awalan rute 'report'
router.register(r'report', ReportViewSet, basename='report')

# URL patterns diambil otomatis dari router
urlpatterns = router.urls