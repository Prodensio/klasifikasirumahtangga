from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, Permission
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserForm, LoginForm, GroupForm, PermissionForm, EditProfileForm
from .models import User



# Create your views here.
def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if user.groups.filter(name='Admin').exists():
                    return redirect('home:indexAdmin')
                elif user.groups.filter(name='Operator').exists():
                    return redirect('home:indexOperator')
                elif user.groups.filter(name='Penduduk').exists():
                    return redirect('home:indexPenduduk')  
            else:
                form.add_error(None, 'Kombinasi email dan kata sandi tidak valid.')
    else:
        form = LoginForm()
    return render(request, 'akun/login.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def createGroup(request):
    user_groups = request.user.groups.all()
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('akun:group_list')
    else:
        form = GroupForm()
    context = {
        'title' : 'AKUN',
        'content_header' : 'TAMBAH GRUP',
        'content_link' : 'USER',
        'user_groups': user_groups,
        'form': form,
    }
    return render(request, 'akun/create_group.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def createPermission(request):
    user_groups = request.user.groups.all()
    if request.method == 'POST':
        form = PermissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('akun:permission_list')
    else:
        form = PermissionForm()
    
    context = {
        'title' : 'AKUN',
        'content_header' : 'TAMBAH PERMISSIONS',
        'content_link' : 'USER',
        'user_groups': user_groups,
        'form': form,
    }
    return render(request, 'akun/create_permission.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def groupList(request):
    user_groups = request.user.groups.all()
    groups = Group.objects.all()
    context = {
        'title' : 'AKUN',
        'content_header' : 'GRUPS',
        'content_link' : 'USER',
        'user_groups': user_groups,
        'groups': groups,
    }
    return render(request, 'akun/group_list.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def permissionList(request):
    user_groups = request.user.groups.all()
    permissions = Permission.objects.all()
    context = {
        'title' : 'AKUN',
        'content_header' : 'PERMISSIONS',
        'content_link' : 'USER',
        'user_groups': user_groups,
        'permissions': permissions,
    }
    return render(request, 'akun/permission_list.html', context)



@login_required
def logoutView(request):
    logout(request)
    return redirect('akun:login') 



@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def deleteUser(request, delete_id):
    hapus = get_object_or_404(User, id=delete_id)
    hapus.delete()
    messages.success(request, 'Data user berhasil dihapus.', extra_tags='success')
    return redirect('akun:index')



@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def createUser(request):
    user_groups = request.user.groups.all()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            selected_groups = form.cleaned_data.get('groups')
            user.groups.set(selected_groups)
            user.is_active = form.cleaned_data.get('is_active')
            user.is_staff = form.cleaned_data.get('is_staff')
            user.save()
            
            return redirect('akun:index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = UserForm()
    
    context = {
        'title' : 'AKUN',
        'content_header' : 'BUAT AKUN',
        'content_link' : 'USER',
        'user_groups': user_groups,
        'form': form,
    }
    return render(request, 'akun/create.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator', 'Penduduk']).exists())
def userDetail(request, detail_id):
    user_groups = request.user.groups.all()
    user_detail = User.objects.get(id=detail_id)
    context = {
        'title' : 'AKUN',
        'content_header' : 'PROFIL',
        'content_link' : 'USER',
        'user_groups' : user_groups,
        'user_detail': user_detail,
    }
    return render(request, 'akun/detail.html', context)

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator', 'Penduduk']).exists())
def profil(request, profil_id):
    user_groups = request.user.groups.all()
    profil_user = User.objects.get(id=profil_id)
    context = {
        'title' : 'AKUN',
        'content_header' : 'PROFIL',
        'content_link' : 'USER',
        'user_groups' : user_groups,
        'profil_user': profil_user,
    }
    return render(request, 'akun/profil.html', context)



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator', 'Penduduk']).exists())
def editProfil(request, edit_profil_id):
    user_groups = request.user.groups.all()
    edit_profil_user = User.objects.get(id=edit_profil_id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=edit_profil_user, user_groups=user_groups)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            else:
                user.password = User.objects.get(pk=edit_profil_user.pk).password
            user.save()
            messages.success(request, 'Data profil berhasil diupdate.', extra_tags='success')
            return redirect('akun:profil', profil_id=edit_profil_user.id)
    else:
        form = EditProfileForm(instance=edit_profil_user, user_groups=user_groups)

    context = {
        'title': 'AKUN',
        'content_header': 'UPDATE AKUN',
        'content_link': 'USER',
        'user_groups': user_groups,
        'form': form,
        'edit_profil_user': edit_profil_user,
    }
    return render(request, 'akun/editProfil.html', context)













@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Admin', 'Operator', 'Penduduk']).exists())
def editUser(request, edit_id):
    user_groups = request.user.groups.all()
    data_edit_user = User.objects.get(id=edit_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=data_edit_user)
        if form.is_valid():
            data_edit_user = form.save(commit=False)
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1:
                data_edit_user.set_password(password1)
            data_edit_user.save()
            selected_groups = form.cleaned_data.get('groups')
            data_edit_user.groups.set(selected_groups)
            # Lakukan tindakan yang sesuai setelah pengguna berhasil diperbarui
            messages.success(request, 'Data user berhasil diubah.', extra_tags='success')
            return redirect('akun:index')
    else:
        form = UserForm(instance=data_edit_user, initial={'password1': data_edit_user.password, 'password2': data_edit_user.password})

    context = {
        'title': 'AKUN',
        'content_header': 'UPDATE AKUN',
        'content_link': 'USER',
        'user_groups': user_groups,
        'form': form,
        'edit_user': data_edit_user,
    }
    return render(request, 'akun/editUser.html', context)



@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def index(request):
    user_groups = request.user.groups.all()
    data_user = User.objects.all().order_by('-id')
    context = {
        'title' : 'AKUN',
        'content_header' : 'DAFTAR AKUN',
        'content_link' : 'USER',
        'data_user': data_user,
        'user_groups': user_groups,
    }
    return render(request, 'akun/index.html',context)
