from django.db import models



# create your models here
class Penduduk(models.Model):
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
    agama = models.CharField(max_length=50, choices=pilihan_agama)
    no_hp = models.CharField(max_length=50)
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
    penghasilan = models.IntegerField()
    pilihan_pendidikan = (
        ('TIDAK SEKOLAH', 'TIDAK SEKOLAH'),
        ('SD', 'SD'),
        ('SMP', 'SMP'),
        ('SMA', 'SMA'),
        ('DIPLOMA', 'DIPLOMA'),
        ('SARJANA', 'SARJANA'),
    )
    pendidikan = models.CharField(max_length=15, choices=pilihan_pendidikan)
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
    
    
    
    def save(self, *args, **kwargs):
        self.nama_penduduk = self.nama_penduduk.upper()
        self.alamat = self.alamat.upper()
        super().save(*args, **kwargs)
        
        
        
    def __str__(self):
        return f"{self.nama_penduduk} - {self.hubungan_dalam_keluarga}"
