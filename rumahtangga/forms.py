from django import forms
from .models import RumahTangga, AnggotaRumahTangga, BantuanRumahTangga
from penduduk.models import Penduduk


# create your foms here
# Form Rumah Tangga
class FormRumahTangga(forms.ModelForm):
    class Meta:
        model = RumahTangga
        fields = [
            'no_rumah_tangga',
            'kepala_rumah_tangga',
            'status_kepemilikan_tempat_tinggal', 
            'luas_lantai_tempat_tinggal',
            'jenis_lantai_tempat_tinggal', 
            'jenis_dinding_tempat_tinggal', 
            'jenis_atap_tempat_tinggal', 
            'fasilitas_buang_air_besar', 
            'sumber_penerangan_rumah', 
            'bahan_bakar_untuk_memasak',
            'jumlah_konsumsi_daging_susu_ayam_dalam_seminggu', 
            'jumlah_membeli_pakaian_baru_dalam_setahun', 
            'jumlah_makan_dalam_sehari', 
            'mampu_membayar_biaya_pengobatan',
            'sumber_air_minum', 
            'memiliki_simpanan_aset', 
            'status_rumah_tangga', 
        ]
        labels = {
            'no_rumah_tangga': 'NO RUMAH TANGGA',
            'kepala_rumah_tangga': 'KEPALA RUMAH TANGGA',
            'status_kepemilikan_tempat_tinggal': 'STATUS KEPEMILIKAN TEMPAT TINGGAL', 
            'luas_lantai_tempat_tinggal': 'LUAS LANTAI TEMPAT TINGGAL (M2)',
            'jenis_lantai_tempat_tinggal': 'JENIS LANTAI TEMPAT TINGGAL', 
            'jenis_dinding_tempat_tinggal': 'JENIS DINDING TEMPAT TINGGAL', 
            'jenis_atap_tempat_tinggal': 'JENIS ATAP TEMPAT TINGGAL', 
            'fasilitas_buang_air_besar': 'FASILITAS BAB', 
            'sumber_penerangan_rumah': 'SUMBER PENERANGAN RUMAH', 
            'bahan_bakar_untuk_memasak': 'BAHAN BAKAR UNTUK MEMASAK',
            'jumlah_konsumsi_daging_susu_ayam_dalam_seminggu': 'JUMLAH KONSUMSI DAGING/SUSU/AYAM DALAM SEMINGGU', 
            'jumlah_membeli_pakaian_baru_dalam_setahun': 'JUMLAH MEMBELI PAKAIAN BARU DALAM SETAHUN', 
            'jumlah_makan_dalam_sehari': 'JUMLAH MAKAN DALAM SEHARI', 
            'mampu_membayar_biaya_pengobatan': 'MAMPU MEMBAYAR BIAYA PENGOBATAN',
            'sumber_air_minum': 'SUMBER AIR MINUM RUMAH TANGGA', 
            'memiliki_simpanan_aset': 'MEMILIKI SIMPANAN ASET', 
            'status_rumah_tangga': 'STATUS RUMAH TANGGA', 
        }
        widgets = {
            'no_rumah_tangga': forms.NumberInput(attrs={'class': 'form-control'}),
            'kepala_rumah_tangga': forms.Select(attrs={'class': 'form-control'}),
            'status_kepemilikan_tempat_tinggal': forms.Select(attrs={'class': 'form-control'}),
            'luas_lantai_tempat_tinggal': forms.TextInput(attrs={'class': 'form-control'}),
            'jenis_lantai_tempat_tinggal': forms.Select(attrs={'class': 'form-control'}),
            'jenis_dinding_tempat_tinggal': forms.Select(attrs={'class': 'form-control'}),
            'jenis_atap_tempat_tinggal': forms.Select(attrs={'class': 'form-control'}),
            'fasilitas_buang_air_besar': forms.Select(attrs={'class': 'form-control'}),
            'sumber_penerangan_rumah': forms.Select(attrs={'class': 'form-control'}),
            'bahan_bakar_untuk_memasak': forms.Select(attrs={'class': 'form-control'}),
            'jumlah_konsumsi_daging_susu_ayam_dalam_seminggu': forms.Select(attrs={'class': 'form-control'}), 
            'jumlah_membeli_pakaian_baru_dalam_setahun': forms.Select(attrs={'class': 'form-control'}),
            'jumlah_makan_dalam_sehari': forms.Select(attrs={'class': 'form-control'}),
            'mampu_membayar_biaya_pengobatan': forms.Select(attrs={'class': 'form-control'}),
            'sumber_air_minum': forms.Select(attrs={'class': 'form-control'}),
            'memiliki_simpanan_aset': forms.Select(attrs={'class': 'form-control'}),
            'status_rumah_tangga': forms.Select(attrs={'class': 'form-control'}),
        } 
        


# Form Anggota Rumah Tangga
class FormAnggotaRumahTangga(forms.ModelForm):
    class Meta:
        model = AnggotaRumahTangga
        fields = [
            'penduduk',
        ]
        labels = {
            'penduduk': 'PENDUDUK',
        }
        widgets = {
            'penduduk': forms.Select(attrs={'class': 'form-control'}),
        }



    def __init__(self, *args, **kwargs):
        super(FormAnggotaRumahTangga, self).__init__(*args, **kwargs)
        self.fields['penduduk'].queryset = Penduduk.objects.all()
        
        
class FormBantuanRumahTangga(forms.ModelForm):
    class Meta:
        model = BantuanRumahTangga
        fields = [
            'rumah_tangga',
            'jenis_bantuan',
            'jumlah_bantuan'
        ]
        labels = {
            'rumah_tangga': 'RUMAH TANGGA',
            'jenis_bantuan' : 'BANTUAN',
            'jumlah_bantuan' : 'JUMLAH'
        }
        widgets = {
            'rumah_tangga': forms.Select(attrs={'class': 'form-control'}),
            'jenis_bantuan': forms.Select(attrs={'class': 'form-control'}),
            'jumlah_bantuan': forms.NumberInput(attrs={'class': 'form-control'}),
        }



    def __init__(self, *args, **kwargs):
        super(FormBantuanRumahTangga, self).__init__(*args, **kwargs)
        self.fields['rumah_tangga'].queryset = RumahTangga.objects.all()
        
