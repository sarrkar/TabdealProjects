from sre_constants import SUCCESS
from django.db import models, transaction, IntegrityError
from django.db.models import F


class Seller(models.Model):

    def __str__(self) -> str:
        return self.name

    name = models.CharField(max_length=50)
    credit = models.BigIntegerField(default=0)


class Customer(models.Model):
    class Meta:
        indexes = [models.Index(fields=['phone',])]

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=11, unique=True)
    charge = models.PositiveBigIntegerField(default=0)


class CreditRequest(models.Model):

    def __str__(self) -> str:
        return f'{self.seller} : {self.amount}'

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

    def __str__(self) -> str:
        return f'{self.seller} - {self.customer} : {self.amount} - {self.status}'

    seller = models.ForeignKey(Seller, null=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET_NULL)
    amount = models.PositiveBigIntegerField()
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=REQUESTED)

    def save(self, *args, **kwargs):
        if self.status != ChargeRequest.REQUESTED:
            raise IntegrityError('cannot change status')
        try:
            self.charge()
            super(ChargeRequest, self).save(*args, **kwargs)
        except IntegrityError:
            self.status = ChargeRequest.FAILED
            super(ChargeRequest, self).save(*args, **kwargs)
            raise IntegrityError('seller credit lower than amount')

    def charge(self):
        with transaction.atomic():
            self.seller.credit = F('credit') - self.amount
            self.seller.save()
            self.customer.charge = F('charge') + self.amount
            self.customer.save()
            self.seller.refresh_from_db()
            if self.seller.credit < 0:
                raise IntegrityError('seller credit lower than amount')
            self.status = ChargeRequest.SUCCESSFUL
