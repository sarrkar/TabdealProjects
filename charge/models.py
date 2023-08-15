from django.db import models


class Seller(models.Model):
    name = models.CharField(max_length=50)
    credit = models.BigIntegerField()


class Customer(models.Model):
    class Meta:
        indexes = [models.Index(fields=['phone',])]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11, unique=True)
