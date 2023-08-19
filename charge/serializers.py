from rest_framework import serializers
from charge.models import Seller, Customer, CreditRequest, ChargeRequest


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['id', 'name', 'credit']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['phone', 'first_name', 'last_name', 'charge']


class CreditRequestViewSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.name')

    class Meta:
        model = CreditRequest
        fields = ['id', 'seller_name', 'amount']


class CreditRequestCreateSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data.get('amount', 0) < 0:
            raise serializers.ValidationError(
                {'amount': 'amount cannot be negative'})
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
    customer_phone = serializers.CharField(
        source='customer.phone', read_only=True)

    def validate(self, data):
        if data.get('amount', 0) < 0:
            raise serializers.ValidationError(
                {'amount': 'amount cannot be negative'})
        if 'seller' not in data:
            raise serializers.ValidationError(
                {'seller': 'seller cannot be empty'})
        return data

    class Meta:
        model = ChargeRequest
        fields = ['seller', 'customer', 'customer_phone', 'amount']
