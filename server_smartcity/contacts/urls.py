from django.urls import path
from . import views

urlpatterns = [
    # Kosongkan string path karena prefix 'contacts/' sudah diatur di urls project
    path('', views.contact_page, name='contact'),
]