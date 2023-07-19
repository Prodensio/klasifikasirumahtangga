from django.shortcuts import render, redirect, get_object_or_404
from .models import RumahTangga, AnggotaRumahTangga, BantuanRumahTangga
from penduduk.models import Penduduk
from .forms import FormRumahTangga, FormAnggotaRumahTangga, FormBantuanRumahTangga
from openpyxl import Workbook
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required, user_passes_test




# create your views here
@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def hapusData(request, hapus_id):
    hapus = RumahTangga.objects.get(pk=hapus_id)
    hapus.delete()
    messages.success(request, 'Data rumah tangga berhasil dihapus.', extra_tags='success')
    return redirect('rumahtangga:index')



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def hapusAnggotaRumahTangga(request, rumah_tangga_id, hapus_id):
    rumah_tangga = get_object_or_404(RumahTangga, pk=rumah_tangga_id)
    anggota = get_object_or_404(AnggotaRumahTangga, pk=hapus_id)
    if anggota == rumah_tangga.anggota_rumah_tangga.first():
        rumah_tangga.delete()
        messages.success(request, 'Data anggota rumah tangga berhasil dihapus.', extra_tags='success')
        return redirect('rumahtangga:index')
    else:
        anggota.delete()
        messages.success(request, 'Data anggota rumah tangga berhasil dihapus.', extra_tags='success')
        return redirect('rumahtangga:detail', rumah_tangga_id=rumah_tangga_id)



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def editData(request, edit_id):
    user_groups = request.user.groups.all()
    edit_data = RumahTangga.objects.get(pk=edit_id)
    form_edit_data = FormRumahTangga(request.POST or None, instance=edit_data)
    if form_edit_data.is_valid():
        form_edit_data.save()
        messages.success(request, 'Data rumah tangga berhasil dirubah.', extra_tags='success')
        return redirect('rumahtangga:detail', rumah_tangga_id=edit_id)
    context = {
        "title": "RUMAH TANGGA",
        "content_header": "EDIT RUMAH TANGGA",
        'content_link' : 'RUMAH TANGGA',
        'user_groups': user_groups,
        "form_edit_data": form_edit_data,
    }
    return render(request, 'rumahtangga/editData.html', context)



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def tambahData(request):
    user_groups = request.user.groups.all()
    penduduk_terpilih = Penduduk.objects.exclude(
        Q(anggota_rumah_tangga__hubungan_dalam_rumah_tangga='ANGGOTA RUMAH TANGGA') |
        Q(anggota_rumah_tangga__hubungan_dalam_rumah_tangga='KEPALA RUMAH TANGGA')
    )
    if request.method == 'POST':
        form_tambah_data = FormRumahTangga(request.POST)
        if form_tambah_data.is_valid():
            rumah_tangga = form_tambah_data.save(commit=False)
            kepala_rumah_tangga = rumah_tangga.kepala_rumah_tangga
            if not RumahTangga.objects.filter(
                Q(kepala_rumah_tangga=kepala_rumah_tangga) |
                Q(anggota_rumah_tangga__penduduk=kepala_rumah_tangga)
            ).exists():
                rumah_tangga.save()
                anggota_rumah_tangga = AnggotaRumahTangga.objects.create(
                    rumah_tangga=rumah_tangga,
                    penduduk=kepala_rumah_tangga,
                    hubungan_dalam_rumah_tangga='KEPALA RUMAH TANGGA'
                )
                messages.success(request, 'Data rumah tangga berhasil ditambahkan.', extra_tags='success')
                return redirect('rumahtangga:index')
            else:
                messages.warning(request, 'Penduduk tersebut sudah menjadi kepala atau anggota rumah tangga.', extra_tags='warning')
    else:
        form_tambah_data = FormRumahTangga()
        form_tambah_data.fields['kepala_rumah_tangga'].queryset = penduduk_terpilih
    context = {
        "title": "RUMAH TANGGA",
        "content_header": "RUMAH TANGGA BARU",
        'content_link' : 'RUMAH TANGGA',
        'user_groups': user_groups,
        "form_tambah_data": form_tambah_data,
    }
    return render(request, 'rumahtangga/tambahData.html', context)



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def bantuanRumahTangga(request):
    user_groups = request.user.groups.all()
    bantuan_rumah_tangga = BantuanRumahTangga.objects.all().order_by('-id')
    context = {
        "title": "RUMAH TANGGA",
        "content_header": "BANTUAN RUMAH TANGGA",
        'content_link' : 'BANTUAN RUMAH TANGGA',
        'user_groups': user_groups,
        "bantuan_rumah_tangga": bantuan_rumah_tangga,
    }
    return render(request, 'rumahtangga/bantuan.html', context)



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def tambahBantuanRumahTangga(request):
    user_groups = request.user.groups.all()
    rumah_tangga = RumahTangga.objects.all()
    if request.method == 'POST':
        form = FormBantuanRumahTangga(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rumahtangga:bantuan')
    else:
        form = FormBantuanRumahTangga()
        
    context = {
        "title": "RUMAH TANGGA",
        "content_header": "BANTUAN RUMAH TANGGA",
        'content_link' : 'BANTUAN RUMAH TANGGA',
        'user_groups': user_groups,
        "form_tambah_data_bantuan_rumah_tangga": form,
        "rumah_tangga": rumah_tangga,
    }
    return render(request, 'rumahtangga/tambahBantuan.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def hapusDataBantuan(request, hapus_bantuan_id):
    hapus = BantuanRumahTangga.objects.get(pk=hapus_bantuan_id)
    hapus.delete()
    messages.success(request, 'Data bantuan berhasil dihapus.', extra_tags='success')
    return redirect('rumahtangga:bantuan')





@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def tambahAnggotaRumahTangga(request, tambah_anggota_id):
    user_groups = request.user.groups.all()
    rumah_tangga = RumahTangga.objects.get(pk=tambah_anggota_id)
    penduduk_terpilih = Penduduk.objects.exclude(
        Q(anggota_rumah_tangga__rumah_tangga=rumah_tangga) |
        Q(anggota_rumah_tangga__hubungan_dalam_rumah_tangga='KEPALA RUMAH TANGGA') |
        Q(anggota_rumah_tangga__hubungan_dalam_rumah_tangga='ANGGOTA RUMAH TANGGA')
    )
    if request.method == 'POST':
        form = FormAnggotaRumahTangga(request.POST)
        if form.is_valid():
            anggota_rumah_tangga = form.save(commit=False)
            anggota_rumah_tangga.rumah_tangga = rumah_tangga
            anggota_rumah_tangga.hubungan_dalam_rumah_tangga = 'ANGGOTA RUMAH TANGGA'
            anggota_rumah_tangga.save()
            messages.success(request, 'Data anggota rumah tangga berhasil ditambahkan.', extra_tags='success')
            return redirect('rumahtangga:detail', rumah_tangga_id=rumah_tangga.id)
    else:
        form = FormAnggotaRumahTangga()
    form.fields['penduduk'].queryset = penduduk_terpilih
    if not penduduk_terpilih:  
        messages.warning(request, "Tidak ada penduduk tersedia untuk ditambahkan sebagai anggota rumah tangga.")
    context = {
        "title": "RUMAH TANGGA",
        "content_header": "TAMBAH ANGGOTA RUMAH TANGGA",
        'content_link' : 'RUMAH TANGGA',
        'user_groups': user_groups,
        "form_tambah_data_anggota_rumah_tangga": form,
        "rumah_tangga": rumah_tangga,
    }
    return render(request, 'rumahtangga/tambahAnggotaRumahTangga.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator','Penduduk']).exists())
def detailRumahTangga(request, rumah_tangga_id):
    user_groups = request.user.groups.all()
    rumah_tangga = get_object_or_404(RumahTangga, id=rumah_tangga_id)
    anggota_rumah_tangga = rumah_tangga.anggota_rumah_tangga.all()
    jumlah_anggota_rumah_tangga = anggota_rumah_tangga.count()
    context = {
        "title": "RUMAH TANGGA",
        "content_header": "PROFIL RUMAH TANGGA",
        'content_link' : 'RUMAH TANGGA',
        'user_groups': user_groups,
        "rumah_tangga": rumah_tangga,
        "anggota_rumah_tangga": anggota_rumah_tangga,
        "jumlah_anggota_rumah_tangga": jumlah_anggota_rumah_tangga,
    }
    if user_groups.filter(name='Penduduk').exists():
        return render(request, 'rumahtangga/detailRumahTanggaPenduduk.html', context)
    else:
        return render(request, 'rumahtangga/detailRumahTangga.html', context)



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def cariData(request):
    user_groups = request.user.groups.all()
    keyword = request.GET.get('keyword', '')
    rumah_tangga = RumahTangga.objects.filter(kepala_rumah_tangga__nama_penduduk__icontains=keyword)
    context = {
        "title": "RUMAH TANGGA",
        'content_link' : 'RUMAH TANGGA',
        'user_groups': user_groups,
        'rumah_tangga': rumah_tangga,
        'keyword': keyword
    }
    return render(request, 'rumahtangga/index.html', context)



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def exportDataToExel(request):
    data_rumah_tangga = RumahTangga.objects.all()
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append([
        'dusun',
        'rt',
        'no_rumah_tangga',
        'no_kartu_keluarga',
        'kepala_rumah_tangga',
        'nik_kepala_rumah_tangga',
        'pekerjaan_kepala_rumah_tangga',
        'penghasilan_kepala_rumah_tangga',
        'pendidikan_kepala_rumah_tangga',
        'alamat_rumah_tangga',
        'jumlah_anggota_rumah_tangga',
        'status_kepemilikan_tempat_tinggal',
        'luas_lantai_tempat_tinggal',
        'jenis_lantai_tempat_tinggal',
        'jenis_dinding_tempat_tinggal',
        'jenis_atap_tempat_tinggal',
        'fasilitas_buang_air_besar',
        'jenis_penerangan_rumah',
        'energi_untuk_memasak',
        'jumlah_konsumsi_daging_susu_telur_dalam_seminggu',
        'jumlah_membeli_pakaian_sekali_dalam_setahun',
        'jumlah_makan_dalam_sehari',
        'mampu_membayar_biaya_pengobatan',
        'sumber_air_minum',
        'memiliki_simpanan_aset',
        'status_rumah_tangga',
    ])
    for rumah_tangga in data_rumah_tangga:
        anggota_rumah_tangga = rumah_tangga.anggota_rumah_tangga.all()
        jumlah_anggota_rumah_tangga = anggota_rumah_tangga.count()
        worksheet.append([
            rumah_tangga.kepala_rumah_tangga.dusun,
            rumah_tangga.kepala_rumah_tangga.rt,
            rumah_tangga.no_rumah_tangga,
            rumah_tangga.kepala_rumah_tangga.no_kartu_keluarga,
            rumah_tangga.kepala_rumah_tangga.nama_penduduk,
            rumah_tangga.kepala_rumah_tangga.no_induk_kependudukan,
            rumah_tangga.kepala_rumah_tangga.pekerjaan,
            rumah_tangga.kepala_rumah_tangga.penghasilan,
            rumah_tangga.kepala_rumah_tangga.pendidikan,
            rumah_tangga.kepala_rumah_tangga.alamat,
            jumlah_anggota_rumah_tangga,
            rumah_tangga.status_kepemilikan_tempat_tinggal,
            rumah_tangga.luas_lantai_tempat_tinggal,
            rumah_tangga.jenis_lantai_tempat_tinggal,
            rumah_tangga.jenis_dinding_tempat_tinggal,
            rumah_tangga.jenis_atap_tempat_tinggal,
            rumah_tangga.fasilitas_buang_air_besar,
            rumah_tangga.jenis_penerangan_rumah,
            rumah_tangga.energi_untuk_memasak,
            rumah_tangga.jumlah_konsumsi_daging_susu_telur_dalam_seminggu,
            rumah_tangga.jumlah_membeli_pakaian_sekali_dalam_setahun,
            rumah_tangga.jumlah_makan_dalam_sehari,
            rumah_tangga.mampu_membayar_biaya_pengobatan,
            rumah_tangga.sumber_air_minum,
            rumah_tangga.memiliki_simpanan_aset,
            rumah_tangga.status_rumah_tangga,
        ])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=rumah_tangga.xlsx'
    workbook.save(response)
    return response



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def laporanRumahTangga(request):
    user_groups = request.user.groups.all()
    selected_year = request.GET.get('tahun')  
    if selected_year and not selected_year.isdigit():
        return HttpResponse("Pilih tahun yang valid.")
    rumah_tangga_miskin = RumahTangga.objects.none()  
    if selected_year:
        rumah_tangga_miskin = RumahTangga.objects.filter(tahun=selected_year, status_rumah_tangga='MISKIN').annotate(jumlah_anggota_rumah_tangga=Count('anggota_rumah_tangga'))
    tahun_list = RumahTangga.objects.values('tahun').annotate(total=Count('tahun')).order_by('-tahun')
    context = {
        "title": "Laporan Rumah Tangga Miskin",
        "content_header": "Laporan",
        'content_link' : 'RUMAH TANGGA',
        'user_groups': user_groups,
        "tahun_list": tahun_list,
        "selected_year": selected_year,
        "rumah_tangga_miskin": rumah_tangga_miskin,
    }
    return render(request, 'rumahtangga/laporanRumahTanggaMiskin.html', context)



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator']).exists())
def index(request):
    user_groups = request.user.groups.all()
    data_rumah_tangga = RumahTangga.objects.all().order_by('-id')
    context = {
        "title": "RUMAH TANGGA",
        "content_header": "DAFTAR RUMAH TANGGA",
        'content_link' : 'RUMAH TANGGA',
        'user_groups': user_groups,
        "rumah_tangga": data_rumah_tangga,
    }
    for rumah_tangga in data_rumah_tangga:
        rumah_tangga.jumlah_anggota_rumah_tangga = rumah_tangga.anggota_rumah_tangga.count()
    return render(request, 'rumahtangga/index.html', context)
