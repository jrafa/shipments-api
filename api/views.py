from rest_framework.viewsets import ModelViewSet

from api.models import Shipment
from api.serializers import ShipmentSerializer


class ShipmentModelViewSet(ModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
