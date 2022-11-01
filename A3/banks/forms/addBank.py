from django import forms
from banks.models import Bank

class AddBankForm(forms.Form):
    name = forms.CharField(required=True)
    description = forms.CharField(required=True)
    inst_num = forms.CharField(required=True)
    swift = forms.CharField(required=True)
    
    class Meta:
        model = Bank
        fields = ["name", "description", "inst_numl", "swift"]

    def clean(self):
        data = super().clean()

        if data['name'] is None:
            self.add_error('name', "This field is required")
        if data['description'] is None:
            self.add_error('description', "This field is required")
        if data['inst_num'] is None:
            self.add_error('inst_num', "This field is required")
        if data['swift'] is None:
            self.add_error('inst_num', "This field is required")
        return data

