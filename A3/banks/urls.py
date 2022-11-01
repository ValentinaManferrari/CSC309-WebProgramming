from django.urls import path

from banks.views import homepage, AddBank, AddBranch, BankDetails, BranchDetails, BankViewAll, BranchViewAll

app_name = 'banks'

urlpatterns = [
    path('', homepage, name="homepage"),
    path('add/', AddBank.as_view()),
    path('<str:bank_id>/branches/add/', AddBranch.as_view()),
    
    path('all/', BankViewAll.as_view()),
    path('<str:bank_id>/details/', BankDetails.as_view()),

    path('branch/<str:branch_id>/details/', BranchDetails.as_view()),
    path('<str:bank_id>/branches/all/', BranchViewAll.as_view()),
]
