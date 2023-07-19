from django.shortcuts import render, redirect, get_object_or_404
from .models import SurveyPenduduk, SurveyRumahTangga
from .forms import FormSurveyPenduduk, FormSurveyRumahTangga
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.
@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def editDataSurveyPenduduk(request, edit_id):
    user_groups = request.user.groups.all()
    edit_data_survey_penduduk = SurveyPenduduk.objects.get(pk=edit_id)
    form_edit_data_survey_penduduk = FormSurveyPenduduk(request.POST or None, instance=edit_data_survey_penduduk)
    if form_edit_data_survey_penduduk.is_valid():
        form_edit_data_survey_penduduk.save()
        messages.success(request, 'Data survey penduduk berhasil dirubah.', extra_tags='success')
        return redirect('survey:index')
    context = {
        "title": "SURVEI",
        "content_header": "EDIT SURVEI PENDUDUK",
        'content_link' : 'SURVEI',
        'user_groups': user_groups,
        "form_edit_data_survey_penduduk": form_edit_data_survey_penduduk,
    }
    return render(request, 'survey/editDataSurveyPenduduk.html', context)



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def editDataSurveyRumahTangga(request, edit_id):
    user_groups = request.user.groups.all()
    edit_data_survey_rumah_tangga = SurveyRumahTangga.objects.get(pk=edit_id)
    form_edit_data_survey_rumah_tangga = FormSurveyRumahTangga(request.POST or None, instance=edit_data_survey_rumah_tangga)
    if form_edit_data_survey_rumah_tangga.is_valid():
        form_edit_data_survey_rumah_tangga.save()
        messages.success(request, 'Data survey rumah tangga berhasil dirubah.', extra_tags='success')
        return redirect('survey:index')
    context = {
        "title": "SURVEI",
        "content_header": "EDIT SURVEI RUMAH TANGGA",
        'content_link' : 'SURVEI',
        'user_groups': user_groups,
        "form_edit_data_survey_rumah_tangga": form_edit_data_survey_rumah_tangga,
    }
    return render(request, 'survey/editDataSurveyRumahTangga.html', context)



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def hapusDataSurveyPenduduk(request, hapus_id):
    user_groups = request.user.groups.all()
    hapus = SurveyPenduduk.objects.get(pk=hapus_id)
    if request.method == 'POST':
        hapus.delete()
        messages.success(request, 'Data penduduk berhasil dihapus.', extra_tags='success')
        return redirect('survey:index')
    context = {
        'data': hapus,
        'user_groups': user_groups,
    }
    return render(request, 'survey/hapusDataSurveyPenduduk.html', context)



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def hapusDataSurveyRumahTangga(request, hapus_id):
    user_groups = request.user.groups.all()
    data = get_object_or_404(SurveyRumahTangga, pk=hapus_id)
    if request.method == 'POST':
        data.delete()
        messages.success(request, 'Data rumah tangga berhasil dihapus.', extra_tags='success')
        return redirect('survey:index')
    context = {
        'data': data,
        'user_groups': user_groups,
    }
    return render(request, 'survey/hapusDataSurveyRumahTangga.html', context)



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator', 'Penduduk']).exists())
def tambahDataSurveyPenduduk(request):
    user_groups = request.user.groups.all()
    form_tambah_data_survey_penduduk = FormSurveyPenduduk()
    if request.method == 'POST':
        form_tambah_data_survey_penduduk = FormSurveyPenduduk(request.POST)
        if form_tambah_data_survey_penduduk.is_valid():
            form_tambah_data_survey_penduduk.save()
            if request.user.groups.filter(name='Penduduk').exists():
                messages.success(request, 'Survey penduduk berhasil ditambahkan.')
                return redirect('home:indexPenduduk')
            else:
                messages.success(request, 'Survey penduduk berhasil ditambahkan.')
                return redirect('survey:index')
    active_tab = 'penduduk'
    context = {
        "title": "SURVEI",
        "content_header": "SURVEI PENDUDUK",
        'content_link' : 'SURVEI',
        'user_groups': user_groups,
        "form_tambah_data_survey_penduduk": form_tambah_data_survey_penduduk,
        "active_tab": active_tab,
    }
    return render(request, 'survey/tambahSurveyPenduduk.html', context)



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator', 'Penduduk']).exists())
def tambahDataSurveyRumahTangga(request):
    user_groups = request.user.groups.all()
    form_tambah_data_survey_rumah_tangga = FormSurveyRumahTangga()
    if request.method == 'POST':
        form_tambah_data_survey_rumah_tangga = FormSurveyRumahTangga(request.POST)
        if form_tambah_data_survey_rumah_tangga.is_valid():
            form_tambah_data_survey_rumah_tangga.save()
            if request.user.groups.filter(name='Penduduk').exists():
                messages.success(request, 'Survey rumah tangga berhasil ditambahkan.')
                return redirect('home:indexPenduduk')  
            else:
                messages.success(request, 'Survey rumah tangga berhasil ditambahkan.')
                return redirect('survey:index')  
    context = {
        "title": "SURVEY",
        "content_header": "SURVEI RUMAH TANGGA",
        'content_link' : 'SURVEI',
        'user_groups': user_groups,
        "form_tambah_data_survey_rumah_tangga": form_tambah_data_survey_rumah_tangga,
    }
    return render(request, 'survey/tambahSurveyRumahTangga.html', context)



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def index(request):
    user_groups = request.user.groups.all()
    data_survey_penduduk = SurveyPenduduk.objects.all().order_by('-id')
    data_survey_rumah_tangga = SurveyRumahTangga.objects.all().order_by('-id')
    context = {
        "title": "SURVEI",
        "content_header": "DATA SURVEI PENDUDUK DAN RUMAH TANGGA",
        'content_link' : 'SURVEI',
        'user_groups': user_groups,
        "data_survey_penduduk" : data_survey_penduduk,
        "data_survey_rumah_tangga" : data_survey_rumah_tangga,
    }
    return render(request, 'survey/index.html', context)