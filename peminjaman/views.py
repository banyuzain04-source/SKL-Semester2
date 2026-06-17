from django.shortcuts import render, redirect
from django.db import connection

# ==========================================
# FUNGSI 1: MENAMPILKAN DAFTAR PEMINJAMAN 
# ==========================================
def list_peminjaman(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.id, s.nama AS nama_siswa, b.judul AS judul_buku, 
                   p.tanggal_pinjam, p.jatuh_tempo, p.status 
            FROM peminjaman p
            JOIN siswa s ON p.siswa_id = s.id
            JOIN buku b ON p.buku_id = b.id
            ORDER BY p.tanggal_pinjam DESC
        """)
        columns = [col[0] for col in cursor.description]
        data_peminjaman = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    return render(request, 'peminjaman/list_peminjaman.html', {'data_peminjaman': data_peminjaman})

# ==========================================
# FUNGSI 2: MENAMBAH PEMINJAMAN & KURANGI STOK
# ==========================================
def tambah_peminjaman(request):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            siswa_id = request.POST.get('siswa_id')
            buku_id = request.POST.get('buku_id')
            tanggal_pinjam = request.POST.get('tanggal_pinjam')
            jatuh_tempo = request.POST.get('jatuh_tempo')
            keperluan = request.POST.get('keperluan')
            status = request.POST.get('status')

            # 1. Masukkan data ke tabel peminjaman
            cursor.execute("""
                INSERT INTO peminjaman (siswa_id, buku_id, tanggal_pinjam, jatuh_tempo, keperluan, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, [siswa_id, buku_id, tanggal_pinjam, jatuh_tempo, keperluan, status])

            # 2. LOGIKA STOK: Jika status awal 'Dipinjam', kurangi stok buku 1
            if status == 'Dipinjam':
                cursor.execute("UPDATE buku SET stok = stok - 1 WHERE id = %s", [buku_id])

            return redirect('list_peminjaman')

        # Dropdown data
        cursor.execute("SELECT id, nama FROM siswa WHERE is_active = True")
        siswa_list = [dict(zip(['id', 'nama'], row)) for row in cursor.fetchall()]

        cursor.execute("SELECT id, judul, stok FROM buku WHERE stok > 0")
        buku_list = [dict(zip(['id', 'judul', 'stok'], row)) for row in cursor.fetchall()]

    return render(request, 'peminjaman/tambah_peminjaman.html', {'siswa_list': siswa_list, 'buku_list': buku_list})

# ==========================================
# FUNGSI 3: UBAH STATUS & KEMBALIKAN STOK
# ==========================================
def ubah_status(request, id):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            status_baru = request.POST.get('status')

            # 1. Ambil data status yang lama dan buku_id untuk dicek
            cursor.execute("SELECT buku_id, status FROM peminjaman WHERE id = %s", [id])
            row = cursor.fetchone()
            buku_id = row[0]
            status_lama = row[1]

            # 2. Update status transaksinya
            cursor.execute("UPDATE peminjaman SET status = %s WHERE id = %s", [status_baru, id])

            # 3. LOGIKA STOK: Jika sebelumnya 'Dipinjam' lalu jadi 'Dikembalikan', tambah stok 1
            if status_lama in ['Dipinjam', 'Terlambat'] and status_baru == 'Dikembalikan':
                cursor.execute("UPDATE buku SET stok = stok + 1 WHERE id = %s", [buku_id])
            
            # Jika admin tidak sengaja klik 'Dikembalikan' lalu balikin lagi ke 'Dipinjam', kurangi stok lagi
            elif status_lama == 'Dikembalikan' and status_baru in ['Dipinjam', 'Terlambat']:
                cursor.execute("UPDATE buku SET stok = stok - 1 WHERE id = %s", [buku_id])

            return redirect('list_peminjaman')

        # Ambil data buat form
        cursor.execute("SELECT id, status FROM peminjaman WHERE id = %s", [id])
        row = cursor.fetchone()
        peminjaman = dict(zip(['id', 'status'], row))

    return render(request, 'peminjaman/ubah_status.html', {'peminjaman': peminjaman})