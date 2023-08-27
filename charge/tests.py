from django.test import TestCase
import random
from charge.models import ChargeRequest, CreditRequest, Customer, Seller
from charge.serializers import ChargeRequestCreateSerializer, CreditRequestCreateSerializer, CustomerSerializer


def get_random_phone_number():
    return f"09{random.randint(0, 999999999):09d}"


class RequestSerializerTest(TestCase):
    def setUp(self):
        RequestSerializerTest.seller = Seller.objects.create(
            name='Test Seller')
        RequestSerializerTest.customer = Customer.objects.create(
            phone='09123456789')

    def tearDown(self):
        RequestSerializerTest.seller.delete()
        RequestSerializerTest.customer.delete()

    def test_charge_request(self):
        request = ChargeRequestCreateSerializer(data={
            'amount': 1000,
            'seller': RequestSerializerTest.seller.pk,
            'customer': RequestSerializerTest.customer.pk,
        })
        self.assertTrue(request.is_valid())

        request = ChargeRequestCreateSerializer(data={
            'customer': RequestSerializerTest.customer.pk,
            'amount': 1000,
        })
        self.assertFalse(request.is_valid())

        request = ChargeRequestCreateSerializer(data={
            'customer': RequestSerializerTest.customer.pk,
            'amount': -1000,
            'seller': RequestSerializerTest.seller.pk,
        })
        self.assertFalse(request.is_valid())

    def test_credit_request(self):
        request = CreditRequestCreateSerializer(data={
            'seller': 1,
            'amount': 1000,
        })
        self.assertTrue(request.is_valid())

        request = CreditRequestCreateSerializer(data={
            'seller': 1,
            'amount': -1000,
        })
        self.assertFalse(request.is_valid())


class CreditModelTest(TestCase):
    def setUp(self):
        CreditModelTest.seller_1 = Seller.objects.create(name='Test Seller 1')
        CreditModelTest.seller_2 = Seller.objects.create(name='Test Seller 2')

    def tearDown(self):
        CreditModelTest.seller_1.delete()
        CreditModelTest.seller_2.delete()

    def test_credit_sum(self):
        credits_1 = [random.randint(1, 10000) for i in range(100)]
        credits_2 = [random.randint(1, 10000) for i in range(150)]
        for c in credits_1:
            CreditRequest(seller=CreditModelTest.seller_1, amount=c).save()
        for c in credits_2:
            CreditRequest(seller=CreditModelTest.seller_2, amount=c).save()
        CreditModelTest.seller_1.refresh_from_db()
        CreditModelTest.seller_2.refresh_from_db()
        self.assertEqual(CreditModelTest.seller_1.credit, sum(credits_1))
        self.assertEqual(CreditModelTest.seller_2.credit, sum(credits_2))


class ChargeModelTest(TestCase):
    def setUp(self):
        ChargeModelTest.seller_1 = Seller.objects.create(name='Test Seller 1')
        ChargeModelTest.seller_2 = Seller.objects.create(name='Test Seller 2')
        for i in range(10):
            CreditRequest(seller=ChargeModelTest.seller_1,
                          amount=random.randint(1000000, 10000000)).save()
            CreditRequest(seller=ChargeModelTest.seller_2,
                          amount=random.randint(1000000, 10000000)).save()
        ChargeModelTest.seller_1.refresh_from_db()
        ChargeModelTest.seller_2.refresh_from_db()

    def tearDown(self):
        ChargeModelTest.seller_1.delete()
        ChargeModelTest.seller_2.delete()

    def test_charge_apply(self):
        seller_1_credit = ChargeModelTest.seller_1.credit
        seller_2_credit = ChargeModelTest.seller_2.credit
        charges_1 = [random.randint(1, 10000) for i in range(1000)]
        charges_2 = [random.randint(1, 10000) for i in range(1000)]
        for c in charges_1:
            customer, created = Customer.objects.get_or_create(
                phone=get_random_phone_number())
            ChargeRequest(seller=ChargeModelTest.seller_1,
                          customer=customer, amount=c).save()
            seller_1_credit -= c
        for c in charges_2:
            customer, created = Customer.objects.get_or_create(
                phone=get_random_phone_number())
            ChargeRequest(seller=ChargeModelTest.seller_2,
                          customer=customer, amount=c).save()
            seller_2_credit -= c
        ChargeModelTest.seller_1.refresh_from_db()
        ChargeModelTest.seller_2.refresh_from_db()
        self.assertEqual(ChargeModelTest.seller_1.credit, seller_1_credit)
        self.assertEqual(ChargeModelTest.seller_2.credit, seller_2_credit)
