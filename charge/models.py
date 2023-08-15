from django.db import models, transaction
from django.db.models import F


class Seller(models.Model):
    name = models.CharField(max_length=50)
    credit = models.BigIntegerField()


class Customer(models.Model):
    class Meta:
        indexes = [models.Index(fields=['phone',])]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11, unique=True)


class CreditRequest(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField()

    def save(self, *args, **kwargs):
        if not self.pk:
            with transaction.atomic():
                self.seller.credit = F('credit') + self.amount
                self.seller.save()
                super(CreditRequest, self).save(*args, **kwargs)


class ChargeRequest(models.Model):

    STATUS_CHOICES = [
        ('R', 'REQUESTED'),
        ('S', 'SUCCESSFUL'),
        ('F', 'FAILED'),
    ]

    seller = models.ForeignKey(Seller, null=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    amount = models.PositiveBigIntegerField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
