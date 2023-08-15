from rest_framework import generics, mixins
from rest_framework.response import Response
from charge.models import ChargeRequest, CreditRequest, Customer, Seller
from charge.serializers import ChargeRequestCreateSerializer, ChargeRequestViewSerializer, CreditRequestCreateSerializer, CreditRequestViewSerializer, CustomerSerializer, SellerSerializer


class SellerList(generics.ListCreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class SellerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
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
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        CreditRequestList.serializer_class = CreditRequestCreateSerializer
        return self.create(request, *args, **kwargs)

class ChargeRequestList(generics.ListCreateAPIView):
    queryset = ChargeRequest.objects.all()
    serializer_class = ChargeRequestViewSerializer

    def get(self, request, *args, **kwargs):
        ChargeRequestList.serializer_class = ChargeRequestViewSerializer
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ChargeRequestList.serializer_class = ChargeRequestCreateSerializer
        customer = Customer.objects.get(phone=request.data['customer_phone'])
        request.data['customer'] = customer.pk
        return self.create(request, *args, **kwargs)

class ChargeRequestCharge(generics.GenericAPIView):
    queryset = ChargeRequest.objects.all()
    serializer_class = ChargeRequestViewSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.charge()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
