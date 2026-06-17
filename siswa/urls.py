from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_siswa, name='list_siswa'),
    path('tambah/', views.tambah_siswa, name='tambah_siswa'),
    path('edit/<int:id>/', views.edit_siswa, name='edit_siswa'),
    path('detail/<int:id>/', views.detail_siswa, name='detail_siswa'),
    path('hapus/<int:id>/', views.hapus_siswa, name='hapus_siswa'),
]

