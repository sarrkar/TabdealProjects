from django.test import TestCase
from charge.models import ChargeRequest, CreditRequest, Seller

class SellerModelTest(TestCase):
    
    def test_name_max_length(self):
        seller = Seller.objects.get(id=1)
        max_length = seller._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)
    
    def test_object_name_is_str(self):
        seller = Seller.objects.get(id=1)
        expected_object_name = self.name
        self.assertEqual(str(seller), expected_object_name)
    
    def test_get_absolute_url(self):
        seller = Seller.objects.get(id=1)
        self.assertEqual(seller.get_absolute_url(), 'sellers/1')
    
    def test_amount(self):
        pass