from django import forms
from .models import User
from django.contrib.auth.models import Group, Permission


# create your forms
class UserForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    groups = forms.ModelMultipleChoiceField(
        label='Groups',
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    # user_permissions = forms.ModelMultipleChoiceField(
    #     label='User Permissions',
    #     queryset=Permission.objects.all(),
    #     widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    # )
    is_active = forms.BooleanField(label='Is Active', initial=True, required=False)
    is_staff = forms.BooleanField(label='Is Staff', initial=False, required=False)
    
    class Meta:
        model = User
        # fields = ['email', 'first_name', 'last_name', 'groups', 'user_permissions', 'is_active', 'is_staff']
        fields = ['email', 'first_name', 'last_name', 'groups', 'is_active', 'is_staff']
        labels = {
            'email': 'Email',
            # 'user_permissions': 'User Permissions',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = self.cleaned_data['is_active']
        user.is_staff = self.cleaned_data['is_staff']
        if commit:
            user.save()
            self.save_m2m()  # Save ManyToMany fields (groups and user_permissions)
        return user
    
class EditProfileForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    is_active = forms.BooleanField(label='Is Active', initial=True, required=False)
    is_staff = forms.BooleanField(label='Is Staff', initial=False, required=False)
    groups = forms.ModelMultipleChoiceField(
        label='Groups',
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email', 'password', 'is_active', 'is_staff', 'groups']

    def __init__(self, *args, **kwargs):
        self.user_groups = kwargs.pop('user_groups', None)
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False

        if self.user_groups:
            if 'Operator' in self.user_groups or 'Penduduk' in self.user_groups:
                self.fields['is_active'].widget = forms.HiddenInput()
                self.fields['is_staff'].widget = forms.HiddenInput()
                self.fields['groups'].widget = forms.HiddenInput()

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        else:
            user.password = User.objects.get(pk=user.pk).password  # Gunakan password yang ada saat ini
        if commit:
            user.save()
        return user

    
    

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']


class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = '__all__'