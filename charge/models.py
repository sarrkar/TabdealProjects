from sre_constants import SUCCESS
from django.db import models, transaction, IntegrityError
from django.db.models import F


class Seller(models.Model):
    name = models.CharField(max_length=50)
    credit = models.BigIntegerField(default=0)


class Customer(models.Model):
    class Meta:
        indexes = [models.Index(fields=['phone',])]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11, unique=True)
    charge = models.PositiveBigIntegerField(default=0)


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
    REQUESTED = 'R'
    SUCCESSFUL = 'S'
    FAILED = 'F'

    STATUS_CHOICES = [
        (REQUESTED, 'REQUESTED'),
        (SUCCESSFUL, 'SUCCESSFUL'),
        (FAILED, 'FAILED'),
    ]

    seller = models.ForeignKey(Seller, null=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET_NULL)
    amount = models.PositiveBigIntegerField()
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=REQUESTED)

    def charge(self):
        with transaction.atomic():
            self.seller.credit = F('credit') - self.amount
            self.customer.charge = F('charge') + self.amount
            self.seller.save()
            self.customer.save()
            if self.seller.credit < 0:
                self.status = ChargeRequest.FAILED
                self.save()
                raise IntegrityError('seller credit lower than amount')
            self.status = ChargeRequest.SUCCESSFUL
            self.save()
