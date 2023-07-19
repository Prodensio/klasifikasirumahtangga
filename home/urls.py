from django.urls import path
from . import views


# your pattern
app_name = 'home'
urlpatterns = [
    path('admin/',views.indexAdmin, name='indexAdmin'),
    path('operator/',views.indexOperator, name='indexOperator'),
    path('penduduk/',views.indexPenduduk, name='indexPenduduk'),
]