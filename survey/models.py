from django.db import models
import datetime



# Create your models here.cls
class SurveyPenduduk(models.Model):
    pilihan_dusun = (
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('IV', 'IV'),
    )
    dusun = models.CharField(max_length=3, choices=pilihan_dusun)
    pilihan_rt = (
        ('001', '001'),
        ('002', '002'),
        ('003', '003'),
        ('004', '004'),
        ('005', '005'),
        ('006', '006'),
        ('007', '007'),
        ('008', '008'),
    )
    rt = models.CharField(max_length=3, choices=pilihan_rt)
    no_rumah_tangga = models.BigIntegerField()
    no_kartu_keluarga = models.BigIntegerField()
    no_induk_kependudukan = models.BigIntegerField()
    nama_penduduk = models.CharField(max_length=255)
    pilihan_jenis_kelamin = (
        ('LAKI-LAKI', 'LAKI-LAKI'),
        ('PEREMPUAN', 'PEREMPUAN'),
    )
    jenis_kelamin = models.CharField(max_length=20, choices=pilihan_jenis_kelamin)
    tempat_lahir = models.CharField(max_length=255)
    tanggal_lahir = models.DateField()
    alamat = models.CharField(max_length=255)
    pilihan_status_pernikahan = (
        ('BELUM KAWIN', 'BELUM KAWIN'),
        ('KAWIN', 'KAWIN'),
        ('CERAI HIDUP', 'CERAI HIDUP'),
        ('CERAI MATI', 'CERAI MATI'),
    )
    status_pernikahan = models.CharField(max_length=50, choices=pilihan_status_pernikahan)
    pilihan_agama = (
        ('ISLAM', 'ISLAM'),
        ('KRISTEN', 'KRISTEN'),
        ('KHATOLIK', 'KHATOLIK'),
        ('HINDU', 'HINDU'),
        ('BUDHA', 'BUDHA'),
        ('KHONGHUCU', 'KHONGHUCU')
    )
    agama = models.CharField(max_length=50, choices=pilihan_agama, blank=True)
    no_hp = models.CharField(max_length=50, blank=True)
    pilihan_pekerjaan = (
        ('TIDAK BEKERJA', 'TIDAK BEKERJA'),
        ('APARATUR DESA','APARATUR DESA'),
        ('BIARAWATI','BIARAWATI'),
        ('BIDAN','BIDAN'),
        ('DOKTER','DOKTER'),
        ('GURU','GURU'),
        ('IBU RUMAH TANGGA','IBU RUMAH TANGGA'),
        ('KARYAWAN SWASTA','KARYAWAN SWASTA'),
        ('KONTRAKTOR','KONTRAKTOR'),
        ('PEDAGANG','PEDAGANG'),
        ('PENSIUNAN','PENSIUNAN'),
        ('PERANGKAT DESA','PERANGKAT DESA'),
        ('PETANI','PETANI'),
        ('SOPIR','SOPIR'), 
        ('TUKANG','TUKANG'),
        ('APOTEKER','APOTEKER'),
        ('PELAJAR/MAHASISWA', 'PELAJAR/MAHASISWA'),
    )
    pekerjaan = models.CharField(max_length=50, choices=pilihan_pekerjaan)
    penghasilan = models.IntegerField(blank=True, null=True)
    pilihan_pendidikan = (
        ('TIDAK SEKOLAH', 'TIDAK SEKOLAH'),
        ('SD', 'SD'),
        ('SMP', 'SMP'),
        ('SMA', 'SMA'),
        ('DIPLOMA', 'DIPLOMA'),
        ('SARJANA', 'SARJANA'),
    )
    pendidikan = models.CharField(max_length=15, choices=pilihan_pendidikan, blank=True)
    pilihan_hubungan_dalam_keluarga = (
        ('KEPALA KELUARGA', 'KEPALA KELUARGA'),
        ('SUAMI', 'SUAMI'),
        ('ISTRI', 'ISTRI'),
        ('ANAK', 'ANAK'),
        ('MENANTU', 'MENANTU'),
        ('CUCU', 'CUCU'),
        ('ORANG TUA', 'ORANG TUA'),
        ('MERTUA', 'MERTUA'),
        ('FAMILI LAIN', 'FAMILI LAIN'),
        ('PEMBANTU', 'PEMBANTU'),
        ('LAINYA', 'LAINYA'),
    )
    hubungan_dalam_keluarga = models.CharField(max_length=255, choices=pilihan_hubungan_dalam_keluarga)
    tahun = models.PositiveIntegerField()



    def save(self, *args, **kwargs):
        self.nama_penduduk = self.nama_penduduk.upper()
        self.alamat = self.alamat.upper()
        if not self.pk:  
            self.tahun = datetime.date.today().year
        super().save(*args, **kwargs)



    def __str__(self):
        return f"{self.nama_penduduk} - {self.hubungan_dalam_keluarga}"



# Tabel Rumah Tangga
class SurveyRumahTangga(models.Model):
    pilihan_dusun = (
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('IV', 'IV'),
    )
    dusun = models.CharField(max_length=3, choices=pilihan_dusun)
    pilihan_rt = (
        ('001', '001'),
        ('002', '002'),
        ('003', '003'),
        ('004', '004'),
        ('005', '005'),
        ('006', '006'),
        ('007', '007'),
        ('008', '008'),
    )
    rt = models.CharField(max_length=3, choices=pilihan_rt)
    no_rumah_tangga = models.BigIntegerField()
    no_kartu_keluarga = models.BigIntegerField()
    kepala_rumah_tangga = models.CharField(max_length=255)
    nik_kepala_rumah_tangga = models.BigIntegerField()
    pilihan_pekerjaan = (
        ('TIDAK BEKERJA', 'TIDAK BEKERJA'),
        ('APARATUR DESA','APARATUR DESA'),
        ('BIARAWATI','BIARAWATI'),
        ('BIDAN','BIDAN'),
        ('DOKTER','DOKTER'),
        ('GURU','GURU'),
        ('IBU RUMAH TANGGA','IBU RUMAH TANGGA'),
        ('KARYAWAN SWASTA','KARYAWAN SWASTA'),
        ('KONTRAKTOR','KONTRAKTOR'),
        ('PEDAGANG','PEDAGANG'),
        ('PENSIUNAN','PENSIUNAN'),
        ('PERANGKAT DESA','PERANGKAT DESA'),
        ('PETANI','PETANI'),
        ('SOPIR','SOPIR'), 
        ('TUKANG','TUKANG'),
    )
    pekerjaan_kepala_rumah_tangga = models.CharField(max_length=50, choices=pilihan_pekerjaan)
    penghasilan_kepala_rumah_tangga = models.IntegerField(blank=True, null=True)
    pilihan_pendidikan = (
        ('TIDAK SEKOLAH', 'TIDAK SEKOLAH'),
        ('SD', 'SD'),
        ('SMP', 'SMP'),
        ('SMA', 'SMA'),
        ('DIPLOMA', 'DIPLOMA'),
        ('SARJANA', 'SARJANA'),
    )
    pendidikan_kepala_rumah_tangga = models.CharField(max_length=15, choices=pilihan_pendidikan, blank=True)
    alamat_rumah_tangga = models.CharField(max_length=255)
    jumlah_anggota_rumah_tangga = models.IntegerField()
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
        ('KERAMIK', 'KERAMIK'),
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
        ('LAMPU MINYAK', 'LAMPU MINYAK'),
    )
    sumber_penerangan_rumah = models.CharField(max_length=255, choices=pilihan_jenis_penerangan)
    pilihan_bahan_bakar_untuk_memasak = (
        ('LPG', 'LPG'),
        ('MINYAK TANAH', 'MINYAK TANAH'),
        ('KAYU BAKAR', 'KAYU BAKAR'),
    )
    bahan_bakar_untuk_memasak = models.CharField(max_length=255, choices=pilihan_bahan_bakar_untuk_memasak)
    pilihan_jumlah_konsumsi_daging_susu_ayam = (
        ('SATU KALI', 'SATU KALI'),
        ('LEBIH DARI SATU KALI', 'LEBIH DARI SATU KALI'),
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
    tahun = models.PositiveIntegerField()



    def save(self, *args, **kwargs):
        self.kepala_rumah_tangga = self.kepala_rumah_tangga.upper()
        self.alamat_rumah_tangga = self.alamat_rumah_tangga.upper()
        if not self.pk:  
            self.tahun = datetime.date.today().year  
        super().save(*args, **kwargs)


