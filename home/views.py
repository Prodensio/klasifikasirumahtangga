from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test








# Create your views here.
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def indexAdmin(request):
    user_groups = request.user.groups.all()
    context = {
        "title": "Home",
        "content_header": "HOME ADMIN",
        "user_groups": user_groups,
    }
    return render(request, 'home/indexAdmin.html', context)



@login_required
@user_passes_test(lambda u: u.groups.filter(name='Operator').exists())
def indexOperator(request):
    user_groups = request.user.groups.all()
    context = {
        "title": "Home",
        "content_header": "HOME OPERATOR",
        "user_groups": user_groups,
    }
    return render(request, 'home/indexOperator.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Penduduk').exists())
def indexPenduduk(request):
    user_groups = request.user.groups.all()
    context = {
        "title": "HOME",
        "content_header": "HOME PENDUDUK",
        "content_link" : "HOME",
        "user_groups": user_groups,
    }
    return render(request, 'home/indexPenduduk.html', context)


# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='Penduduk').exists())
# def cariPenduduk(request):
#     keyword = request.GET.get('keyword', '')
#     penduduk = []
    
#     if keyword:
#         penduduk = Penduduk.objects.filter(nama_penduduk__icontains=keyword)
    
#     context = {
#         'penduduk': penduduk,
#         'keyword': keyword
#     }
    
#     return render(request, 'home/cariDataPenduduk.html', context)



