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
        if data['charge'] < 0:
            raise serializers.ValidationError({'charge': 'charge cannot be negative'})
        return data

    class Meta:
        model = Customer
        fields = ['id', 'phone', 'first_name', 'last_name', 'charge']

class CreditRequestViewSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.name')

    class Meta:
        model = CreditRequest
        fields = ['id', 'seller_name', 'amount']

class CreditRequestCreateSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['amount'] < 0:
            raise serializers.ValidationError({'amount': 'amount cannot be negative'})
        return data

    class Meta:
        model = CreditRequest
        fields = ['id', 'seller', 'amount']

class ChargeRequestViewSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.name')
    customer_phone = serializers.CharField(source='customer.phone')

    class Meta:
        model = ChargeRequest
        fields = ['id', 'seller_name', 'customer_phone', 'amount', 'status']

class ChargeRequestCreateSerializer(serializers.ModelSerializer):
    customer_phone = serializers.CharField(source='customer.phone', read_only=True)

    def validate(self, data):
        if data['amount'] < 0:
            raise serializers.ValidationError({'amount': 'amount cannot be negative'})
        if data['seller'] is None:
            raise serializers.ValidationError({'seller': 'seller cannot be empty'})
        return data

    class Meta:
        model = ChargeRequest
        fields = ['id', 'seller', 'customer', 'customer_phone', 'amount']