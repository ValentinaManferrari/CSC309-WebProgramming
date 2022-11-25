# from django import forms
# from django.core.exceptions import ValidationError
# import re, datetime
#
#
# class UpdateCardForm(forms.ModelForm):
#
#     card_number = forms.CharField(required=True, max_length=30)
#     card_holder_name = forms.CharField(required=True, max_length=30)
#     cvc = forms.CharField(max_length=3)
#     expire_date = forms.DateField(required=True)
#
#     def clean_card_num(self):
#         card_num = self.cleaned_data.get('card_num')
#
#         # reference: https://stackoverflow.com/questions/9315647/regex-credit-card-number-tests
#         rgx_visa = re.compile("^4[0-9]{12}(?:[0-9]{3})?$") # visa
#         rgx_master = re.compile("^5[1-5][0-9]{14}|^(222[1-9]|22[3-9]\\d|2[3-6]\\d{2}|27[0-1]\\d|2720)[0-9]{12}$")
#
#         if not (re.fullmatch(rgx_visa, card_num) or re.fullmatch(rgx_master, card_num)):
#             raise ValidationError('Enter a valid card number')
#         return card_num
#
#     def clean_expire_date(self):
#         date = self.cleaned_data.get('date')
#         if date < datetime.date.today():
#             raise ValidationError("Enter a valid date")
#         return date
#
#     def clean_cvc(self):
#         cvc = self.cleaned_data.get('cvc')
#         rgx = re.compile(r'^\d{3}$')
#         if re.fullmatch(rgx,cvc):
#             return cvc
#         else:
#             raise ValidationError("Enter a valid cvc")
#         return cvc
#
#
#
