import datetime
from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext_lazy as _

from django import forms
from .models import Leave, AcceptLeave, RejectLeave, VacationLimit

class CreateLeaveForm(forms.ModelForm): 

    class Meta: 
        model = Leave
        fields = "__all__"
        exclude = ['employee', 'status']
        widgets = {
            'leave_type': forms.Select(attrs={'class': 'form-control'}),
            'leave_date': forms.DateInput(format='%Y-%m-%d', attrs={'id':'datepicker', 'placeholder': 'Date leave', 'class': 'form-control'}),
            'return_date': forms.DateInput(format='%Y-%m-%d', attrs={'id':'datepicker1', 'placeholder': 'Date return', 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', "rows":5, "cols":20}),
        }


    def clean(self):
        cleaned_data = super().clean()
        leave_date = self.cleaned_data.get('leave_date')
        return_date = self.cleaned_data.get('return_date')

        # Check if a return_date is greater than leave_date
        if return_date < datetime.date.today():
            raise forms.ValidationError("Return date should be greater than leave date.")
        # Check if a date is not in the past. 
        if leave_date < datetime.date.today():
            raise forms.ValidationError("Leave date should be greater than today.")
        # Check if a return_date is greater than leave_date
        if leave_date > return_date:
            raise forms.ValidationError("Leave date can't be greater than return date.")



class CreateAcceptLeaveForm(forms.ModelForm):

    class Meta:
        model = AcceptLeave
        fields = []
        exclude = ['status', 'leave']


class CreateRejectLeaveForm(forms.ModelForm):

    class Meta:
        model = RejectLeave
        fields = []
        exclude = ['status', 'leave']


class UpdateVacationLimitForm(forms.ModelForm):

    class Meta:
        model = VacationLimit
        fields = "__all__"
        exclude = ["employee"]
        widgets = {
            'normal_days_constant': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter constant normal days'}),
            'normal_days': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter normal days'}),
            'children_days_constant': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter constant children days'}),
            'children_days': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter children days'}),
            'request_days_constant': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter constant request days'}),
            'request_days': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter request number'}),
        }

    def __init__(self, *args, **kwargs):
        super(UpdateVacationLimitForm, self).__init__(*args, **kwargs)
        self.fields['normal_days_constant'].required == True
        self.fields['normal_days'].required == True
        self.fields['children_days_constant'].required == True
        self.fields['children_days'].required == True
        self.fields['request_days_constant'].required == True
        self.fields['request_days'].required == True

    

class ExportLeaveForm(forms.Form):

    leave_date = forms.DateField(widget=forms.TextInput(attrs={'id':'datepicker', 'placeholder': 'Date leave', 'class': 'form-control'}))
    return_date = forms.DateField(widget=forms.TextInput(attrs={'id':'datepicker1', 'placeholder': 'Date leave', 'class': 'form-control'}))
