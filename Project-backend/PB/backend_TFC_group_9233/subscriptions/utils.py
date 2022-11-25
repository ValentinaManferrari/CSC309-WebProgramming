from django.db import models
from accounts.models import OurUser
from studios.models import Studio
import re
from datetime import datetime, date, timedelta
from django.utils.text import slugify
from rest_framework.response import Response
from subscriptions.models import Subscription, UserSubscription, Card, Payment

# for helper functions

"""
Input: 
    request: current user
    studio: should be a studio object
Return:
    if has subscription at the studio: return a UserSubscription object
    if no subscription at the studio: return None

* Note: One user can only have one subscription at one studio
"""


def user_subscription(request):
    try:
      user_sub = UserSubscription.objects.get(user=request.user)
      payment_date = datetime.strptime(user_sub.next_payment_date, '%Y-%m-%d')
      if date.today() < payment_date.date():
          return user_sub
    except:
        return None


def check_valid_subscription(request):
    subscription_qs = Subscription.objects.filter(title=slugify(request.data['plan']))
    if subscription_qs.exists():
        return subscription_qs.first()
    else:
        return None


def check_valid_card(request):
    card_qs = Card.objects.filter(user__username=request.user.username)
    if card_qs.exists():
        return card_qs.first()
    else:
        return None


def check_valid_user_subscription(request):
    user_subscription_qs = UserSubscription.objects.filter(user__username=request.user.username)
    if user_subscription_qs.exists():
        return user_subscription_qs.first()
    else:
        return None


def check_valid_payment(request, payment_id):
    payment_qs = Payment.objects.filter(user__username=request.user.username, pk=payment_id)
    if payment_qs.exists():
        return payment_qs.first()
    else:
        return None


def validate_card_info(request):
    if not (request.data['card_num'] and request.data['card_holder_name'] and request.data['cvc'] and request.data[
        'expire_date']):
        return "Enter all fields"

    card_num = request.data['card_num']
    card_holder_name = request.data['card_holder_name']
    cvc = request.data['cvc']
    expire_date = request.data['expire_date']

    # reference: https://stackoverflow.com/questions/9315647/regex-credit-card-number-tests
    rgx_visa = re.compile(r"^4[0-9]{12}(?:[0-9]{3})?$")
    rgx_master = re.compile(r"^5[1-5][0-9]{14}|^(222[1-9]|22[3-9]\\d|2[3-6]\\d{2}|27[0-1]\\d|2720)[0-9]{12}$")

    if not (re.fullmatch(rgx_visa, card_num) or re.fullmatch(rgx_master, card_num)):
        return 'Enter a valid card number'

    rgx = re.compile(r'^\d{3}$')
    if not re.fullmatch(rgx, cvc):
        return "Enter a valid cvc"

    expire_date_parsed = datetime.strptime(expire_date, '%Y-%m-%d')
    if expire_date_parsed.date() < date.today():
        return "Enter a valid date"

    return None

def finish_current_create_next_payment(request, payment_id):

    payment = check_valid_payment(request, payment_id)

    if payment.recurrence:
        # the payment is recurrent but use has no subscription, something is wrong
        user_sub = check_valid_user_subscription(request)
        if not user_sub:
            return None
        else:
            current_plan = user_sub.plan  # Subscription obj
            payment_next = Payment.objects.create(
                user=OurUser.objects.get(username=request.user.username),
                card=Card.objects.get(user__username=request.user.username),
                date=date.today() + current_plan.iteration,
                amount=current_plan.price,
                recurrence=True,
                recurrence_type=current_plan.subscription_type,
                status='UNPAID',
            )
            payment_next.save()

            # update usersubscription next_payment_date
            user_sub.next_payment_date = payment_next.date
            user_sub.save()

    # finish current payment
    payment.date = date.today()
    payment.status = 'SUCCESS'
    payment.save()

    if payment.status == 'SUCCESS':
        return payment
    else:
        return None


