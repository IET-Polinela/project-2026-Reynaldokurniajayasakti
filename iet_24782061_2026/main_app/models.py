from django.db import models
from django.conf import settings # Diperlukan untuk relasi ke Custom User Model

# 1. Konstanta STATUS_CHOICES
# Menambahkan nilai "DRAFT" sesuai instruksi Lab 9 [cite: 30, 40]
STATUS_CHOICES = [
    ('DRAFT', 'Draft'),
    ('REPORTED', 'Reported'),
    ('VERIFIED', 'Verified'),
    ('IN_PROGRESS', 'In Progress'),
    ('RESOLVED', 'Resolved'),
]

# 2. Class Report
class Report(models.Model):
    CATEGORY_CHOICES = [
        ('Infrastruktur', 'Infrastruktur'),
        ('Keamanan', 'Keamanan'),
        ('Kesehatan', 'Kesehatan'),
        ('Lainnya', 'Lainnya'),
    ]

    title = models.CharField(max_length=200)
    
    category = models.CharField(
        max_length=100, 
        choices=CATEGORY_CHOICES, 
        default='Lainnya'
    )
    
    description = models.TextField()
    location = models.CharField(max_length=200)

    # Tambahkan field reporter berupa ForeignKey ke CustomUser [cite: 31, 50, 51]
    # Menggunakan settings.AUTH_USER_MODEL agar sesuai dengan konfigurasi di settings.py [cite: 31, 52]
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports',
        null=True,
        blank=True
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='REPORTED'
    )
    
    # Menambahkan field created_at dan updated_at [cite: 33, 64, 65]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title