from django.forms import ModelForm, CharField

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Boss, Firm, Section, SalaryInfo, BankInfo
from django import forms

class CreateUserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter firstname'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter lastname'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter email'}),
        }

    def __init__(self, *args, **kwargs):
            super(CreateUserForm, self).__init__(*args, **kwargs)
            self.fields['password1'].required = False
            self.fields['password2'].required = False


class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter firstname'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter lastname'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter email'}),
        }


class UpdateUsernameForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Enter Username...'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Enter Password...'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Enter Password...'}))


class UpdateUserProfileForm(forms.ModelForm):

    boss = forms.ModelChoiceField(queryset=Boss.only_director_role.all(), widget=forms.Select(attrs={'class':'form-control'})),
    firm = forms.ModelChoiceField(queryset=Firm.objects.all(), widget=forms.Select(attrs={'class':'form-control'})),
    section = forms.ModelChoiceField(queryset=Section.objects.all(), widget=forms.Select(attrs={'class':'form-control'})),

    class Meta:

        model = UserProfile
        fields = ['boss', 'firm', 'country', 'section', 'city', 'street', 'zip_code', 'phone_number', 'possition', 'birth_date']
        widgets = {
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter country'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter city'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter street'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter zip code'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter phone number'}),
            'possition': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter possition'}),
            'birth_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter birth date'}),
        }


    def __init__( self,  *args, **kwargs ):
        super(UpdateUserProfileForm, self).__init__(*args, **kwargs)
        self.fields['boss'].queryset = Boss.only_director_role.all()
        self.fields['boss'].required = True
        self.fields['firm'].required = True
        self.fields['section'].required = True
        self.fields['country'].required = True
        self.fields['city'].required = True
        self.fields['street'].required = True
        self.fields['zip_code'].required = True
        self.fields['phone_number'].required = True
        self.fields['possition'].required = True
        self.fields['birth_date'].required = True



class updateProfilePictureForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'class':'custom-file-input', 'type':"file", 'id':"customFile"})
        }

class UpdateUserProfileEmployeeForm(forms.ModelForm):

    boss = forms.ModelChoiceField(queryset=Boss.only_supervisor_role.all(), widget=forms.Select(attrs={'class':'form-control'})),
    firm = forms.ModelChoiceField(queryset=Firm.objects.all(), widget=forms.Select(attrs={'class':'form-control'})),
    section = forms.ModelChoiceField(queryset=Section.objects.all(), widget=forms.Select(attrs={'class':'form-control'})),

    class Meta:

        model = UserProfile
        fields = ['boss', 'firm', 'country', 'section', 'city', 'street', 'zip_code', 'phone_number', 'possition', 'birth_date']
        widgets = {
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter country'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter city'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter street'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter zip code'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter phone number'}),
            'possition': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter possition'}),
            'birth_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter birth date'}),
        }


    def __init__( self,  *args, **kwargs ):
        super(UpdateUserProfileEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['boss'].queryset = Boss.only_supervisor_role.all()  



class UpdateSalaryInfoForm(forms.ModelForm):

    class Meta:

        model = SalaryInfo
        fields = ['salary', 'year_salary', 'type_contract']
        widgets = {
            'salary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter salary'}),
            'year_salary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter year salary'}),
            'type_contract': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
            super(UpdateSalaryInfoForm, self).__init__(*args, **kwargs)
            self.fields['salary'].required = True
            self.fields['year_salary'].required = True
            self.fields['type_contract'].required = True


class UpdateBankInfoForm(forms.ModelForm):

    class Meta:

        model = BankInfo
        fields = ['bank_name', 'bank_number']
        widgets = {
            'bank_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter bank name'}),
            'bank_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter bank number'}),
        }

    def __init__(self, *args, **kwargs):
            super(UpdateBankInfoForm, self).__init__(*args, **kwargs)
            self.fields['bank_name'].required = True
            self.fields['bank_number'].required = True


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Enter Username...'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Enter Password...'}))


