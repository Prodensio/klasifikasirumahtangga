from django.db import models
import datetime
from penduduk.models import Penduduk



# Create your models here.
# Tabel Rumah Tangga
class RumahTangga(models.Model):
    no_rumah_tangga = models.BigIntegerField()
    kepala_rumah_tangga = models.OneToOneField(Penduduk, on_delete=models.CASCADE, related_name='rumah_tangga')
    pilihan_status_tempat_tinggal = (
        ('MILIK SENDIRI', 'MILIK SENDIRI'),
        ('KONTRAK/SEWA', 'KONTRAK/SEWA'),
        ('BEBAS SEWA', 'BEBAS SEWA'),
        ('DIPINJAMI', 'DIPINJAMI'), 
        ('DINAS', 'DINAS'), 
    )
    status_kepemilikan_tempat_tinggal = models.CharField(max_length=255, choices=pilihan_status_tempat_tinggal)
    luas_lantai_tempat_tinggal = models.IntegerField()
    pilihan_lantai = (
        ('MARMER/GRANIT', 'MARMER/GRANIT'),
        ('KERAMIK', 'KERAMIK'),
        ('PARKET/VINIL/PERMADANI', 'PARKET/VINIL/PERMADANI'),
        ('SEMEN', 'SEMEN'),
        ('TANAH', 'TANAH'),
    )
    jenis_lantai_tempat_tinggal = models.CharField(max_length=255, choices=pilihan_lantai)
    pilihan_jenis_dinding = (
        ('SEMEN', 'SEMEN'),
        ('BAMBU', 'BAMBU'),
    )
    jenis_dinding_tempat_tinggal = models.CharField(max_length=255, choices=pilihan_jenis_dinding)
    pilihan_jenis_atap = (
        ('GENTENG', 'GENTENG'),
        ('SENG', 'SENG'),
        ('JERAMI/IJUK', 'JERAMI/IJUK'),
    )
    jenis_atap_tempat_tinggal = models.CharField(max_length=255, choices=pilihan_jenis_atap)
    jenis_fasilitas_bab = (
        ('TIDAK PUNYA', 'TIDAK PUNYA'),
        ('JAMBAN SENDIRI', 'JAMBAN SENDIRI'),
        ('JAMBAN BERSAMA/TETANGGA', 'JAMBAN BERSAMA/TETANGA'),
        ('JAMBAN UMUM', 'JAMBAN UMUM'),
    )
    fasilitas_buang_air_besar = models.CharField(max_length=255, choices=jenis_fasilitas_bab)
    pilihan_jenis_penerangan = (
        ('TIDAK ADA', 'TIDAK ADA'),
        ('LISTRIK PLN', 'LISTRIK PLN'),
        ('LISTRIK NON PLN', 'LISTRIK NON PLN'),
        ('LAMPU MINYAK', 'LAMPU MINYAK'),
    )
    sumber_penerangan_rumah = models.CharField(max_length=255, choices=pilihan_jenis_penerangan)
    pilihan_energi_memasak = (
        ('LPG', 'LPG'),
        ('MINYAK TANAH', 'MINYAK TANAH'),
        ('KAYU BAKAR', 'KAYU BAKAR'),
    )
    bahan_bakar_untuk_memasak = models.CharField(max_length=255, choices=pilihan_energi_memasak)
    pilihan_jumlah_konsumsi_daging_susu_ayam = (
        ('KURANG DARI TIGA KALI', 'KURANG DARI TIGA KALI'),
        ('LEBIH DARI SAMA DENGAN TIGA KALI', 'LEBIH DARI SAMA DENGAN TIGA KALI'),
    )
    jumlah_konsumsi_daging_susu_ayam_dalam_seminggu = models.CharField(max_length=255, choices=pilihan_jumlah_konsumsi_daging_susu_ayam)
    pilihan_jumlah_membeli_pakaian = (
        ('SATU KALI', 'SATU KALI'),
        ('LEBIH DARI SATU KALI', 'LEBIH DARI SATU KALI'),
    )
    jumlah_membeli_pakaian_baru_dalam_setahun = models.CharField(max_length=255, choices=pilihan_jumlah_membeli_pakaian)
    pilihan_jumlah_makan_dalam_sehari = (
        ('KURANG DARI SAMA DENGAN DUA KALI', 'KURANG DARI SAMA DENGAN DUA KALI'),
        ('LEBIH DARI DUA KALI', 'LEBIH DARI DUA KALI'),
    )
    jumlah_makan_dalam_sehari = models.CharField(max_length=255, choices=pilihan_jumlah_makan_dalam_sehari)
    pilihan_sanggup_bayar = (
        ('MAMPU', 'MAMPU'),
        ('TIDAK MAMPU', 'TIDAK MAMPU'),
    )
    mampu_membayar_biaya_pengobatan = models.CharField(max_length=255, choices=pilihan_sanggup_bayar)
    pilihan_sumber_air_minum = (
        ('MATA AIR/PERPIPAAN', 'MATA AIR/PERPIPAAN'),
        ('SUNGAI/DANAU/EMBUNG', 'SUNGAI/DANAU/EMBUNG'),
        ('TADAH AIR HUJAN', 'TADAH AIR HUJAN'),
    )
    sumber_air_minum = models.CharField(max_length=255, choices=pilihan_sumber_air_minum)
    pilihan_simpanan = (
        ('YA', 'YA'),
        ('TIDAK', 'TIDAK'),
    )
    memiliki_simpanan_aset= models.CharField(max_length=255, choices=pilihan_simpanan)
    pilihan_status_rumah_tangga = (
        ('MISKIN', 'MISKIN'),
        ('TIDAK MISKIN', 'TIDAK MISKIN')
    )
    status_rumah_tangga = models.CharField(max_length=255, choices=pilihan_status_rumah_tangga)
    tahun = models.PositiveIntegerField()
    
    
    def __str__(self):
        return f"{self.kepala_rumah_tangga}"

    def save(self, *args, **kwargs):
        self.status_rumah_tangga = self.status_rumah_tangga.upper()
        if not self.pk:  # Jika objek baru
            self.tahun = datetime.date.today().year  # Isi tahun dengan tahun saat ini
        super().save(*args, **kwargs)




# tabel Anggota Rumah tangga
class AnggotaRumahTangga(models.Model):
    penduduk = models.ForeignKey(Penduduk, on_delete=models.CASCADE, related_name='anggota_rumah_tangga')
    rumah_tangga = models.ForeignKey(RumahTangga, on_delete=models.CASCADE, related_name='anggota_rumah_tangga')
    pilihan_hubungan = (
        ('KEPALA RUMAH TANGGA', 'KEPALA RUMAH TANGGA'),
        ('ANGGOTA RUMAH TANGGA', 'ANGGOTA RUMAH TANGGA'),
    )
    hubungan_dalam_rumah_tangga = models.CharField(max_length=255, choices=pilihan_hubungan)
    
    
    
    def __str__(self):
        return f"{self.penduduk} - {self.rumah_tangga}"
    
    
class BantuanRumahTangga(models.Model):
    rumah_tangga = models.ForeignKey(RumahTangga, on_delete=models.CASCADE, related_name='bantuan_rumah_tangga')
    pilihan_bantuan = (
        ('BLT DANA DESA', 'BLT DANA DESA'),
        ('PKH', 'PKH'),
        ('BST', 'BST'),
        ('BANPRES', 'BANPRES'),
        ('UMKM', 'UMKM'),
        ('BANTUAN PEKERJA', 'BANTUAN PEKERJA'),
        ('BANTUAN PENDIDIKAN ANAK', 'BANTUAN PENDIDIKAN ANAK'),
        ('BANTUAN LAINYA', 'BANTUAN LAINYA'),
    )
    jenis_bantuan = models.CharField(max_length=255, choices=pilihan_bantuan)
    jumlah_bantuan = models.IntegerField()
    
    def __str__(self):
        return f"{self.jenis_bantuan} - {self.rumah_tangga.kepala_rumah_tangga.nama_penduduk}"
