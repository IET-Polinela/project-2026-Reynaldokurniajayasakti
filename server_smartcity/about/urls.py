from django.urls import path
from . import views

urlpatterns = [
    # Kosongkan string path karena prefix 'about/' sudah diatur di urls project
    path('', views.about_page, name='about'),
]