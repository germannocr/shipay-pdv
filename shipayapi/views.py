import json

from django.http import JsonResponse
from rest_framework import status

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException

from shipayapi.exceptions import MissingCnpjValue, UnexistentEstablisment
from shipayapi.mappers import map_post_response, map_get_response, map_invalid_post_response
from shipayapi.models import Transaction, Establishment
from shipayapi.persistency import create_transaction
from shipayapi.serializers import TransactionSerializer, EstablishmentSerializer
from shipayapi.validations import validate_post_body


@api_view(["POST"])
def add_transaction(request):
    request_body = json.loads(request.body)
    try:
        validate_post_body(request_body=request_body)
        new_transaction = create_transaction(request_body=request_body)
        if new_transaction:
            mapped_response = map_post_response()
            return mapped_response
        else:
            mapped_response = map_invalid_post_response()
            return mapped_response

    except APIException as custom_exception:
        return JsonResponse({
            'aceito': 'false',
            'more info': custom_exception.default_detail
        },
            safe=False,
            status=custom_exception.status_code
        )

    except Exception as exception:
        return JsonResponse({
            'error': str(exception)
        },
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def retrieve_transactions(request):
    establishment_cnpj = request.query_params.get('cnpj', None)
    if establishment_cnpj:
        establishment_object = Establishment.objects.filter(cnpj=establishment_cnpj)
        transactions = Transaction.objects.filter(establishment=establishment_cnpj)
    else:
        raise MissingCnpjValue(code=400)
    if establishment_object:
        transaction_dictionary = TransactionSerializer(transactions, many=True)
        establishment_dictionary = EstablishmentSerializer(establishment_object, many=True)
        return map_get_response(transactions_dictionary=transaction_dictionary,
                                establishment_dictionary=establishment_dictionary)
    else:
        raise UnexistentEstablisment(code=404)
