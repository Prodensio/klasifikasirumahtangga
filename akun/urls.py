from django.urls import path
from . import views

# create your urls
app_name = "akun"
urlpatterns = [
    path('detail/<int:detail_id>', views.userDetail, name='detail'),
    path('edit/<int:edit_id>', views.editUser, name='editUser'),
    path('profil/<int:profil_id>', views.profil, name='profil'),
    path('editProfil/<int:edit_profil_id>', views.editProfil, name='editProfil'),
    path('delete/<int:delete_id>', views.deleteUser, name='delete'),
    path('logout/',views.logoutView, name='logout'),
    path('akun/',views.index, name='index'),
    path('create/', views.createUser, name='create'),
    path('group/create/', views.createGroup, name='create_group'),
    path('permission/create/', views.createPermission, name='create_permission'),
    path('group/list/', views.groupList, name='group_list'),
    path('permission/list/', views.permissionList, name='permission_list'),
    path('',views.loginView, name='login'),
]