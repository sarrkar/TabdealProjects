from rest_framework import serializers
from charge.models import Seller, Customer, CreditRequest, ChargeRequest
import re

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['id', 'name', 'credit']

class CustomerSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if re.match(r'^09\d{9}$', data['phone']) is None:
            raise serializers.ValidationError({'phone': 'invalid phone number'})
        return data

    class Meta:
        model = Customer
        fields = ['id', 'phone', 'first_name', 'last_name', 'charge']

class CreditRequestSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.name')

    class Meta:
        model = CreditRequest
        fields = ['id', 'seller_name', 'amount']

class ChargeRequestSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.name')
    customer_phone = serializers.CharField(source='customer.phone')

    class Meta:
        model = ChargeRequest
        fields = ['id', 'seller_name', 'customer_phone', 'status']