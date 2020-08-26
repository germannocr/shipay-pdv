import json

from django.test import TestCase, Client
from rest_framework import status

from shipayapi.models import Establishment, Transaction

client = Client()
API_URL = 'http://localhost:8000/api/v1/'


# Create your tests here.
class CreateTransactionsTest(TestCase):

    def setUp(self):
        Establishment.objects.create(
            id=1,
            name="Nosso Restaurante",
            cnpj="45.283.163/0001-67",
            owner="Fabio",
            phone="99999999999"
        )

        self.valid_payload = {
            "estabelecimento": "45.283.163/0001-67",
            "cliente": "094.214.930-01",
            "valor": 590.01,
            "descricao": "Almoço em restaurante chique pago via Shipay!"
        }
        self.invalid_payload = {
            "estabelecimento": "63.754.223/0001-64",
            "cliente": "489.481.313-13",
            "valor": 100.01,
            "descricao": "Jantar em restaurante de esquina pago via Shipay!"
        }

    def test_create_transaction(self):
        response = client.post(
            f"{API_URL}transacao",
            data=json.dumps(self.valid_payload),
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content)
        self.assertEqual(response.get('aceito'), 'true')

        response = client.post(
            f"{API_URL}transacao",
            data=json.dumps(self.invalid_payload),
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = json.loads(response.content)
        self.assertEqual(response.get('aceito'), 'false')

    def test_create_transaction_with_wrong_parameters(self):
        invalid_data = {
            "estabelecimento": "63.754.223/0001-64",
            "cliente": 48948131313,
            "valor": 100.01,
            "descricao": "Jantar em restaurante de esquina pago via Shipay!"
        }
        response = client.post(
            f"{API_URL}transacao",
            data=json.dumps(invalid_data),
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        invalid_data = {
            "estabelecimento": "63.754.223/0001-64",
            "cliente": "489.481.313-13",
            "valor": "100.01",
            "descricao": "Jantar em restaurante de esquina pago via Shipay!"
        }
        response = client.post(
            f"{API_URL}transacao",
            data=json.dumps(invalid_data),
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        invalid_data = {
            "estabelecimento": "63.754.223/0001-64",
            "cliente": "489.481.313-13",
            "valor": "100.01",
            "descricao": 200
        }
        response = client.post(
            f"{API_URL}transacao",
            data=json.dumps(invalid_data),
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        invalid_data = {
            "estabelecimento": 550,
            "cliente": "489.481.313-13",
            "valor": "100.01",
            "descricao": "Jantar em restaurante de esquina pago via Shipay!"
        }
        response = client.post(
            f"{API_URL}transacao",
            data=json.dumps(invalid_data),
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_transaction_missing_fields(self):
        invalid_data = {
            "cliente": "094.214.930-01",
            "valor": 590.01,
            "descricao": "Almoço em restaurante chique pago via Shipay!"
        }
        response = client.post(
            f"{API_URL}transacao",
            data=json.dumps(invalid_data),
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        invalid_data = {
            "estabelecimento": "45.283.163/0001-67",
            "valor": 590.01,
            "descricao": "Almoço em restaurante chique pago via Shipay!"
        }
        response = client.post(
            f"{API_URL}transacao",
            data=json.dumps(invalid_data),
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        invalid_data = {
            "estabelecimento": "45.283.163/0001-67",
            "cliente": "094.214.930-01",
            "descricao": "Almoço em restaurante chique pago via Shipay!"
        }
        response = client.post(
            f"{API_URL}transacao",
            data=json.dumps(invalid_data),
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        invalid_data = {
            "estabelecimento": "45.283.163/0001-67",
            "cliente": "094.214.930-01",
            "valor": 590.01,
        }
        response = client.post(
            f"{API_URL}transacao",
            data=json.dumps(invalid_data),
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetAllTransactions(TestCase):
    def setUp(self):
        self.establishment_cnpj = '45.283.163/0001-67'
        Establishment.objects.create(
            id=1,
            name="Nosso Restaurante",
            cnpj=self.establishment_cnpj,
            owner="Fabio",
            phone="99999999999"
        )

        Transaction.objects.create(
            establishment=self.establishment_cnpj,
            description="Almoço",
            amount=500.00,
            customer="094.214.930-01"
        )

        Transaction.objects.create(
            establishment=self.establishment_cnpj,
            description="Jantar",
            amount=250.00,
            customer="094.214.930-01"
        )

        Transaction.objects.create(
            establishment=self.establishment_cnpj,
            description="Lanche",
            amount=100.00,
            customer="094.214.930-01"
        )

    def test_retrieve_all_transactions(self):
        response = client.get(
            f"{API_URL}transacoes/estabelecimento?cnpj={self.establishment_cnpj}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)
        self.assertEqual(response.get('estabelecimento').get('cnpj'), self.establishment_cnpj)
        self.assertEqual(response.get('total_recebidos'), '850.00')

        response = client.get(
                f"{API_URL}transacoes/estabelecimento?cnpj=63.754.223/0001-64",
            )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
