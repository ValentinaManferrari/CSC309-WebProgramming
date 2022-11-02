from wsgiref import validate
from django.core.exceptions import ValidationError
from django import forms
from banks.models import Branch
from django.core.validators import validate_email

class AddBranchForm(forms.Form):
    name = forms.CharField(required=False)
    transit_num = forms.IntegerField(required=False)
    address = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    capacity = forms.IntegerField(required=False)
    
    class Meta:
        model = Branch
        fields = ["name", "transit_num", "address", "email", "capacity"]

    def clean(self):
        data = super().clean()
        
        if not data.get('name'):
            self.add_error('name', "This field is required")
        if not data.get('transit_num'):
            self.add_error('transit_num', "This field is required")
        if not data.get('address'):
            self.add_error('address', "This field is required")
        
        if not data.get('email'):
            self.add_error('email', "This field is required")
        else:
            try:
                validate_email(data.get('email'))
            except ValidationError:
                self.add_error('email', "Enter a valid email address")

        return data

