from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, related_name='rooms', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Room'

class Person(models.Model):
    name = models.CharField(max_length = 100)
    email = models.EmailField(unique = True)
    contact = models.CharField(max_length = 8)
    room = models.ForeignKey(Room, related_name='people', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    balance = models.FloatField(default=0)
    paid = models.FloatField(default=0)
    charged = models.FloatField(default=0)


    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Person'

class Transaction(models.Model):
    product = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    persons = models.ManyToManyField(Person, through='TransactionDetail', through_fields=('transaction', 'person'))

    def __str__(self):
        return self.product

    class Meta:
        db_table = 'Transaction'

class TransactionDetail(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    paid = models.FloatField()
    who_paid = models.ForeignKey(Person, related_name='transactions_paid', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.person.name} - {self.transaction.product}'

    class Meta:
        db_table = 'TransactionDetail'
