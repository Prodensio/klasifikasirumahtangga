from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Penduduk
from .forms import FormPenduduk
from openpyxl import Workbook
from django.http import HttpResponse
from rumahtangga.models import RumahTangga
from django.contrib.auth.decorators import login_required, user_passes_test



# create your views here
@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def hapusData(request, hapus_id):
    hapus = Penduduk.objects.get(pk=hapus_id)
    hapus.delete()
    messages.success(request, 'Data penduduk berhasil dihapus.', extra_tags='success')
    return redirect('penduduk:index')



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def editData(request, edit_id):
    user_groups = request.user.groups.all()
    edit_data = Penduduk.objects.get(pk=edit_id)
    form_edit_data = FormPenduduk(request.POST or None, instance=edit_data)
    if form_edit_data.is_valid():
        form_edit_data.save()
        messages.success(request, 'Data penduduk berhasil dirubah.', extra_tags='success')
        return redirect('penduduk:index')
    context = {
        "title": "PENDUDUK",
        "content_header": "EDIT DATA PENDUDUK",
        'content_link' : 'PENDUDUK',
        'user_groups': user_groups,
        "form_edit_data": form_edit_data,
    }
    return render(request, 'penduduk/editData.html', context)



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def tambahData(request):
    user_groups = request.user.groups.all()
    form_tambah_data = FormPenduduk(request.POST or None)
    if form_tambah_data.is_valid():
        form_tambah_data.save()
        messages.success(request, 'Data penduduk berhasil ditambahkan.', extra_tags='success')
        return redirect('penduduk:index')
    context = {
        "title": "PENDUDUK",
        "content_header": "TAMBAH DATA PENDUDUK",
        'content_link' : 'PENDUDUK',
        'user_groups': user_groups,
        "form_tambah_data": form_tambah_data,
    }
    return render(request, 'penduduk/tambahData.html', context)



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def exportDataToExel(request):
    data_penduduk = Penduduk.objects.all()
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append([
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
    ])
    for penduduk in data_penduduk:
        worksheet.append([
            penduduk.dusun,
            penduduk.rt,
            penduduk.no_kartu_keluarga,
            penduduk.no_induk_kependudukan,
            penduduk.nama_penduduk,
            penduduk.jenis_kelamin,
            penduduk.tempat_lahir,
            penduduk.tanggal_lahir,
            penduduk.alamat,
            penduduk.status_pernikahan,
            penduduk.agama,
            penduduk.no_hp,
            penduduk.pekerjaan,
            penduduk.penghasilan,
            penduduk.pendidikan,
            penduduk.hubungan_dalam_keluarga,
        ])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=penduduk.xlsx'
    response.flush()
    workbook.save(response)
    return response



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def lihatData(request, lihat_id):
    user_groups = request.user.groups.all()
    data_penduduk = get_object_or_404(Penduduk, pk=lihat_id)
    context = {
        "title": "PENDUDUK",
        "content_header": "DATA PENDUDUK",
        'content_link' : 'PENDUDUK',
        'user_groups': user_groups,
        "penduduk": data_penduduk
    }
    return render(request, 'penduduk/index.html', context)



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Penduduk']).exists())
def cariDataPenduduk(request):
    user_groups = request.user.groups.all()
    keyword = request.GET.get('keyword','')
    data_penduduk = Penduduk.objects.filter(nama_penduduk__icontains=keyword)
    context = {
        "title": "PENDUDUK",
        "content_header": "DATA PENDUDUK",
        'content_link' : 'PENDUDUK',
        'user_groups': user_groups,
        "penduduk": data_penduduk,
        'keyword' : keyword
    }
    return render(request, 'penduduk/cariDataPenduduk.html', context)






@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def cariData(request):
    keyword = request.GET.get('keyword', '')
    penduduk = Penduduk.objects.filter(nama_penduduk__icontains=keyword)
    context = {
        'penduduk': penduduk,
        'keyword': keyword
    }
    return render(request, 'penduduk/index.html', context)



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def detailRumahTangga(request, anggota_rumah_tangga_id):
    rumah_tangga = get_object_or_404(RumahTangga, id=anggota_rumah_tangga_id)
    return render(request, 'rumahtangga/detailRumahTangga.html', {'rumah_tangga': rumah_tangga})



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def index(request):
    user_groups = request.user.groups.all()
    data_penduduk = Penduduk.objects.prefetch_related('rumah_tangga__anggota_rumah_tangga').all().order_by('-id')
    context = {
        "title": "PENDUDUK",
        "content_header": "DATA PENDUDUK",
        'content_link' : 'PENDUDUK',
        'user_groups': user_groups,
        "penduduk": data_penduduk,
    }

    return render(request, 'penduduk/index.html', context)







