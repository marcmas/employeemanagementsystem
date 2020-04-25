from django import forms
from .models import Regulations, RegulationsStatus
from django.db.models import Q
from django.contrib.auth.models import User


class CreateRegulationForm(forms.ModelForm):
    employee = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={'class': 'form-control'}), queryset=User.objects.filter(Q(groups__name='employee') | Q(groups__name='supervisor')))


    class Meta:
        model = Regulations
        fields = ['employee', 'description', 'necessary', 'come_into_force', 'file']
        widgets = {
            'description': forms.Textarea(attrs={'rows':4, 'class': 'form-control', 'placeholder': 'Enter Description...'}),
            'necessary': forms.CheckboxInput(attrs={'class': 'form-check-inline', 'type':"checkbox"}),
            'come_into_force': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'id':'datepicker', 'placeholder': 'Come into force date'}),
            'file': forms.FileInput(attrs={'class':'custom-file-input', 'type':"file", 'id':"customFile"})
        }

    def __init__(self, *args, **kwargs):
        super(CreateRegulationForm, self).__init__(*args, **kwargs)
        self.fields['description'].required == True


# class AcceptRegulationStatus(forms.ModelForm):
#     class Meta:
#         model = RegulationsStatus
#         fields = []
#         exclude = ['employee', 'regulation', 'accept', 'accept_date']