import datetime

from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Shipment, Sender, Recipient


def create_shipment(shipment_id):
    return Shipment.objects.create(
        post_date=datetime.datetime(2022, 5, 31, 10, 5, 59, tzinfo=datetime.timezone.utc),
        received_date=datetime.datetime(2022, 6, 1, 12, 40, 52, tzinfo=datetime.timezone.utc),
        id=shipment_id,
    )


def count_shipments():
    return Shipment.objects.count()


def create_sender(shipments):
    sender = Sender(
        first_name='Nina',
        last_name='Pastori',
        address='Garcia 10',
        city='Barcelona',
        zipcode='12345',
        email='ninap@gmail.com',
    )
    sender.save()
    sender.shipments.add(shipments)
    return sender


def create_recipient(shipments):
    recipient = Recipient(
        first_name='Rosario',
        last_name='Flores',
        address='Sol 99',
        city='Madrid',
        zipcode='12345',
        email='rosariof@gmail.com',
    )
    recipient.save()
    recipient.shipments.add(shipments)
    return recipient


class ShipmentTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.shipment_1 = create_shipment('575c2acd-be7e-4c62-a319-225d2619b176')
        cls.shipment_2 = create_shipment('6c66ebfd-541c-43d2-8bee-168718e30ee8')
        cls.shipment_3 = create_shipment('c2fd278b-c97f-46ba-9b81-e919efe8bf60')
        cls.sender = create_sender(cls.shipment_1)
        cls.recipient = create_recipient(cls.shipment_1)

    def test_get_all_shipments_with_success(self):
        # when
        response = self.client.get('/api/v1/shipments', format='json')

        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            [
                {
                    'id': '575c2acd-be7e-4c62-a319-225d2619b176',
                    'post_date': '2022-05-31T10:05:59Z',
                    'received_date': '2022-06-01T12:40:52Z',
                    'sender': [
                        {
                            'id': 1,
                            'first_name': 'Nina',
                            'last_name': 'Pastori',
                            'address': 'Garcia 10',
                            'city': 'Barcelona',
                            'zipcode': '12345',
                            'email': 'ninap@gmail.com',
                        }
                    ],
                    'recipient': [
                        {
                            'id': 1,
                            'first_name': 'Rosario',
                            'last_name': 'Flores',
                            'address': 'Sol 99',
                            'city': 'Madrid',
                            'zipcode': '12345',
                            'email': 'rosariof@gmail.com',
                        }
                    ],
                },
                {
                    'id': '6c66ebfd-541c-43d2-8bee-168718e30ee8',
                    'post_date': '2022-05-31T10:05:59Z',
                    'received_date': '2022-06-01T12:40:52Z',
                    'sender': [],
                    'recipient': [],
                },
                {
                    'id': 'c2fd278b-c97f-46ba-9b81-e919efe8bf60',
                    'post_date': '2022-05-31T10:05:59Z',
                    'received_date': '2022-06-01T12:40:52Z',
                    'sender': [],
                    'recipient': [],
                },
            ],
        )

    def test_get_shipment_with_success(self):
        # when
        response = self.client.get(
            '/api/v1/shipments/575c2acd-be7e-4c62-a319-225d2619b176', format='json'
        )

        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'id': '575c2acd-be7e-4c62-a319-225d2619b176',
                'post_date': '2022-05-31T10:05:59Z',
                'received_date': '2022-06-01T12:40:52Z',
                'sender': [
                    {
                        'id': 1,
                        'first_name': 'Nina',
                        'last_name': 'Pastori',
                        'address': 'Garcia 10',
                        'city': 'Barcelona',
                        'zipcode': '12345',
                        'email': 'ninap@gmail.com',
                    }
                ],
                'recipient': [
                    {
                        'id': 1,
                        'first_name': 'Rosario',
                        'last_name': 'Flores',
                        'address': 'Sol 99',
                        'city': 'Madrid',
                        'zipcode': '12345',
                        'email': 'rosariof@gmail.com',
                    }
                ],
            },
        )

    def test_get_shipment_not_found(self):
        # when
        response = self.client.get('/api/v1/shipments/1', format='json')

        # then
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_shipment_with_success(self):
        # when
        response = self.client.delete(
            '/api/v1/shipments/c2fd278b-c97f-46ba-9b81-e919efe8bf60', format='json'
        )

        # then
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(count_shipments(), 2)

    def test_create_shipment_with_success(self):
        data = {
            'post_date': '2022-05-31T10:50:59Z',
            'received_date': '2022-06-01T12:45:52Z',
            'sender': [
                {
                    'first_name': 'Abc',
                    'last_name': 'Abc',
                    'address': 'Abc 10',
                    'city': 'Toledo',
                    'zipcode': '12345',
                    'email': 'abc@gmail.com',
                }
            ],
            'recipient': [
                {
                    'first_name': 'Mercedes',
                    'last_name': 'Lopez',
                    'address': 'Gutierez 10',
                    'city': 'Bilbao',
                    'zipcode': '12345',
                    'email': 'mercedes.lopez@gmail.com',
                }
            ],
        }

        # when
        response = self.client.post('/api/v1/shipments', data, format='json')

        # then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(count_shipments(), 4)

    def test_update_shipment_with_success(self):
        data = {
            'post_date': '2022-05-01T10:50:59Z',
            'received_date': '2022-05-02T12:45:52Z',
        }

        # when
        response = self.client.patch(
            '/api/v1/shipments/c2fd278b-c97f-46ba-9b81-e919efe8bf60', data, format='json'
        )

        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'id': 'c2fd278b-c97f-46ba-9b81-e919efe8bf60',
                'post_date': '2022-05-01T10:50:59Z',
                'received_date': '2022-05-02T12:45:52Z',
                'sender': [],
                'recipient': [],
            },
        )
