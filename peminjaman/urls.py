from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_peminjaman, name='list_peminjaman'),
    path('tambah/', views.tambah_peminjaman, name='tambah_peminjaman'),
    path('ubah_status/<int:id>/', views.ubah_status, name='ubah_status'),
]