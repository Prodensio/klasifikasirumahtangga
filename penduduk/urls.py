from django.urls import path
from . import views


# urls pattern
app_name = "penduduk"
urlpatterns = [
    path('edit/<edit_id>', views.editData, name='editData'),
    path('hapus/<hapus_id>', views.hapusData, name='hapusData'),
    path('lihat/<lihat_id>', views.lihatData, name='lihatData'),
    path('tambah/', views.tambahData, name='tambahData'),
    path('export/', views.exportDataToExel, name='exportData'),
    path('cariDataPenduduk/', views.cariDataPenduduk, name='cariDataPenduduk'),
    path('cari/', views.cariData, name='cariData'),
    path('detail/<int:rumah_tangga_id>/', views.detailRumahTangga, name='detail'),
    path('', views.index, name='index'),
    
] 