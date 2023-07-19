from django import forms
from .models import Penduduk


# create your forms here
class FormPenduduk(forms.ModelForm):
    class Meta:
        model = Penduduk
        fields = [
            'dusun',
            'rt',
            'no_kartu_keluarga',
            'no_induk_kependudukan',
            'nama_penduduk',
            'jenis_kelamin',
            'tempat_lahir',
            'tanggal_lahir',
            'alamat',
            'status_pernikahan',
            'agama',
            'no_hp',
            'pekerjaan',
            'penghasilan',
            'pendidikan',
            'hubungan_dalam_keluarga',
        ]
        labels = {
            'dusun' : 'DUSUN',
            'rt' : 'RT',
            'no_kartu_keluarga' : 'NO KARTU KELUARGA',
            'no_induk_kependudukan': 'NO INDUK KEPENDUDUKAN',
            'nama_penduduk': 'NAMA PENDUDUK',
            'jenis_kelamin': 'JENIS KELAMIN',
            'tempat_lahir': 'TEMPAT LAHIR',
            'tanggal_lahir': 'TANGGAL LAHIR',
            'alamat': 'ALAMAT',
            'status_pernikahan': 'STATUS PERNIKAHAN',
            'agama': 'AGAMA',
            'no_hp': 'NO HP',
            'pekerjaan': 'PEKERJAAN',
            'penghasilan': 'PENGHASILAN',
            'pendidikan': 'PENDIDIKAN',
            'hubungan_dalam_keluarga': 'HUBUNGAN DALAM KELUARGA',
        }
        widgets = {
            'dusun' : forms.Select(attrs={'class': 'form-control'}),
            'rt' : forms.Select(attrs={'class': 'form-control'}),
            'no_kartu_keluarga' : forms.NumberInput(attrs={'class': 'form-control'}),
            'no_induk_kependudukan': forms.NumberInput(attrs={'class': 'form-control'}),
            'nama_penduduk': forms.TextInput(attrs={'class': 'form-control'}),
            'jenis_kelamin': forms.Select(attrs={'class': 'form-control'}),
            'tempat_lahir': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_lahir': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'alamat' : forms.TextInput(attrs={'class': 'form-control'}) ,
            'status_pernikahan': forms.Select(attrs={'class': 'form-control'}),
            'agama': forms.Select(attrs={'class': 'form-control'}),
            'no_hp': forms.NumberInput(attrs={'class': 'form-control'}),
            'pekerjaan': forms.Select(attrs={'class': 'form-control'}),
            'penghasilan': forms.NumberInput(attrs={'class': 'form-control'}),
            'pendidikan': forms.Select(attrs={'class': 'form-control'}),
            'hubungan_dalam_keluarga': forms.Select(attrs={'class': 'form-control'}),
        }
        
