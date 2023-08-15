from django.contrib import admin

from charge.models import ChargeRequest, CreditRequest, Customer, Seller

admin.site.register(Seller)
admin.site.register(Customer)
admin.site.register(CreditRequest)
admin.site.register(ChargeRequest)