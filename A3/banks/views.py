from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import FormView, RedirectView, DetailView, ListView
from banks.forms.addBank import AddBankForm
from banks.forms.addBranch import AddBranchForm
from banks.models import Bank, Branch
from django.core import serializers
from django.http import JsonResponse
import json

# Create your views here.
def homepage(request):
	return render(request=request, template_name='bank/home.html')


class AddBank(FormView):
	template_name = 'banks/add_bank.html'
	form_class = AddBankForm

	def form_valid(self, form):
		newBank = Bank.objects.create(name=form.cleaned_data['name'],
            description = form.cleaned_data['description'],
			inst_num = form.cleaned_data['inst_num'],
			swift = form.cleaned_data['swift']
		)
		return HttpResponseRedirect(f"/banks/{newBank.id}/details/")


class AddBranch(FormView):
	template_name = 'banks/add_branch.html'
	form_class = AddBranchForm

	def form_valid(self, form):
		newBranch = Branch.objects.create(bank = Bank.objects.get(pk = self.kwargs['bank_id']),
			name = form.cleaned_data['name'],
            transit_num = form.cleaned_data['transit_num'],
			address = form.cleaned_data['address'],
			email = form.cleaned_data['email'],
			capacity = form.cleaned_data['capacity']
		)
		return HttpResponseRedirect(f"/banks/branch/{newBranch.id}/details/")


class BankViewAll(ListView):
    template_name = 'banks/all_banks.html'
    queryset = Bank.objects.all()
    context_object_name = 'banks'


class BankDetails(DetailView):
	model = Bank
	template_name = 'banks/bank_details.html'
	context_object_name = 'bank'

	def get_object(self, **kwargs):
		return Bank.objects.get(pk=self.kwargs['bank_id'])


class BranchDetails(DetailView):

	def get_object(self, **kwargs):
		return Branch.objects.get(pk=self.kwargs['branch_id'])

	def get(self, request, *args, **kwargs):
		obj = self.get_object()
		data = {}
		data["id"] = self.kwargs['branch_id']
		data["name"] = obj.name
		data["transit_num"] = obj.transit_num
		data["address"] = obj.address
		data["email"] = obj.email
		data["capacity"] = obj.capacity
		data["last_modified"] = str(obj.last_modified)
		return HttpResponse(json.dumps(data), content_type="application/json")


class BranchViewAll(ListView):
	def get_queryset(self, **kwargs):
		return Branch.objects.filter(bank__id__contains=self.kwargs['bank_id'])

	def get(self, request, *args, **kwargs):
		queryset = self.get_queryset()
		list = []
		for obj in queryset:
			data = {}
			# data["id"] = self.kwargs['branch_id']
			data["name"] = obj.name
			data["transit_num"] = obj.transit_num
			data["address"] = obj.address
			data["email"] = obj.email
			data["capacity"] = obj.capacity
			data["last_modified"] = str(obj.last_modified)
			list.append(data)
		return HttpResponse(json.dumps(list), content_type="application/json")