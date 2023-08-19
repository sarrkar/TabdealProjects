from rest_framework import generics, mixins, status
from rest_framework.response import Response
from django.db import IntegrityError
from charge.models import ChargeRequest, CreditRequest, Customer, Seller
from charge.serializers import ChargeRequestCreateSerializer, ChargeRequestViewSerializer, CreditRequestCreateSerializer, CreditRequestViewSerializer, CustomerSerializer, SellerSerializer


class SellerList(generics.ListAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class SellerDetail(generics.RetrieveAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDetail(generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get(phone=self.kwargs['phone'])


class CreditRequestList(generics.ListCreateAPIView):
    queryset = CreditRequest.objects.all()
    serializer_class = CreditRequestViewSerializer

    def get(self, request, *args, **kwargs):
        CreditRequestList.serializer_class = CreditRequestViewSerializer
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        CreditRequestList.serializer_class = CreditRequestCreateSerializer
        return super().post(request, *args, **kwargs)


class ChargeRequestList(generics.ListCreateAPIView):
    queryset = ChargeRequest.objects.all()
    serializer_class = ChargeRequestViewSerializer

    def get(self, request, *args, **kwargs):
        ChargeRequestList.serializer_class = ChargeRequestViewSerializer
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ChargeRequestList.serializer_class = ChargeRequestCreateSerializer
        customer = Customer.objects.get(phone=request.data['customer_phone'])
        request.data['customer'] = customer.pk
        return super().post(request, *args, **kwargs)


class ChargeRequestCharge(generics.GenericAPIView):
    queryset = ChargeRequest.objects.all()
    serializer_class = ChargeRequestViewSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.charge()
        except IntegrityError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
