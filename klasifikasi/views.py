import os
import base64
# project
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import SVMModel, Prediksi, DataModeling
from survey.models import SurveyRumahTangga
from django.contrib import messages
from django.conf import settings

# dataminig
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from django_pandas.io import read_frame
from sklearn.pipeline import Pipeline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from openpyxl import Workbook
from django.http import HttpResponse
from sklearn.svm import SVC
import seaborn as sns
import pandas as pd
import numpy as np
import pickle
import csv
import io
from sklearn import svm






# create your views here


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def exportDataToExel(request):
    data_prediksi_rumah_tangga = Prediksi.objects.all()
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append([
        'no',
        'kepala_rumah_tangga',
        'luas_lantai_tempat_tinggal',
        'jenis_lantai_tempat_tinggal',
        'jenis_dinding_tempat_tinggal',
        'fasilitas_buang_air_besar',
        'sumber_air_minum',
        'sumber_penerangan_rumah',
        'bahan_bakar_untuk_memasak',
        'jumlah_konsumsi_daging_susu_ayam_dalam_seminggu',
        'jumlah_makan_dalam_sehari',
        'jumlah_membeli_pakaian_baru_dalam_setahun',
        'penghasilan_kepala_rumah_tangga',
        'pendidikan_kepala_rumah_tangga',
        'mampu_membayar_biaya_pengobatan',
        'memiliki_simpanan_aset',
        'status_rumah_tangga',
    ])
    for prediksi in data_prediksi_rumah_tangga:
        worksheet.append([
                            prediksi.id, 
                            prediksi.survey_rumah_tangga.kepala_rumah_tangga, 
                            prediksi.survey_rumah_tangga.luas_lantai_tempat_tinggal, 
                            prediksi.survey_rumah_tangga.jenis_lantai_tempat_tinggal, 
                            prediksi.survey_rumah_tangga.jenis_dinding_tempat_tinggal, 
                            prediksi.survey_rumah_tangga.fasilitas_buang_air_besar, 
                            prediksi.survey_rumah_tangga.sumber_air_minum, 
                            prediksi.survey_rumah_tangga.sumber_penerangan_rumah,
                            prediksi.survey_rumah_tangga.bahan_bakar_untuk_memasak, 
                            prediksi.survey_rumah_tangga.jumlah_konsumsi_daging_susu_ayam_dalam_seminggu, 
                            prediksi.survey_rumah_tangga.jumlah_makan_dalam_sehari, 
                            prediksi.survey_rumah_tangga.jumlah_membeli_pakaian_baru_dalam_setahun, 
                            prediksi.survey_rumah_tangga.penghasilan_kepala_rumah_tangga, 
                            prediksi.survey_rumah_tangga.pendidikan_kepala_rumah_tangga, 
                            prediksi.survey_rumah_tangga.mampu_membayar_biaya_pengobatan,
                            prediksi.survey_rumah_tangga.memiliki_simpanan_aset, 
                            prediksi.prediction,
        ])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=prediksi_rumah_tangga.xlsx'
    workbook.save(response)
    return response



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def laporanPrediksi(request):
    user_groups = request.user.groups.all()
    try:
        prediksi_obj = Prediksi.objects.all().order_by('-id')
        context = {
            "title": "KLASIFIKASI",
            "content_header": "HASIL PREDIKSI RUMAH TANGGA",
            'content_link' : 'KLASIFIKASI',
            'user_groups': user_groups,
            "data_prediksi": prediksi_obj,
        }
        return render(request, 'klasifikasi/laporanPrediksi.html', context)
    except Prediksi.DoesNotExist:
        context = {
            "title": "KLASIFIKASI",
            "content_header": "HASIL PREDIKSI RUMAH TANGGA",
            'content_link' : 'KLASIFIKASI',
            'user_groups': user_groups,
            "data_prediksi": None,
        }
        return render(request, 'klasifikasi/laporanPrediksi.html', context)
    except Exception as e:
        context = {
            "title": "KLASIFIKASI",
            "content_header": "HASIL PREDIKSI RUMAH TANGGA",
            'content_link' : 'KLASIFIKASI',
            'user_groups': user_groups,
            "error_message": str(e),
        }
        return render(request, 'klasifikasi/laporanPrediksi.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def modelView(request):
    user_groups = request.user.groups.all()
    context = {
            "title": "KLASIFIKASI",
            "content_header": "MODELING",
            'content_link' : 'KLASIFIKASI',
            'user_groups': user_groups,
    }
    return render(request, 'klasifikasi/modeling.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def loadDatasetCSV(request):
    user_groups = request.user.groups.all()
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')

        if csv_file is None:
            messages.error(request, "Tidak ada file CSV yang dipilih. Silakan pilih file CSV untuk diunggah.")
            return redirect('klasifikasi:modeling')

        # Baca file CSV dan simpan data ke database
        try:
            csv_reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
            headers = next(csv_reader, None)
            if headers:
                for row in csv_reader:
                    data_dict = dict(zip(headers, row))  # Menggabungkan label dengan nilai pada setiap baris
                    DataModeling.objects.create(
                        luas_lantai_tempat_tinggal=data_dict.get('luas_lantai_tempat_tinggal', ''),
                        jenis_lantai_tempat_tinggal=data_dict.get('jenis_lantai_tempat_tinggal', ''),
                        jenis_dinding_tempat_tinggal=data_dict.get('jenis_dinding_tempat_tinggal', ''),
                        fasilitas_buang_air_besar=data_dict.get('fasilitas_buang_air_besar', ''),
                        sumber_air_minum=data_dict.get('sumber_air_minum', ''),
                        sumber_penerangan_rumah=data_dict.get('sumber_penerangan_rumah', ''),
                        bahan_bakar_untuk_memasak=data_dict.get('bahan_bakar_untuk_memasak', ''),
                        jumlah_konsumsi_daging_susu_ayam_dalam_seminggu=data_dict.get('jumlah_konsumsi_daging_susu_ayam_dalam_seminggu', ''),
                        jumlah_makan_dalam_sehari=data_dict.get('jumlah_makan_dalam_sehari', ''),
                        jumlah_membeli_pakaian_baru_dalam_setahun=data_dict.get('jumlah_membeli_pakaian_baru_dalam_setahun', ''),
                        penghasilan_kepala_rumah_tangga=data_dict.get('penghasilan_kepala_rumah_tangga', ''),
                        pendidikan_kepala_rumah_tangga=data_dict.get('pendidikan_kepala_rumah_tangga', ''),
                        mampu_membayar_biaya_pengobatan=data_dict.get('mampu_membayar_biaya_pengobatan', ''),
                        memiliki_simpanan_aset=data_dict.get('memiliki_simpanan_aset', ''),
                        status_rumah_tangga=data_dict.get('status_rumah_tangga', '')
                    )
                messages.success(request, "Data berhasil disimpan")
                return redirect('klasifikasi:modeling')
            else:
                messages.error(request, "File CSV kosong. Silakan pilih file CSV dengan data yang valid.")
                return redirect('klasifikasi:modeling')
        except csv.Error:
            messages.error(request, "Terjadi kesalahan saat membaca file CSV. Pastikan format file CSV benar.")
            return redirect('klasifikasi:modeling')

    context = {
        "title": "KLASIFIKASI",
        "content_header": "LOAD DATA",
        'content_link': 'KLASIFIKASI',
        'user_groups': user_groups,
    }
    return render(request, 'klasifikasi/modeling.html', context)



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def tampilData(request):
    user_groups = request.user.groups.all()
    if request.method == 'GET':
        data = DataModeling.objects.all()
        if not data:
            messages.info(request, "Data tidak tersedia dalam database. Silakan tambahkan data terlebih dahulu.")
            return redirect('klasifikasi:modeling')

        request.session['data'] = list(data.values())
        context = {
            "title": "KLASIFIKASI",
            "content_header": "LOAD DATA",
            'content_link': 'KLASIFIKASI',
            'user_groups': user_groups,
            'data': data
        }
        return render(request, 'klasifikasi/modeling.html', context)

    

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def splitData(request):
    user_groups = request.user.groups.all()
    if request.method == 'GET':
        data = request.session.get('data')
        df = pd.DataFrame(data)
        
        # pisahkan feature dan label
        X = df.drop(columns='status_rumah_tangga')
        y = df['status_rumah_tangga']
        
        # split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=2)
        
        data_training = pd.concat([X_train, y_train], axis=1)
        data_testing = pd.concat([X_test, y_test], axis=1)
        
    context = {
            'title': "KLASIFIKASI",
            'content_header': "SPLIT DATA",
            'content_link' : 'KLASIFIKASI',
            'user_groups': user_groups,
            'data_training' : data_training,
            'data_testing' : data_testing
        }
    return render(request, 'klasifikasi/splitdata.html', context)
    
    
@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def latihModel(request):
    user_groups = request.user.groups.all()
    if request.method == "GET":
        data = request.session.get('data')
        df = pd.DataFrame(data)
        
        # drop kolom yang tidak dibutuhkan
        df.drop(['id'], axis=1, inplace=True)

        # memisahkan label dan fitur
        X = df.drop(columns='status_rumah_tangga')
        y = df['status_rumah_tangga']

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=2)

        # Pipeline preprocessing
        # numerik features
        numeric_features = ['luas_lantai_tempat_tinggal', 'penghasilan_kepala_rumah_tangga']
        numeric_transformer = StandardScaler()
        # ordinal feature
        ordinal_features = ['jenis_lantai_tempat_tinggal', 'jenis_dinding_tempat_tinggal', 'fasilitas_buang_air_besar','sumber_penerangan_rumah', 'bahan_bakar_untuk_memasak', 'jumlah_konsumsi_daging_susu_ayam_dalam_seminggu','jumlah_makan_dalam_sehari', 'jumlah_membeli_pakaian_baru_dalam_setahun', 'pendidikan_kepala_rumah_tangga']
        ordinal_transformer = OrdinalEncoder()
        # nominal features
        nominal_features = ['sumber_air_minum','mampu_membayar_biaya_pengobatan', 'memiliki_simpanan_aset']
        nominal_transformer = OneHotEncoder()
        # ColumnTransformer untuk menggabungkan preprocessor fitur numerik dan kategori
        preprocessor = ColumnTransformer(
            transformers=[
                    ('numeric', numeric_transformer, numeric_features),
                    ('ordinal', ordinal_transformer, ordinal_features),
                    ('nominal', nominal_transformer, nominal_features)
                ])
        # modeling
        svm = SVC()
        pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('svm', svm)])
        pipeline.fit(X_train, y_train)
        # evaluasi model dengan melihat akurasi
        y_train_pred_svm = pipeline.predict(X_train)
        akurasi_data_training_svm = accuracy_score(y_train_pred_svm, y_train)
        laporan_klasifikasi_data_train_svm = classification_report(y_train_pred_svm, y_train)
        cm_data_training_svm = confusion_matrix(y_train, y_train_pred_svm)


        # confusion matrx data training
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(cm_data_training_svm, annot=True, fmt='d', cmap='Blues')
        plt.xlabel('Prediksi')
        plt.ylabel('Aktual')
        plt.title('Confusion Matrix - Data Training')
        
        # simpan plot untuk di buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plot_data_svm = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        
        
        

        # prediksi data testing
        y_test_pred_svm = pipeline.predict(X_test)
        akurasi_data_testing_svm = accuracy_score(y_test_pred_svm, y_test)
        laporan_klasifikasi_data_testing_svm = classification_report(y_test_pred_svm, y_test)
        cm_data_testing_svm = confusion_matrix(y_test, y_test_pred_svm)

        # confusion matrix data testing
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(cm_data_testing_svm, annot=True, fmt='d', cmap='Blues')
        plt.xlabel('Prediksi')
        plt.ylabel('Aktual')
        plt.title('Confusion Matrix - Data Testing')

        # Save the plot to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plot_data_test_svm = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        # akhir bagian svm


        # mencari parameter terbaik untuk svm
        param_grid = {
            'svm__C': [0.001, 0.01, 0.1, 1, 10, 100],
            'svm__kernel': ['linear', 'rbf', 'poly'],
            'svm__gamma': [0.1, 0.01, 0.001],
        }

        grid_search = GridSearchCV(estimator=pipeline, param_grid=param_grid, cv=10)
        grid_search.fit(X_train, y_train)
        best_params = grid_search.best_params_
        
        # latih data dengan best parameter
        best_model = grid_search.best_estimator_
        best_model.fit(X_train, y_train)


        # evaluasi model dengan melihat akurasi data training
        y_train_pred = best_model.predict(X_train)
        akurasi_data_training = accuracy_score(y_train_pred, y_train)
        laporan_klasifikasi_data_train = classification_report(y_train_pred, y_train)
        cm_data_training = confusion_matrix(y_train, y_train_pred)

        # plot untuk confussion matrix data training
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(cm_data_training, annot=True, fmt='d', cmap='Blues')
        plt.xlabel('Prediksi')
        plt.ylabel('Aktual')
        plt.title('Confusion Matrix - Data Training')
        
        # Save the plot to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()

        #prediksi dengan menggunakan data testing
        y_test_pred = best_model.predict(X_test)
        akurasi_data_testing = accuracy_score(y_test_pred, y_test)
        laporan_klasifikasi_data_testing = classification_report(y_test_pred, y_test)
        cm_data_testing = confusion_matrix(y_test, y_test_pred)

        # Plot confusion matrix untuk data testing
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(cm_data_testing, annot=True, fmt='d', cmap='Blues')
        plt.xlabel('Prediksi')
        plt.ylabel('Aktual')
        plt.title('Confusion Matrix - Data Testing')

        # Save the plot to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plot_data_test = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()


        # Encode the trained model to a base64 string
        encoded_model = base64.b64encode(pickle.dumps(best_model)).decode('utf-8')
        # Save the encoded model to session
        request.session['trained_model'] = encoded_model

    context = {
            "title": "KLASIFIKASI",
            "content_header": "MODELING",
            'content_link' : 'KLASIFIKASI',
            'user_groups': user_groups,
            'best_params': best_params,
            'akurasi_data_training_svm': akurasi_data_training_svm,
            'laporan_klasifikasi_data_train_svm': laporan_klasifikasi_data_train_svm,
            'akurasi_data_testing_svm': akurasi_data_testing_svm,
            'laporan_klasifikasi_data_testing_svm': laporan_klasifikasi_data_testing_svm,
            'akurasi_data_training': akurasi_data_training,
            'laporan_klasifikasi_data_train': laporan_klasifikasi_data_train,
            'akurasi_data_testing': akurasi_data_testing,
            'laporan_klasifikasi_data_testing': laporan_klasifikasi_data_testing,
            'plot_data_svm': plot_data_svm,
            'plot_data_test_svm': plot_data_test_svm,
            'plot_data': plot_data,
            'plot_data_test': plot_data_test,
        }

    return render(request, 'klasifikasi/latihModel.html', context)



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def simpanModel(request):
    user_groups = request.user.groups.all()
    if request.method == 'GET':
        # Decode the base64 string to retrieve the trained model
        encoded_model = request.session['trained_model']
        trained_model = pickle.loads(base64.b64decode(encoded_model.encode('utf-8')))

        # Save the model to the SVMModel model
        svm_model = SVMModel()
        svm_model.save_model(trained_model)

        messages.success(request, 'Model Berhasil Disimpan')
        return redirect('klasifikasi:modeling')






@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def prediksi(request, prediksi_id):
    try:
        data_survey_rumah_tangga = get_object_or_404(SurveyRumahTangga, pk=prediksi_id)
        model_path = os.path.join(settings.BASE_DIR, 'svm_models', 'svm_model_20230714124345_yQJqoJaQ.pkl')
        try:
            with open(model_path, 'rb') as file:
                model = pickle.load(file)
        except FileNotFoundError:
            messages.error(request, "Model file not found.")
            return redirect('klasifikasi:index')  
        columns = [
            'luas_lantai_tempat_tinggal',
            'jenis_lantai_tempat_tinggal',
            'jenis_dinding_tempat_tinggal',
            'fasilitas_buang_air_besar',
            'sumber_air_minum',
            'sumber_penerangan_rumah',
            'bahan_bakar_untuk_memasak',
            'jumlah_konsumsi_daging_susu_ayam_dalam_seminggu',
            'jumlah_makan_dalam_sehari',
            'jumlah_membeli_pakaian_baru_dalam_setahun',
            'penghasilan_kepala_rumah_tangga',
            'pendidikan_kepala_rumah_tangga',
            'mampu_membayar_biaya_pengobatan',
            'memiliki_simpanan_aset'
        ]
        features = [
            data_survey_rumah_tangga.luas_lantai_tempat_tinggal,
            data_survey_rumah_tangga.jenis_lantai_tempat_tinggal,
            data_survey_rumah_tangga.jenis_dinding_tempat_tinggal,
            data_survey_rumah_tangga.fasilitas_buang_air_besar,
            data_survey_rumah_tangga.sumber_air_minum,
            data_survey_rumah_tangga.sumber_penerangan_rumah,
            data_survey_rumah_tangga.bahan_bakar_untuk_memasak,
            data_survey_rumah_tangga.jumlah_konsumsi_daging_susu_ayam_dalam_seminggu,
            data_survey_rumah_tangga.jumlah_makan_dalam_sehari,
            data_survey_rumah_tangga.jumlah_membeli_pakaian_baru_dalam_setahun,
            data_survey_rumah_tangga.penghasilan_kepala_rumah_tangga,
            data_survey_rumah_tangga.pendidikan_kepala_rumah_tangga,
            data_survey_rumah_tangga.mampu_membayar_biaya_pengobatan,
            data_survey_rumah_tangga.memiliki_simpanan_aset,
        ]
        data_df = pd.DataFrame([features], columns=columns)
        prediction = model.predict(data_df)
        prediction = prediction[0]
        data_survey_rumah_tangga.prediction = prediction
        data_survey_rumah_tangga.predicted = True
        data_survey_rumah_tangga.save()
        prediksi_obj = Prediksi(survey_rumah_tangga=data_survey_rumah_tangga, prediction=prediction)
        prediksi_obj.save()
        return redirect('klasifikasi:laporanPrediksi')
    except SurveyRumahTangga.DoesNotExist:
        messages.error(request, "Survey not found.")
        return redirect('klasifikasi:index') 
    except FileNotFoundError:
        messages.error(request, "Model file not found.")
        return redirect('klasifikasi:index')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('klasifikasi:index') 



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def index(request):
    user_groups = request.user.groups.all()
    # Get the list of predicted record IDs
    predicted_ids = Prediksi.objects.values_list('survey_rumah_tangga_id', flat=True)

    # Fetch the survey data excluding the predicted records
    data_survey_rumah_tangga = SurveyRumahTangga.objects.exclude(id__in=predicted_ids).order_by('-id')

    context = {
        "title": "KLASIFIKASI",
        "content_header": "PREDIKSI",
        'content_link' : 'KLASIFIKASI',
        'user_groups': user_groups,
        "data_survey_rumah_tangga": data_survey_rumah_tangga,
    }

    if not data_survey_rumah_tangga:
        messages.info(request, "Tidak ada data yang bisa diprediksi.")

    return render(request, 'klasifikasi/index.html', context)

