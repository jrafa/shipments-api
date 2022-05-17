from rest_framework import serializers

from api.models import Shipment, Sender, Recipient

from drf_writable_nested.serializers import WritableNestedModelSerializer


class SenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sender
        fields = ['id', 'first_name', 'last_name', 'address', 'city', 'zipcode', 'email']


class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = ['id', 'first_name', 'last_name', 'address', 'city', 'zipcode', 'email']


class ShipmentSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    sender = SenderSerializer(many=True)
    recipient = RecipientSerializer(many=True)

    class Meta:
        model = Shipment
        fields = ['id', 'post_date', 'received_date', 'sender', 'recipient']
