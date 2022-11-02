from asyncio.windows_events import NULL
from email.policy import default
from pyexpat import model
# from typing_extensions import Required
from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE

# Create your models here.
class Bank(models.Model):
    owner = models.ForeignKey(to=User, on_delete=CASCADE, related_name='banks')
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(max_length=200, null=False)
    inst_num = models.CharField(max_length=200, null=False)
    swift_code = models.CharField(max_length=200, null=False)

    def __str__(self):
        return str({self.name})

class Branch(models.Model):
    bank = models.ForeignKey(to=Bank, on_delete=CASCADE, related_name='branches')
    name = models.CharField(max_length=200, null=False)
    transit_num = models.CharField(max_length=200, null=False)
    address = models.CharField(max_length=200, null=False)
    email = models.EmailField(max_length=200, default='admin@utoronto.ca')
    capacity = models.PositiveIntegerField(null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str({self.name})