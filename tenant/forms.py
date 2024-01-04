from django.forms.widgets import TextInput,Textarea,Select,DateInput,CheckboxInput,FileInput,PasswordInput,EmailInput
from django import forms

from . models import *


class TenantForm(forms.ModelForm):

    class Meta:
        model = Tenant
        fields = ['name','address','image']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Name'}), 
            'address': Textarea(attrs={'class': 'required form-control text-area','placeholder' : 'Enter Address','rows':'2'}), 
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }
        
    def clean_image(self):
        
        image_file = self.cleaned_data.get('image')
        if image_file:
            if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".png") or image_file.name.endswith(".jpeg")):
                raise forms.ValidationError("Only .jpg or .png files are accepted")
        return image_file
    
    
class TenantDocumentForm(forms.ModelForm):

    class Meta:
        model = TenantDocuments
        fields = ['name','document']

        widgets = {
            'name': Select(attrs={'class': 'select2 form-control mb-3 custom-select'}),
            'document': FileInput(attrs={'class': 'form-control dropify'}),
        }
    
        
class TenantUnitAssignForm(forms.ModelForm):

    class Meta:
        model = TenantUnitAssignment
        fields = ['tenant','agreement_end_date','monthly_rent_date','attachement']

        widgets = {
            'tenant': Select(attrs={'class': 'select2 form-control mb-3 custom-select'}),
            'agreement_end_date': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Agrement End Date'}), 
            'monthly_rent_date': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Rent Date'}), 
            'attachement': FileInput(attrs={'class': 'form-control dropify'}),
        }