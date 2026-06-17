from django.contrib import admin
from django.urls import path, include
from buku.views import dashboard 

urlpatterns = [
    path('admin/', admin.site.urls),
    # Dashboard (Halaman Utama)
    path('', dashboard, name='dashboard'),
    
    # Rute ke masing-masing aplikasi
    path('buku/', include('buku.urls')),
    path('siswa/', include('siswa.urls')),
    path('peminjaman/', include('peminjaman.urls')),
]