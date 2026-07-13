from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from main_app.models import Report

User = get_user_model()


class ReportAPIAndViewTests(APITestCase):
    """Pengujian tambahan untuk API report dan view monolitik."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='citizen_modul4',
            password='Password123!',
            is_admin=False,
        )
        self.admin = User.objects.create_user(
            username='admin_modul4',
            password='Password123!',
            is_admin=True,
            is_staff=True,
        )
        self.report = Report.objects.create(
            title='Laporan Modul 4',
            category='Infrastruktur',
            description='Deskripsi uji',
            location='Lokasi uji',
            status='REPORTED',
            reporter=self.user,
        )

    def test_api_list_requires_authentication(self):
        response = self.client.get('/api/report/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_list_for_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/report/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_api_detail_returns_report(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/report/{self.report.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.report.title)

    def test_admin_can_update_status_via_api(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            f'/api/report/{self.report.pk}/',
            {'status': 'VERIFIED'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.report.refresh_from_db()
        self.assertEqual(self.report.status, 'VERIFIED')


class MonolithicViewAccessTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin_view',
            password='Password123!',
            is_admin=True,
            is_staff=True,
        )
        self.user = User.objects.create_user(
            username='citizen_view',
            password='Password123!',
            is_admin=False,
        )

    def test_home_page_is_accessible(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_admin_can_access_report_list(self):
        self.client.login(username='admin_view', password='Password123!')
        response = self.client.get(reverse('report_list'))
        self.assertEqual(response.status_code, 200)
