from rest_framework import serializers

from .models import Payment

class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Payment
        fields = ('credit_card_number', 'card_holder', 'expiration_date', 'security_code', 'amount') 

