from django.db import models
from accounts.models import OurUser
from studios.models import Studio
import re
from dateutil.relativedelta import relativedelta
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

"""
Helper Function for checking subscription
"""


def user_subscription(request):
    try:
        user_sub = UserSubscription.objects.get(
            user__username=request.user.username)
        payment_date = datetime.strptime(
            user_sub.next_payment_date, '%Y-%m-%d')
        if date.today() < payment_date.date():
            return user_sub
    except:
        return None


"""
Helper Function for Create objects / get data
"""


def create_user_subscription(request, new_plan, next_plan):
    user_sub = UserSubscription.objects.create(
        user=OurUser.objects.get(username=request.user.username),
        plan=new_plan,
        start_date=date.today(),
        next_plan=next_plan)
    user_sub.save()
    return user_sub


def schedule_payment(request, plan, card, date, status):

    payment = Payment.objects.create(
        user=OurUser.objects.get(username=request.user.username),
        card=card,
        date=date,
        amount=plan.price,
        recurrence_type=plan.subscription_type,
        status=status,
    )
    payment.save()

    return payment


def get_next_date(request, plan, date):
    if plan.subscription_type == 'MONTHLY':
        new_date = date + relativedelta(months=+1)
        return new_date
    elif plan.subscription_type == 'ANNUALLY':
        new_date = date + relativedelta(years=+1)
        return new_date
    else:
        return None


"""
Helper Function for Validation
"""


def check_valid_subscription(request):
    subscription_qs = Subscription.objects.filter(
        title=slugify(request.data['plan']))
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
    user_subscription_qs = UserSubscription.objects.filter(
        user__username=request.user.username)
    if user_subscription_qs.exists():
        return user_subscription_qs.first()
    else:
        return None


def check_valid_payment(request, payment_id):
    payment_qs = Payment.objects.filter(
        user__username=request.user.username, pk=payment_id)
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
    rgx_master = re.compile(
        r"^5[1-5][0-9]{14}|^(222[1-9]|22[3-9]\\d|2[3-6]\\d{2}|27[0-1]\\d|2720)[0-9]{12}$")

    if not (re.fullmatch(rgx_visa, card_num) or re.fullmatch(rgx_master, card_num)):
        return 'Enter a valid card number'

    rgx = re.compile(r'^\d{3}$')
    if not re.fullmatch(rgx, cvc):
        return "Enter a valid cvc"

    expire_date_parsed = datetime.strptime(expire_date, '%Y-%m-%d')
    if expire_date_parsed.date() < date.today():
        return "Enter a valid date"

    return None


"""
Helper Function for Auto Payment
"""


def auto_payment_printer(auto_result, serializer):
    auto = {"auto payment": auto_result}
    auto.update(serializer.data)
    return auto


def auto_payment(request, serializer):

    # check auto payment
    payment_qs = Payment.objects.filter(
        user__username=request.user.username, status='UNPAID')

    if payment_qs.exists():
        payment = payment_qs.first()
        payment_date = datetime.strptime(str(payment.date), '%Y-%m-%d')
        if date.today() >= payment_date.date():

            # check valid card
            card = check_valid_card(request)
            if not card:
                return auto_payment_printer("no valid card", serializer)
            else:

                # check valid payment
                payment = check_valid_payment(request, payment.pk)
                if not payment:
                    return auto_payment_printer("not valid payment", serializer)
                else:

                    # check valid user subscription
                    user_sub = check_valid_user_subscription(request)
                    if not user_sub:
                        return auto_payment_printer("This payment should not be made cuz you don't have subscription.", serializer)
                    else:
                        if not user_sub.next_plan:
                            return auto_payment_printer("This payment should not be made cuz you have cancelled future subscription.", serializer)
                        else:
                            next_plan = user_sub.next_plan  # Subscription obj
                            next_payment_date = get_next_date(
                                request, next_plan, payment.date)

                            # make current payment
                            payment.status = 'SUCCESS'
                            payment.card = card
                            payment.date = date.today()
                            payment.save()

                            # schedule future payment
                            payment_next = schedule_payment(
                                request, next_plan, card, next_payment_date, 'UNPAID')

                            # update user subscription
                            user_sub.plan = next_plan
                            user_sub.next_plan = next_plan
                            user_sub.next_payment_date = payment_next.date
                            user_sub.save()

                            return auto_payment_printer("success", serializer)
        else:
            return auto_payment_printer("not yet", serializer)
    else:
        return auto_payment_printer("none", serializer)
