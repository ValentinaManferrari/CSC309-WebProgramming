from django.db import models
from django.conf import settings
from accounts.models import OurUser
from rest_framework.response import Response
from studios.models import Studio
from rest_framework.fields import CurrentUserDefault
from django.core.exceptions import ValidationError
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import re
import datetime

# Create your models here.

"""
Subscription: 
store all subscription plans
"""

SUBSCRIPTION_CHOICES = (
    ('MONTHLY', 'charge by month'),
    ('ANNUALLY', 'charge annually'),
)

PAYMENT_STATUS = (
    ('UNPAID', 'unpaid'),
    ('SUCCESS', 'success'),
    ('CANCELLED', 'cancelled')
)


class Subscription(models.Model):

    title = models.SlugField(null=False, unique=True)
    subscription_type = models.CharField(
        choices=SUBSCRIPTION_CHOICES, default=None, max_length=50)
    price = models.FloatField(default=0)
    iteration = models.DurationField(
        verbose_name='iteration(days,hours,min,sec)', default=datetime.timedelta(days=30), editable=False)

    def save(self, *args, **kwargs):
        if self.subscription_type == 'MONTHLY':
            self.iteration = datetime.timedelta(days=30)
        elif self.subscription_type == 'ANNUALLY':
            self.iteration = datetime.timedelta(days=365)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


"""
UserSubscription: 
store user's subscription plan.
One subscription --> multiple users
One user --> one subscription
"""


class UserSubscription(models.Model):

    # https://stackoverflow.com/questions/5870537/whats-the-difference-between-django-onetoonefield-and-foreignkey
    user = models.ForeignKey(
        OurUser, related_name='user_subscription', on_delete=models.CASCADE)
    plan = models.ForeignKey(
        Subscription, related_name='current_plan_subscription', on_delete=models.CASCADE, null=True)
    start_date = models.DateField(null=True, blank=True)
    next_payment_date = models.DateField(null=True, blank=True, editable=False)
    next_plan = models.ForeignKey(
        Subscription, related_name='next_plan_subscription', on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username + "/" + self.plan.title


"""
Card:
a card a user holds.
"""


class Card(models.Model):

    def validate_card_num(card_num):
        # reference: https://stackoverflow.com/questions/9315647/regex-credit-card-number-tests
        rgx_visa = re.compile(r"^4[0-9]{12}(?:[0-9]{3})?$")
        rgx_master = re.compile(
            r"^5[1-5][0-9]{14}|^(222[1-9]|22[3-9]\\d|2[3-6]\\d{2}|27[0-1]\\d|2720)[0-9]{12}$")

        if not (re.fullmatch(rgx_visa, card_num) or re.fullmatch(rgx_master, card_num)):
            return Response('Enter a valid card number')
        return card_num

    def validate_cvc(cvc):
        rgx = re.compile(r'^\d{3}$')
        if not re.fullmatch(rgx, cvc):
            return Response("Enter a valid cvc")
        return cvc

    def validate_expire_date(expire_date):
        if expire_date:
            if expire_date < datetime.date.today():
                return Response("Enter a valid date")
        else:
            return Response("Enter a valid date")
        return expire_date

    user = models.ForeignKey(OurUser, on_delete=models.CASCADE)
    card_num = models.CharField(max_length=30, validators=[validate_card_num])
    expire_date = models.DateField(
        validators=[validate_expire_date], null=False)
    card_holder_name = models.CharField(max_length=30)  # only for payment
    cvc = models.CharField(max_length=30, validators=[validate_cvc])

    def __str__(self):
        return self.card_num


"""
Payment:
a payment made by a user, can be history or future payment.
For history payment, date is the past time when the payment is made.
For future payment, date is some time in future.
"""


class Payment(models.Model):
    user = models.ForeignKey(OurUser, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True)
    card_num = models.CharField(max_length=30, editable=False)
    date = models.DateField()  # future : date >= now and UNPAID
    amount = models.FloatField(max_length=30)
    recurrence_type = models.CharField(
        null=True, choices=SUBSCRIPTION_CHOICES, blank=True, max_length=10)
    # if a new payment need to be added once this payment has been done
    # recurrence = models.BooleanField(null=False, blank=False, default=False)
    # success = models.BooleanField(null=False, blank=False, default=False)
    status = models.CharField(null=False, blank=False,
                              choices=PAYMENT_STATUS, max_length=10)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.card:
            self.card_num = self.card.card_num
        else:
            self.card_num = '0000000000000000'
        super().save(*args, **kwargs)
