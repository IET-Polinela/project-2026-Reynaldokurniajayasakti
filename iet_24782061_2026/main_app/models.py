from django.db import models

# 1. Konstanta STATUS_CHOICES
STATUS_CHOICES = [
    ('REPORTED', 'Reported'),
    ('VERIFIED', 'Verified'),
    ('IN_PROGRESS', 'In Progress'),
    ('RESOLVED', 'Resolved'),
]

# 2. Gabungkan semua ke dalam SATU class Report
class Report(models.Model):
    # Pindahkan CATEGORY_CHOICES ke sini
    CATEGORY_CHOICES = [
        ('Infrastruktur', 'Infrastruktur'),
        ('Keamanan', 'Keamanan'),
        ('Kesehatan', 'Kesehatan'),
        ('Lainnya', 'Lainnya'),
    ]

    title = models.CharField(max_length=200)
    
    # Pastikan category menggunakan choices=CATEGORY_CHOICES
    category = models.CharField(
        max_length=100, 
        choices=CATEGORY_CHOICES, 
        default='Lainnya'
    )
    
    description = models.TextField()
    location = models.CharField(max_length=200)
    
    # Field status yang sudah benar
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='REPORTED'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title