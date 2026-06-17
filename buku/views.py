from django.shortcuts import render, redirect
from django.db import connection

# ==========================================
# FUNGSI 1: MENAMPILKAN DAFTAR BUKU (R - Read)
# ==========================================
def list_buku(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM buku ORDER BY id ASC")
        columns = [col[0] for col in cursor.description]
        data_buku = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    context = {'data_buku': data_buku}
    return render(request, 'buku/list_buku.html', context)


# ==========================================
# FUNGSI 2: MENAMBAH BUKU BARU (C - Create)
# ==========================================
def tambah_buku(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        pengarang = request.POST.get('pengarang')
        kategori = request.POST.get('kategori')
        penerbit = request.POST.get('penerbit')
        tahun_terbit = request.POST.get('tahun_terbit')
        rak = request.POST.get('rak')
        stok = request.POST.get('stok')
        deskripsi = request.POST.get('deskripsi')

        with connection.cursor() as cursor:
            # Hapus bagian ', isbn' dan '%s' paling ujung agar sesuai dengan kolom tabel asli kamu
            cursor.execute("""
                INSERT INTO buku (judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok, deskripsi)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, [judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok, deskripsi])
        
        return redirect('list_buku')
    
    return render(request, 'buku/tambah_buku.html')
# ==========================================
# FUNGSI 3: MENGUBAH DATA BUKU (U - Update)
# ==========================================
def edit_buku(request, id):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            judul = request.POST.get('judul')
            pengarang = request.POST.get('pengarang')
            kategori = request.POST.get('kategori')
            penerbit = request.POST.get('penerbit')
            tahun_terbit = request.POST.get('tahun_terbit')
            rak = request.POST.get('rak')
            stok = request.POST.get('stok')
            deskripsi = request.POST.get('deskripsi')
            isbn = request.POST.get('isbn', None)

            cursor.execute("""
                UPDATE buku 
                SET judul=%s, pengarang=%s, kategori=%s, penerbit=%s, tahun_terbit=%s, rak=%s, stok=%s, deskripsi=%s
                WHERE id=%s
            """, [judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok, deskripsi, id])
            
            return redirect('list_buku')

        # Ambil data lama untuk ditampilkan di form
        cursor.execute("SELECT * FROM buku WHERE id = %s", [id])
        row = cursor.fetchone()
        
        columns = [col[0] for col in cursor.description]
        buku = dict(zip(columns, row))

    return render(request, 'buku/edit_buku.html', {'buku': buku})

def hapus_buku(request, id):
    with connection.cursor() as cursor:
        # Eksekusi perintah hapus berdasarkan ID
        cursor.execute("DELETE FROM buku WHERE id = %s", [id])
    
    # Setelah dihapus, langsung kembali ke halaman daftar buku
    return redirect('list_buku')

def detail_buku(request, id):
    with connection.cursor() as cursor:
        # Ambil data 1 buku berdasarkan ID
        cursor.execute("SELECT * FROM buku WHERE id = %s", [id])
        row = cursor.fetchone()
        
        # Ubah jadi dictionary
        columns = [col[0] for col in cursor.description]
        buku = dict(zip(columns, row))

    return render(request, 'buku/detail_buku.html', {'buku': buku})

def dashboard(request):
    with connection.cursor() as cursor:
        # Menghitung total stok buku keseluruhan
        cursor.execute("SELECT SUM(stok) FROM buku")
        total_buku = cursor.fetchone()[0] or 0

        # Menghitung total macam/judul buku
        cursor.execute("SELECT COUNT(*) FROM buku")
        total_judul = cursor.fetchone()[0] or 0

        # Menghitung buku yang sedang dipinjam
        cursor.execute("SELECT COUNT(*) FROM peminjaman WHERE status = 'Dipinjam'")
        sedang_dipinjam = cursor.fetchone()[0] or 0

        # Menghitung buku yang sudah dikembalikan
        cursor.execute("SELECT COUNT(*) FROM peminjaman WHERE status = 'Dikembalikan'")
        sudah_dikembalikan = cursor.fetchone()[0] or 0

    context = {
        'total_buku': total_buku,
        'total_judul': total_judul,
        'sedang_dipinjam': sedang_dipinjam,
        'sudah_dikembalikan': sudah_dikembalikan
    }
    return render(request, 'dashboard.html', context)