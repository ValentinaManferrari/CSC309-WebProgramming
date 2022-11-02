from django import forms
from banks.models import Bank

class AddBankForm(forms.Form):
    name = forms.CharField(required=False)
    description = forms.CharField(required=False)
    inst_num = forms.CharField(required=False)
    swift_code = forms.CharField(required=False)
    
    class Meta:
        model = Bank
        fields = ["name", "description", "inst_numl", "swift_code"]

    def clean(self):
        data = super().clean()
        if not data.get('name'):
            self.add_error('name', "This field is required")
        if not data.get('description'):
            self.add_error('description', "This field is required")
        if not data.get('inst_num'):
            self.add_error('inst_num', "This field is required")
        if not data.get('swift_code'):
            self.add_error('swift_code', "This field is required")
        return data

