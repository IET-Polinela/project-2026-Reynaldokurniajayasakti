from django.db import models

# 1. Tambahkan konstanta STATUS_CHOICES di atas class [cite: 151]
STATUS_CHOICES = [
    ('REPORTED', 'Reported'),
    ('VERIFIED', 'Verified'),
    ('IN_PROGRESS', 'In Progress'),
    ('RESOLVED', 'Resolved'),
]

class Report(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)
    
    # 2. Perbarui field status agar menggunakan choices [cite: 163-165]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES, # Tambahkan baris ini
        default='REPORTED'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title