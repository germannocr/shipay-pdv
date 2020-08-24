import json

from django.http import JsonResponse
from rest_framework import status

# Create your views here.
from rest_framework.decorators import api_view

from shipayapi.mappers import map_post_response, map_get_response, map_invalid_post_response
from shipayapi.models import Transaction, Establishment
from shipayapi.persistency import create_transaction
from shipayapi.serializers import TransactionSerializer
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

    except Exception as e:
        return JsonResponse({
            'error': str(e)
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
        raise Exception
    transaction_dictionary = TransactionSerializer(transactions, many=True)
    establishment_dictionary = TransactionSerializer(establishment_object, many=True)
    return map_get_response(transaction_dictionary, establishment_dictionary)
