from django.urls import path
from . import views


# create your urls here
app_name = "klasifikasi"
urlpatterns = [
    path('modeling/splitData', views.splitData, name='splitData'),
    path('modeling/tampil', views.tampilData, name='tampilData'),
    path('modeling/importData', views.loadDatasetCSV, name='importData'),
    path('prediksi/<int:prediksi_id>', views.prediksi, name='prediksi'),
    path('exportData/', views.exportDataToExel, name='exportData'),
    path('modeling/latihModel', views.latihModel, name='latihModel'),
    path('modeling/simpanModel', views.simpanModel, name='simpanModel'),
    path('modeling/', views.modelView, name='modeling'),
    path('laporan/', views.laporanPrediksi, name='laporanPrediksi'),
    path('', views.index, name = 'index'),
]