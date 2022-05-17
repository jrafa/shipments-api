import uuid

from django.db import models

from api.constants import MAX_LENGTH, ZIPCODE_LENGTH


class Customer(models.Model):
    first_name = models.CharField(max_length=MAX_LENGTH)
    last_name = models.CharField(max_length=MAX_LENGTH)
    address = models.CharField(max_length=MAX_LENGTH)
    city = models.CharField(max_length=MAX_LENGTH)
    zipcode = models.CharField(max_length=ZIPCODE_LENGTH)
    email = models.EmailField()

    class Meta:
        abstract = True


class Shipment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post_date = models.DateTimeField()
    received_date = models.DateTimeField()

    def __str__(self):
        return f'Shipment id: {self.id}'


class Sender(Customer):
    shipments = models.ManyToManyField(Shipment, related_name='sender', blank=True)

    def __str__(self):
        return f'Sender id: {self.id}'


class Recipient(Customer):
    shipments = models.ManyToManyField(Shipment, related_name='recipient', blank=True)

    def __str__(self):
        return f'Recipient id: {self.id}'
