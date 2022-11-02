from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.views.generic import FormView, RedirectView, DetailView, ListView
from banks.forms.addBank import AddBankForm
from banks.forms.addBranch import AddBranchForm
from banks.models import Bank, Branch
from django.http import JsonResponse

# Create your views here.
def homepage(request):
	return render(request=request, template_name='bank/header.html')

# # # # # IF YOU KNOW FORMS, YOU KNOW # # # # #

class AddBank(FormView):
	template_name = 'banks/add_bank.html'
	form_class = AddBankForm

	# def get(self, request, *args, **kwargs):
	# 	form = AddBankForm()
	# 	context = {'bank_form': form}
	# 	if self.request.user.is_anonymous:
	# 		return HttpResponse('401 UNAUTHORIZED', status=401)
	# 	return render(request, 'banks/add_bank.html', context)
		
	def form_valid(self, form):
		if not self.request.user.is_anonymous:
			newBank = Bank.objects.create(
				owner = self.request.user,
				name = form.cleaned_data['name'],
				description = form.cleaned_data['description'],
				inst_num = form.cleaned_data['inst_num'],
				swift_code = form.cleaned_data['swift_code']
			)
			return HttpResponseRedirect(f"/banks/{newBank.id}/details/")
		else:
			return HttpResponse('401 UNAUTHORIZED', status=401)

class AddBranch(FormView):
	template_name = 'banks/add_branch.html'
	form_class = AddBranchForm

	# def get(self, request, *args, **kwargs):
	# 	form = AddBranchForm()
	# 	context = {'branch_form': form}
	# 	if self.request.user.is_anonymous:
	# 		return HttpResponse('401 UNAUTHORIZED', status=401)
	# 	try:
	# 		bank_obj = Bank.objects.get(pk = self.kwargs['bank_id'])
	# 	except Bank.DoesNotExist:
	# 		return HttpResponse('404 NOT FOUND', status=404)
	# 	if self.request.user != bank_obj.owner:
	# 		return HttpResponse('403 FORBIDDEN', status=401)
	# 	return render(request, 'banks/add_branch.html', context)

	def form_valid(self, form):
		if self.request.user.is_anonymous:
			return HttpResponse('401 UNAUTHORIZED', status=401)	
		try:
			bank_obj = Bank.objects.get(pk = self.kwargs['bank_id'])
		except Bank.DoesNotExist:
			return HttpResponse('404 NOT FOUND', status=404)

		if self.request.user == bank_obj.owner:
			newBranch = Branch.objects.create(
				bank = bank_obj,
				name = form.cleaned_data['name'],
				transit_num = form.cleaned_data['transit_num'],
				address = form.cleaned_data['address'],
				email = form.cleaned_data['email'],
				capacity = form.cleaned_data['capacity']
			)
			return HttpResponseRedirect(f"/banks/branch/{newBranch.id}/details/")
		else:
			return HttpResponse('403 FORBIDDEN', status=403)				

# # # # # WRONG CRAWD # # # # #

class BankViewAll(ListView):
    template_name = 'banks/all_banks.html'
    queryset = Bank.objects.all()
    context_object_name = 'banks'


class BankDetails(DetailView):
	model = Bank
	template_name = 'banks/bank_details.html'
	context_object_name = 'bank'

	def get_object(self, **kwargs):
		try:
			bank = Bank.objects.get(pk=self.kwargs['bank_id'])
		except Bank.DoesNotExist:
			raise Http404()
		return bank

# # # # # JSON IS BETTER # # # # #

class BranchDetails(DetailView):
	def get_object(self, **kwargs):
		try:
			branch = Branch.objects.get(pk=self.kwargs['branch_id'])
		except Branch.DoesNotExist:
			raise Http404()
		return branch

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
		return JsonResponse(data)


class BranchViewAll(ListView):
	def get_queryset(self, **kwargs):
		try:
			branches = Branch.objects.filter(bank__id__contains=self.kwargs['bank_id'])
		except Branch.DoesNotExist:
			raise Http404()
		return branches
	
	def get(self, request, *args, **kwargs):
		queryset = self.get_queryset()
		list = []
		for obj in queryset:
			data = {}
			data["id"] = obj.pk
			data["name"] = obj.name
			data["transit_num"] = obj.transit_num
			data["address"] = obj.address
			data["email"] = obj.email
			data["capacity"] = obj.capacity
			data["last_modified"] = str(obj.last_modified)
			list.append(data)
		return JsonResponse(list, safe=False)

