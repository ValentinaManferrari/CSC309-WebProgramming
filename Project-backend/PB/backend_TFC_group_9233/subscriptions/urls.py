from django.urls import path
from .views import Subscribe, PaymentList, UpdateUserSubscription, \
  CardList
# , MakePayment

app_name = 'subscriptions'

urlpatterns = [
  path('api/view/all/', Subscribe.as_view(), name='view_all_subscription_choice'),
  path('api/my_subscription/', UpdateUserSubscription.as_view(), name='update_user_subscription'),
  path('api/payment/view/', PaymentList.as_view(), name='view_all_payments'),
  # path('api/payment/<int:payment_id>/', MakePayment.as_view(), name='make_payment'),
  path('api/card/', CardList.as_view(), name='view_and_edit_cards'),
]

"""
User subscribe plan, then make payment for the plan.
Once press subscribe, the plan is on hold for user with paid status = False. 
                      User also lose previous subscription.
Once payment made, the plan paid status = True.
"""