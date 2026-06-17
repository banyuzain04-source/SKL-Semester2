# buku/models.py
from django.db import models

class Buku(models.Model):
    judul = models.CharField(max_length=255)
    pengarang = models.CharField(max_length=255)
    kategori = models.CharField(max_length=50)
    penerbit = models.CharField(max_length=255)
    tahun_terbit = models.IntegerField()
    rak = models.CharField(max_length=50)
    stok = models.IntegerField()
    deskripsi = models.TextField()

    class Meta:
        db_table = 'buku'  # Ini memaksa Django membuat nama tabel "buku" bukan "buku_buku"