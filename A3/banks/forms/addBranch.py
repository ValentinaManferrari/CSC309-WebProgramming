from wsgiref import validate
from django.core.exceptions import ValidationError
from django import forms
from banks.models import Branch
from django.core.validators import validate_email

class AddBranchForm(forms.Form):
    name = forms.CharField(required=True)
    transit_num = forms.IntegerField(required=True)
    address = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    capacity = forms.IntegerField(required=False)
    
    class Meta:
        model = Branch
        fields = ["name", "transit_num", "address", "email", "capacity"]

    def clean(self):
        data = super().clean()

        # if data['name'] is None:
        #     self.add_error('name', "This field is required")
        # if data['transit_num'] is None:
        #     self.add_error('transit_num', "This field is required")
        # if data['address'] is None:
        #     self.add_error('address', "This field is required")
        # if data['email'] is None:
        #     self.add_error('email', "This field is required")
        # # if validate_email(data['email']):
        # #     self.add_error('email', "This field is required")
        # try:
        #     validate_email(data['email'])
        # except ValidationError:
        #     self.add_error('email', "Enter a valid email address")

        return data

