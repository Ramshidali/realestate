from django.forms.widgets import TextInput,Textarea,Select,DateInput,CheckboxInput,FileInput,PasswordInput,EmailInput
from django import forms
from . models import *

        
class AdminUserForm(forms.ModelForm):

    class Meta:
        model = AdminUser
        fields = ['first_name','last_name','email','phone','date_of_birth','image','password']

        widgets = {
            'first_name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter First Name'}), 
            'last_name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Last Name'}), 
            'email': EmailInput(attrs={'class': 'required form-control','placeholder' : 'Enter Email'}), 
            'phone': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Phone Number'}), 
            'date_of_birth': TextInput(attrs={'class': 'required form-control','id':'date_of_birth','name':'birthday','placeholder' : 'Enter Date of Birth'}), 
            'image': FileInput(attrs={'class': 'form-control dropify'}),
            'password': PasswordInput(attrs={'class': 'required form-control','placeholder' : 'Enter Password'}), 
        }
        
    def clean_image(self):
        
        image_file = self.cleaned_data.get('image')
        if image_file:
            if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".png") or image_file.name.endswith(".jpeg")):
                raise forms.ValidationError("Only .jpg or .png files are accepted")
        return image_file