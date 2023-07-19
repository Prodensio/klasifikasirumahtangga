from django.urls import path
from . import views


# create your urls here
app_name = "rumahtangga"
urlpatterns = [
    path('detail/<int:rumah_tangga_id>/', views.detailRumahTangga, name='detail'),
    path('detail/<int:rumah_tangga_id>/hapus/<int:hapus_id>/', views.hapusAnggotaRumahTangga, name='hapusAnggota'),
    path('hapus/<int:hapus_id>/', views.hapusData, name='hapusData'),
    path('edit/<int:edit_id>/', views.editData, name='editData'),
    path('tambahDataAnggota/<int:tambah_anggota_id>/', views.tambahAnggotaRumahTangga, name='tambahDataAnggota'),
    path('bantuan/', views.bantuanRumahTangga, name='bantuan'),
    path('tambahBantuan/', views.tambahBantuanRumahTangga, name='tambahBantuan'),
    path('hapusBantuan/<int:hapus_bantuan_id>', views.hapusDataBantuan, name='hapusBantuan'),
    path('export/', views.exportDataToExel, name='exportData'),
    path('tambah/', views.tambahData, name='tambahData'),
    path('cari/', views.cariData, name='cariData'),
    path('laporan/', views.laporanRumahTangga, name='laporan'),
    path('', views.index, name='index'),
]
