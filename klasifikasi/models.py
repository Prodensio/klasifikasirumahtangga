import os
import pickle
import datetime
import random
import string
from django.db import models
from survey.models import SurveyRumahTangga


# create your models here
class DataModeling(models.Model):
    luas_lantai_tempat_tinggal = models.IntegerField()
    jenis_lantai_tempat_tinggal = models.CharField(max_length=50)
    jenis_dinding_tempat_tinggal = models.CharField(max_length=50)
    fasilitas_buang_air_besar = models.CharField(max_length=50)
    sumber_air_minum = models.CharField(max_length=50)
    sumber_penerangan_rumah = models.CharField(max_length=50)
    bahan_bakar_untuk_memasak = models.CharField(max_length=50)
    jumlah_konsumsi_daging_susu_ayam_dalam_seminggu = models.CharField(max_length=50)
    jumlah_makan_dalam_sehari = models.CharField(max_length=50)
    jumlah_membeli_pakaian_baru_dalam_setahun = models.CharField(max_length=50)
    penghasilan_kepala_rumah_tangga = models.IntegerField()
    pendidikan_kepala_rumah_tangga = models.CharField(max_length=50)
    mampu_membayar_biaya_pengobatan = models.CharField(max_length=50)
    memiliki_simpanan_aset = models.CharField(max_length=50)
    status_rumah_tangga = models.CharField(max_length=50)
    
    
    
    def __str__(self):
        return str(self.status_rumah_tangga)
    
    


class SVMModel(models.Model):
    model_file = models.FileField(upload_to='svm_models/')

    def save_model(self, model):
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        unique_filename = f'svm_model_{timestamp}_{random_string}.pkl'

        model_file_path = os.path.join('svm_models', unique_filename)
        os.makedirs(os.path.dirname(model_file_path), exist_ok=True)

        with open(model_file_path, 'wb') as file:
            pickle.dump(model, file)

        self.model_file.name = model_file_path
        self.save()

    def load_model(self):
        with open(self.model_file.path, 'rb') as file:
            model = pickle.load(file)
        return model


class Prediksi(models.Model):
    survey_rumah_tangga = models.ForeignKey(SurveyRumahTangga, on_delete=models.CASCADE)
    prediction = models.CharField(max_length=100)

    def __str__(self):
        return f"Prediksi untuk {self.survey_rumah_tangga}"

