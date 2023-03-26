from django.contrib import admin
from .models import Subscription, UserSubscription, Payment, Card

# Register your models here.
admin.site.register(Subscription)
admin.site.register(UserSubscription)
admin.site.register(Payment)
admin.site.register(Card)
