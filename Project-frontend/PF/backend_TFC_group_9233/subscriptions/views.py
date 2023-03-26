from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from django.http import JsonResponse
from accounts.models import OurUser
from dateutil.relativedelta import relativedelta
from django.utils.text import slugify
from rest_framework.exceptions import NotFound, NotAcceptable
from .models import Subscription, UserSubscription, Payment, Card
from subscriptions.serializers import SubscriptionSerializer, UserSubscriptionSerializer, PaymentSerializer, CardSerializer
from datetime import datetime, date
import subscriptions.utils as ut

# Create your views here.

"""
Subscribe: 
- Show all subscription, highlighted users' current subscription if any.
- No need for authentication, all users can access
"""


class Subscribe(ListAPIView):

    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return Subscription.objects.all()

    def get_paginated_response(self, data):
        return Response(data)


"""
UpdateUserSubscription: Update, Subscribe or Cancel current user's plan.
"""


class UpdateUserSubscription(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserSubscriptionSerializer

    def get(self, request):
        user_sub = ut.check_valid_user_subscription(request)
        if user_sub:
            serializer = UserSubscriptionSerializer(user_sub)
            # check auto payment
            return Response(ut.auto_payment(request, serializer))
        else:
            return Response("You don't have subscription now")

    def post(self, request):

        # update
        if request.data['action'] == 'update':
            user_sub = ut.check_valid_user_subscription(request)
            if not user_sub:
                return Response("You dont have a current subscription yet")
            else:
                if not user_sub.next_plan:
                    return Response("You have a subscription now, but do not have any future subscription. Please subscribe")
                else:
                    new_plan = ut.check_valid_subscription(request)
                    if not new_plan:
                        return Response('The plan is not valid')
                    else:
                        card = ut.check_valid_card(request)
                        if not card:
                            return Response("You dont have a valid card to pay yet")
                        else:
                            # cancel previously scheduled payment
                            payment_qs = Payment.objects.filter(
                                status='UNPAID', date__gte=date.today())
                            if payment_qs.exists():
                                payment = payment_qs.first()
                                payment.status = 'CANCELLED'
                                payment.save()

                            # schedule future payment
                            ut.schedule_payment(
                                request, new_plan, card, user_sub.next_payment_date, 'UNPAID')

                            # update next subscription
                            user_sub.next_plan = new_plan
                            user_sub.save()

                            serializer = UserSubscriptionSerializer(user_sub)
                            return Response(serializer.data)

        # cancel
        elif request.data['action'] == 'cancel':
            user_sub = ut.check_valid_user_subscription(
                request)  # check if user subscription record
            if not user_sub:
                return Response('You dont have a subscription to cancel')
            else:
                # cancel future payment
                if not user_sub.next_plan:
                    return Response('You already cancelled your future subscription, current subscription will stay valid through' + user_sub.next_payment_date)
                else:
                    payment_qs = Payment.objects.filter(
                        date__gte=date.today(), status='UNPAID')
                    if payment_qs.exists():
                        for instance in payment_qs:
                            instance.status = 'CANCELLED'
                            instance.card = None
                            instance.save()

                    # cancel subscription
                    user_sub.next_plan = None
                    user_sub.save()
                    return Response('Cancel future subscription success')

        # subscribe
        elif request.data['action'] == 'subscribe':
            if len(Subscription.objects.all()) == 0:
                return Response('No subscription plan to choose from')
            else:
                user_sub = ut.check_valid_user_subscription(request)
                if user_sub:
                    if user_sub.next_plan:
                        return Response("You already have future subscription, please choose to update")
                    else:
                        new_plan = ut.check_valid_subscription(request)
                        if new_plan:
                            card = ut.check_valid_card(request)
                            if not card:
                                return Response("You dont have a valid card to pay yet")
                            else:
                                # add future subscription, schdule new payment
                                user_sub.next_plan = new_plan
                                user_sub.save()
                                new_date = user_sub.next_payment_date
                                ut.schedule_payment(
                                    request, new_plan, card, new_date, 'UNPAID')
                                serializer = UserSubscriptionSerializer(
                                    user_sub)
                                return Response(serializer.data)
                        else:
                            return Response("The plan chosen is invalid")
                else:
                    new_plan = ut.check_valid_subscription(request)
                    if new_plan:
                        card = ut.check_valid_card(request)
                        if not card:
                            return Response("You dont have a valid card to pay yet")
                        else:
                            # add current & future subscription, make imm payment, schedule new payment
                            next_plan = new_plan
                            next_payment_date = ut.get_next_date(
                                request, new_plan, date.today())
                            if not next_payment_date:
                                return Response("Subscription has invalid subscription type")
                            else:
                                user_sub = ut.create_user_subscription(
                                    request, new_plan, next_plan)
                                user_sub.next_payment_date = next_payment_date
                                user_sub.save()
                                ut.schedule_payment(
                                    request, new_plan, card, date.today(), 'SUCCESS')
                                ut.schedule_payment(
                                    request, new_plan, card, next_payment_date, 'UNPAID')
                                serializer = UserSubscriptionSerializer(
                                    user_sub)
                                return Response(serializer.data)
                    else:
                        return Response("The chosen plan is not valid")

        else:
            return Response('not valid action')


"""
PaymentList:
- View All Payment History & Scheduled Payment
"""


class PaymentList(ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.all()

    def get_paginated_response(self, data):
        return Response(data)


"""
CardList:
- View All Cards
"""


class CardList(ListAPIView, APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CardSerializer

    def get_queryset(self):
        return Card.objects.all()

    def get_paginated_response(self, data):
        return Response(data)

    def post(self, request):

        # update
        if request.data['action'] == 'update':
            card = ut.check_valid_card(request)
            if not card:
                return Response("No card to update")
            else:
                if ut.validate_card_info(request):
                    return Response(ut.validate_card_info(request))

                card.card_num = request.data['card_num']
                card.cvc = request.data['cvc']
                card.card_holder_name = request.data['card_holder_name']
                card.expire_date = request.data['expire_date']
                card.save()

                # save to exactly origin card object, so for payments, the card_num shall all change
                # only update card_num info for future payments

                queryset_future = Payment.objects.filter(
                    date__gte=date.today(), status='UNPAID')
                for instance in queryset_future:
                    instance.card = card
                    instance.save()

                queryset_today_unpaid = Payment.objects.filter(
                    date=date.today(), status='UNPAID')
                for instance in queryset_today_unpaid:
                    instance.card = card
                    instance.save()

                serializer = CardSerializer(card)
                return Response(serializer.data)

        # delete
        elif request.data['action'] == 'delete':
            card = ut.check_valid_card(request)
            if not card:
                return Response('No card to delete')
            else:
                queryset_unpaid = Payment.objects.filter(status='UNPAID')
                for instance in queryset_unpaid:
                    instance.card = None
                    instance.save()
                card.delete()
                return Response('Card deleted successfully')

        # add
        elif request.data['action'] == 'add':
            card = ut.check_valid_card(request)
            if card:
                return Response("You've have card info, please update")
            else:
                if ut.validate_card_info(request):
                    return Response(ut.validate_card_info(request))

                card = Card.objects.create(
                    user=OurUser.objects.get(username=request.user.username),
                    card_num=request.data['card_num'],
                    cvc=request.data['cvc'],
                    card_holder_name=request.data['card_holder_name'],
                    expire_date=request.data['expire_date']
                )
                card.save()

                queryset_future = Payment.objects.filter(
                    date__gte=date.today(), status='UNPAID')
                for instance in queryset_future:
                    instance.card = card
                    instance.save()

                queryset_today_unpaid = Payment.objects.filter(status='UNPAID')
                for instance in queryset_today_unpaid:
                    instance.card = card
                    instance.save()

                serializer = CardSerializer(card)
                return Response(serializer.data)

        else:
            return Response('not valid action')
