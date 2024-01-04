from django.forms.widgets import TextInput,Textarea,Select,DateInput,CheckboxInput,FileInput,PasswordInput,EmailInput
from django import forms

from . models import *

        
class PropertyForm(forms.ModelForm):

    class Meta:
        model = Property
        fields = ['name','address','features','location','image']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Name'}), 
            'address': Textarea(attrs={'class': 'required form-control text-area','placeholder' : 'Enter Address','rows':'2'}), 
            'location': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Location'}), 
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }
        
    def clean_image(self):
        
        image_file = self.cleaned_data.get('image')
        if image_file:
            if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".png") or image_file.name.endswith(".jpeg")):
                raise forms.ValidationError("Only .jpg or .png files are accepted")
        return image_file
    
class UnitForm(forms.ModelForm):

    class Meta:
        model = Unit
        fields = ['type','rent_cost','main_image']

        widgets = {
            'type': Select(attrs={'class': 'select2 form-control mb-3 custom-select'}),
            'rent_cost': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Location'}), 
            'main_image': FileInput(attrs={'class': 'form-control dropify'}),
        }
        
    def clean_main_image(self):
        
        image_file = self.cleaned_data.get('main_image')
        if image_file:
            if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".png") or image_file.name.endswith(".jpeg")):
                raise forms.ValidationError("Only .jpg or .png files are accepted")
        return image_file