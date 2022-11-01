from django.contrib import admin
from banks.models import Bank, Branch

# Register your models here.
# class BranchInline(admin.TabularInline):
#     model = Branch
#     fields = ['id', 'name']


# class BankAdmin(admin.ModelAdmin):
#     readonly_fields = ['id', 'url']
#     fields = ['id', 'name', 'url']
#     inlines = [BranchInline]
#     list_display = ['id', 'name', 'url']


admin.site.register(Bank)
admin.site.register(Branch)