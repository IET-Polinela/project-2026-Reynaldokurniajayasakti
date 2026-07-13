from django.test import TestCase
from django.urls import reverse
from django.http import Http404
from django.core.exceptions import PermissionDenied
import json
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from main_app.models import Report

# ─────────────────────────────────────────────────────────────────────────────
# PENJELASAN: get_user_model()
# ─────────────────────────────────────────────────────────────────────────────
# Django mendukung custom user model melalui setting AUTH_USER_MODEL.
# Pada proyek ini, user model kustom didefinisikan di usermanagement.User.
# Menggunakan get_user_model() memastikan kita selalu mereferensikan model
# user yang benar, bukan django.contrib.auth.models.User bawaan.
# ─────────────────────────────────────────────────────────────────────────────
User = get_user_model()

# =============================================================================
# ADDITIONAL TESTS FOR 100% STATEMENT COVERAGE
# =============================================================================

class SerializerAndModelCoverageTests(APITestCase):
    """
    Kelas pengujian tambahan untuk menaikkan coverage model dan serializer.
    """
    def setUp(self):
        self.warga = User.objects.create_user(
            username='warga_str_test',
            password='Password123!',
            is_admin=False
        )

    def test_report_model_str(self):
        """
        Menguji str(report) agar memanggil __str__ dan mengembalikan judul laporan.
        """
        report = Report.objects.create(
            title='Laporan Str Uji',
            category='Lainnya',
            description='Deskripsi',
            location='Lokasi',
            status='REPORTED',
            reporter=self.warga
        )
        self.assertEqual(str(report), 'Laporan Str Uji')

    def test_report_serializer_no_request_context(self):
        """
        Menguji serializer tanpa menyertakan request dalam context,
        sehingga is_owner mengembalikan False.
        """
        from main_app.serializers import ReportSerializer
        report = Report.objects.create(
            title='Laporan Serializer Uji',
            category='Lainnya',
            description='Deskripsi',
            location='Lokasi',
            status='REPORTED',
            reporter=self.warga
        )
        serializer = ReportSerializer(report, context={})
        self.assertFalse(serializer.data['is_owner'])
        self.assertEqual(serializer.data['reporter_name'], 'Warga Anonim')


class MainAppMonolithicViewsCoverageTests(TestCase):
    """Meng-cover alur view monolitik, pencarian, dan API non-DRF."""

    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin_mono',
            password='Password123!',
            is_admin=True,
            is_staff=True,
        )
        self.citizen = User.objects.create_user(
            username='citizen_mono',
            password='Password123!',
            is_admin=False,
            is_staff=False,
        )
        self.report = Report.objects.create(
            title='Laporan Monolitik Uji',
            category='Infrastruktur',
            description='Ada kerusakan infrastruktur.',
            location='Bandung',
            status='REPORTED',
            reporter=self.citizen,
        )

    def test_report_detail_api_valid(self):
        from main_app.views import report_detail_api
        from django.test import RequestFactory

        factory = RequestFactory()
        request = factory.get('/dummy-url/')
        response = report_detail_api(request, self.report.id)
        self.assertEqual(response.status_code, 200)

    def test_report_detail_api_invalid(self):
        from main_app.views import report_detail_api
        from django.test import RequestFactory

        factory = RequestFactory()
        request = factory.get('/dummy-url/')
        with self.assertRaises(Http404):
            report_detail_api(request, 99999)

    def test_report_search_unauthenticated(self):
        response = self.client.get(reverse('report_search') + '?q=Lampu')
        self.assertEqual(response.status_code, 200)

    def test_report_search_citizen(self):
        self.client.login(username='citizen_mono', password='Password123!')
        response = self.client.get(reverse('report_search') + '?q=Monolitik')
        self.assertEqual(response.status_code, 200)

    def test_report_search_admin(self):
        self.client.login(username='admin_mono', password='Password123!')
        response = self.client.get(reverse('report_search') + '?q=Monolitik')
        self.assertEqual(response.status_code, 200)

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/home.html')

    def test_report_list_view_unauthenticated(self):
        response = self.client.get(reverse('report_list'))
        self.assertEqual(response.status_code, 302)

    def test_report_list_view_citizen(self):
        self.client.login(username='citizen_mono', password='Password123!')
        response = self.client.get(reverse('report_list'))
        self.assertEqual(response.status_code, 302)

    def test_report_list_view_admin(self):
        self.client.login(username='admin_mono', password='Password123!')
        response = self.client.get(reverse('report_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/report_list.html')

    def test_report_create_view_unauthenticated(self):
        response = self.client.get(reverse('report_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/home.html')

    def test_report_create_view_citizen(self):
        self.client.login(username='citizen_mono', password='Password123!')
        response = self.client.get(reverse('report_create'))
        self.assertEqual(response.status_code, 200)

    def test_report_create_view_admin_get(self):
        self.client.login(username='admin_mono', password='Password123!')
        response = self.client.get(reverse('report_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/home.html')

    def test_report_create_view_admin_post_valid(self):
        self.client.login(username='admin_mono', password='Password123!')
        payload = {
            'title': 'Laporan Form Baru',
            'category': 'Infrastruktur',
            'description': 'Deskripsi baru.',
            'location': 'Jakarta',
        }
        response = self.client.post(reverse('report_create'), payload)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(Report.objects.filter(title='Laporan Form Baru').exists())

    def test_home_view_form_valid_citizen_denied(self):
        self.client.login(username='citizen_mono', password='Password123!')
        payload = {
            'title': 'Laporan Ditolak',
            'category': 'Infrastruktur',
            'description': 'Deskripsi',
            'location': 'Bandung',
        }
        response = self.client.post(reverse('report_create'), payload)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Report.objects.filter(title='Laporan Ditolak').exists())

    def test_report_detail_view_unauthenticated(self):
        response = self.client.get(reverse('report_detail', kwargs={'pk': self.report.id}))
        self.assertEqual(response.status_code, 302)

    def test_report_detail_view_citizen(self):
        self.client.login(username='citizen_mono', password='Password123!')
        response = self.client.get(reverse('report_detail', kwargs={'pk': self.report.id}))
        self.assertEqual(response.status_code, 200)

    def test_report_detail_view_admin(self):
        self.client.login(username='admin_mono', password='Password123!')
        response = self.client.get(reverse('report_detail', kwargs={'pk': self.report.id}))
        self.assertEqual(response.status_code, 200)

    def test_report_update_view_unauthenticated(self):
        response = self.client.get(reverse('report_edit', kwargs={'pk': self.report.id}))
        self.assertEqual(response.status_code, 302)

    def test_report_update_view_citizen(self):
        self.client.login(username='citizen_mono', password='Password123!')
        response = self.client.get(reverse('report_edit', kwargs={'pk': self.report.id}))
        self.assertEqual(response.status_code, 302)

    def test_report_update_view_admin_get(self):
        self.client.login(username='admin_mono', password='Password123!')
        response = self.client.get(reverse('report_edit', kwargs={'pk': self.report.id}))
        self.assertEqual(response.status_code, 200)

    def test_report_update_view_admin_post_valid(self):
        self.client.login(username='admin_mono', password='Password123!')
        payload = {
            'title': 'Laporan Terupdate Oleh Admin',
            'category': 'Infrastruktur',
            'description': 'Deskripsi terupdate.',
            'location': 'Jakarta',
        }
        response = self.client.post(reverse('report_edit', kwargs={'pk': self.report.id}), payload)
        self.assertEqual(response.status_code, 302)
        self.report.refresh_from_db()
        self.assertEqual(self.report.title, 'Laporan Terupdate Oleh Admin')

    def test_report_delete_view_unauthenticated(self):
        response = self.client.get(reverse('report_delete', kwargs={'pk': self.report.id}))
        self.assertEqual(response.status_code, 302)

    def test_report_delete_view_citizen(self):
        self.client.login(username='citizen_mono', password='Password123!')
        response = self.client.get(reverse('report_delete', kwargs={'pk': self.report.id}))
        self.assertEqual(response.status_code, 302)

    def test_report_delete_view_admin_get(self):
        self.client.login(username='admin_mono', password='Password123!')
        response = self.client.get(reverse('report_delete', kwargs={'pk': self.report.id}))
        self.assertEqual(response.status_code, 200)

    def test_report_delete_view_admin_post(self):
        self.client.login(username='admin_mono', password='Password123!')
        response = self.client.post(reverse('report_delete', kwargs={'pk': self.report.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Report.objects.filter(id=self.report.id).exists())

    def test_report_delete_view_direct_delete_method(self):
        from main_app.views import ReportDeleteView
        from django.test import RequestFactory
        from django.contrib.messages.storage.fallback import FallbackStorage

        factory = RequestFactory()
        request = factory.post(reverse('report_delete', kwargs={'pk': self.report.id}))
        request.user = self.admin
        setattr(request, 'session', {})
        messages_storage = FallbackStorage(request)
        setattr(request, '_messages', messages_storage)

        view = ReportDeleteView()
        view.setup(request, pk=self.report.id)
        response = view.delete(request)
        self.assertEqual(response.status_code, 302)

    def test_report_update_status_view_unauthenticated(self):
        response = self.client.post(reverse('update_status', kwargs={'pk': self.report.id}), {'status': 'VERIFIED'})
        self.assertEqual(response.status_code, 302)

    def test_report_update_status_view_citizen(self):
        self.client.login(username='citizen_mono', password='Password123!')
        response = self.client.post(reverse('update_status', kwargs={'pk': self.report.id}), {'status': 'VERIFIED'})
        self.assertEqual(response.status_code, 302)

    def test_report_api_list_authenticated_and_pagination(self):
        from main_app.views import report_api_list
        from django.test import RequestFactory

        factory = RequestFactory()
        request = factory.get('/api/report/?tab=feed')
        request.user = self.citizen
        response = report_api_list(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('results', data)

    def test_report_api_list_disable_pagination(self):
        from main_app.views import report_api_list
        from django.test import RequestFactory

        factory = RequestFactory()
        request = factory.get('/api/report/?disable_pagination=true')
        request.user = self.citizen
        response = report_api_list(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.content), list)