from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from django.http import JsonResponse
from accounts.models import OurUser
from django.utils.text import slugify
from rest_framework.exceptions import NotFound, NotAcceptable
from .models import Subscription, UserSubscription, Payment, Card
from subscriptions.serializers import SubscriptionSerializer, UserSubscriptionSerializer, PaymentSerializer, CardSerializer
from datetime import datetime, date
from subscriptions.utils import check_valid_card, check_valid_payment, check_valid_user_subscription, check_valid_subscription, validate_card_info, finish_current_create_next_payment

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

        user_sub = check_valid_user_subscription(request)
        if user_sub:
            serializer = UserSubscriptionSerializer(user_sub)

            # check auto payment
            payment_qs = Payment.objects.filter(user__username=request.user.username, status='UNPAID')
            if payment_qs.exists():
                payment = payment_qs.first()
                payment_date = datetime.strptime(str(payment.date), '%Y-%m-%d')
                if date.today() >= payment_date.date():
                    card = check_valid_card(request)
                    if not card:
                        return Response("Your card is expired, please update")
                    else:
                        payment = finish_current_create_next_payment(request, payment.pk)
                        if not payment:
                            auto = {"auto payment": "failed"}
                            auto.update(serializer.data)
                            return Response(auto)
                        else:
                            auto = {"auto payment": "success"}
                            auto.update(serializer.data)
                            return Response(auto)
                else:
                    auto = {"auto payment": "none"}
                    auto.update(serializer.data)
                    return Response(auto)
            return Response(serializer.data)
        else:
            return Response("You don't have subscription now")


    def post(self, request):

        # update
        if request.data['action'] == 'update':
            user_sub = check_valid_user_subscription(request)
            if not user_sub:
                return Response("You dont have a subscription yet")
            else:
                new_plan = check_valid_subscription(request)
                if not new_plan:
                    return Response('The plan is not valid')
                else:
                    card = check_valid_card(request)
                    if not card:
                        return Response("You dont have a valid card to pay yet")
                    else:
                        # cancel previous plan next payment
                        payment_qs = Payment.objects.filter(recurrence=True, date__gte=date.today())
                        if payment_qs.exists():
                            payment = payment_qs.first()
                            payment.status = 'CANCELLED'
                            payment.save()

                        # immediate payment of new plan
                        payment_now = Payment.objects.create(
                            user=OurUser.objects.get(username=request.user.username),
                            card=card,
                            date=date.today(),
                            amount=new_plan.price,
                            recurrence=True,
                            recurrence_type=new_plan.subscription_type,
                            status='SUCCESS'
                        )
                        payment_now.save()

                        # schedule future payment
                        payment_future = Payment.objects.create(
                            user=OurUser.objects.get(username=request.user.username),
                            card=card,
                            date=date.today()+new_plan.iteration,
                            amount=new_plan.price,
                            recurrence=True,
                            recurrence_type=new_plan.subscription_type,
                            status='UNPAID',
                        )
                        payment_future.save()

                        # update current subscription
                        user_sub.plan = new_plan
                        user_sub.start_date = date.today()
                        user_sub.next_payment_date = payment_future.date
                        user_sub.save()

                        serializer = UserSubscriptionSerializer(user_sub)
                        return Response(serializer.data)

        # cancel
        elif request.data['action'] == 'cancel':
            user_sub = check_valid_user_subscription(request)
            if not user_sub:
                return Response('You dont have a subscription to cancel')
            else:
                # cancel future payment
                payment_qs = Payment.objects.filter(recurrence=True, date__gte=date.today(), status='UNPAID')
                if payment_qs.exists():
                    for instance in payment_qs:
                        instance.status = 'CANCELLED'
                        instance.card = None
                        instance.save()

                # cancel subscription
                user_sub.delete()
                return Response('Cancel subscription success')

        # subscribe
        elif request.data['action'] == 'subscribe':
            if len(Subscription.objects.all()) == 0:
                return Response('No subscription plan to choose from')
            else:
                user_sub = check_valid_user_subscription(request)
                if user_sub:
                    return Response("You already have one subscription, please choose uppdate")
                else:
                    new_plan = check_valid_subscription(request)
                    if new_plan:
                        card = check_valid_card(request)
                        if not card:
                            return Response("You dont have a valid card to pay yet")
                        else:
                            # subscribe
                            user_sub = UserSubscription.objects.create(
                                user=OurUser.objects.get(username=request.user.username),
                                plan=new_plan,
                                start_date=date.today(),
                            )
                            user_sub.save()

                            # immediate payment
                            payment_now = Payment.objects.create(
                                user=OurUser.objects.get(username=request.user.username),
                                card=card,
                                date=date.today(),
                                amount=new_plan.price,
                                recurrence=True,
                                recurrence_type=new_plan.subscription_type,
                                status='SUCCESS',
                            )
                            payment_now.save()

                            # schedule future payment
                            payment_future = Payment.objects.create(
                                user=OurUser.objects.get(username=request.user.username),
                                card=card,
                                date=date.today()+new_plan.iteration,
                                amount=new_plan.price,
                                recurrence=True,
                                recurrence_type=new_plan.subscription_type,
                                status='UNPAID',
                            )
                            payment_future.save()

                            user_sub.next_payment_date=payment_future.date
                            user_sub.save()

                            serializer = UserSubscriptionSerializer(user_sub)
                            return Response(serializer.data)

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
            card = check_valid_card(request)
            if not card:
                return Response("No card to update")
            else:
                if validate_card_info(request):
                    return Response(validate_card_info(request))

                card.card_num = request.data['card_num']
                card.cvc = request.data['cvc']
                card.card_holder_name = request.data['card_holder_name']
                card.expire_date = request.data['expire_date']
                card.save()

                # save to exactly origin card object, so for payments, the card_num shall all change
                # only update card_num info for future payments

                queryset_future = Payment.objects.filter(date__gte=date.today(), status = 'UNPAID')
                for instance in queryset_future:
                    instance.card = card
                    instance.save()

                queryset_today_unpaid = Payment.objects.filter(date=date.today(), status='UNPAID')
                for instance in queryset_today_unpaid:
                    instance.card = card
                    instance.save()

                serializer = CardSerializer(card)
                return Response(serializer.data)

        # delete
        elif request.data['action'] == 'delete':
            card = check_valid_card(request)
            if not card:
                return Response('No card to delete')
            else:
                queryset_unpaid = Payment.objects.filter(status='UNPAID')
                for instance in queryset_unpaid:
                    instance.card =None
                    instance.save()
                card.delete()
                return Response('Card deleted successfully')

        # add
        elif request.data['action'] == 'add':
            card = check_valid_card(request)
            if card:
                return Response("You've have card info, please update")
            else:
                if validate_card_info(request):
                    return Response(validate_card_info(request))

                card = Card.objects.create(
                    user=OurUser.objects.get(username=request.user.username),
                    card_num=request.data['card_num'],
                    cvc=request.data['cvc'],
                    card_holder_name=request.data['card_holder_name'],
                    expire_date=request.data['expire_date']
                    )
                card.save()

                queryset_future = Payment.objects.filter(date__gte=date.today(), status = 'UNPAID')
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

# """
# MakePayment:
# - Update UserSubscription Payment status & Plan Start Date
# - Update Payment History
# """
# class MakePayment(APIView):
#
#     permission_classes = [IsAuthenticated]
#     serializer_class = PaymentSerializer
#
#     def get(self, request, payment_id):
#         payment = check_valid_payment(request, payment_id)
#         if payment:
#             serializer = PaymentSerializer(payment)
#             return Response(serializer.data)
#
#     def post(self, request, payment_id):
#
#         payment = check_valid_payment(request, payment_id)
#         if not payment:
#             return Response("This payment does not exist")
#         else:
#             if payment.status == 'SUCCESS':
#                 return Response("This payment has been made already")
#             elif payment.status == 'CANCELLED':
#                 return Response('This payment has been cancelled already')
#             else:
#                 if payment.date > date.today():
#                     return Response('This payment is scheduled for future')
#                 else:
#                     card = check_valid_card(request)
#                     if not card:
#                         return Response("You don't have valid card")
#                     else:
#                         payment = finish_current_create_next_payment(request, payment_id)
#                         if not payment:
#                             return Response("Payment not made")
#                         else:
#                             return Response("Payment success")
