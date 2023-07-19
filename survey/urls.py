from django.urls import path
from . import views

app_name = "survey"
urlpatterns = [
    path('hapusdataSurveyPenduduk/<hapus_id>', views.hapusDataSurveyPenduduk, name='hapusDataSurveyPenduduk'),
    path('editdataSurveyPenduduk/<edit_id>', views.editDataSurveyPenduduk, name='editDataSurveyPenduduk'),
    path('hapusdataSurveyRumahTangga/<hapus_id>', views.hapusDataSurveyRumahTangga,name='hapusDataSurveyRumahTangga'),
    path('editdataSurveyRumahTangga/<edit_id>', views.editDataSurveyRumahTangga, name='editDataSurveyRumahTangga'),
    path('tambahDataSurveyPenduduk/', views.tambahDataSurveyPenduduk, name='tambahDataSurveyPenduduk'),
    path('tambahDataSurveyRumahTangga/', views.tambahDataSurveyRumahTangga, name='tambahDataSurveyRumahTangga'),
    path('', views.index, name='index')
]


