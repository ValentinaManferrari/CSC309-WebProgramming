from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Subscription, UserSubscription, Payment, Card
from rest_framework.fields import CurrentUserDefault
from django.utils.text import slugify
import re
from datetime import datetime, date


class SubscriptionSerializer(ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('title', 'price', 'subscription_type')


class UserSubscriptionSerializer(ModelSerializer):

    user_username = serializers.CharField(source='user.username')
    plan_title = serializers.CharField(source='plan.title')

    class Meta:
        model = UserSubscription
        fields = ('user_username', 'plan_title', 'start_date',
                  'next_payment_date', 'next_plan')


class PaymentSerializer(ModelSerializer):

    class Meta:
        model = Payment
        # fields = ('user','card_num','date','amount','status','recurrence','recurrence_type')
        fields = "__all__"


class CardSerializer(ModelSerializer):

    class Meta:
        model = Card
        fields = "__all__"

    def save(self):
        user = CurrentUserDefault()
        card_num = self.validated_data['card_num']
        cvc = self.validated_data['cvc']
        card_holder_name = self.validated_data['card_holder_name']
        expire_date = self.validated_data['expire_date']

    def validate_card_num(self, card_num):
        # reference: https://stackoverflow.com/questions/9315647/regex-credit-card-number-tests
        rgx_visa = re.compile(r"^4[0-9]{12}(?:[0-9]{3})?$")
        rgx_master = re.compile(
            r"^5[1-5][0-9]{14}|^(222[1-9]|22[3-9]\\d|2[3-6]\\d{2}|27[0-1]\\d|2720)[0-9]{12}$")

        if not (re.fullmatch(rgx_visa, card_num) or re.fullmatch(rgx_master, card_num)):
            raise serializers.ValidationError('Enter a valid card number')
        return card_num

    def validate_cvc(self, cvc):
        rgx = re.compile(r"^\d{3}$")
        if not re.fullmatch(rgx, cvc):
            raise serializers.ValidationError("Enter a valid cvc")
        return cvc

    def validate_expire_date(self, expire_date):
        # date = datetime.strptime(expire_date, '%Y-%m-%d').date()
        if expire_date < date.today():
            raise serializers.ValidationError("Enter a valid date")
        return expire_date
