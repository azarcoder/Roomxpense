from django.contrib import admin
from . models import Room,Person,Transaction,TransactionDetail
# Register your models here.
admin.site.register(Room)
admin.site.register(Person)
admin.site.register(Transaction)
admin.site.register(TransactionDetail)