from django.http import JsonResponse
from rest_framework import status

from shipayapi.serializers import EstablishmentSerializer, TransactionSerializer


def map_post_response():
    """
    Creates an object of type JsonResponse that represents a well succeeded transaction creation.

    Returns:
        JsonResponse:A JSON response object with status code 201.
    """
    return JsonResponse(
        {
            'aceito': 'true'
        },
        safe=False,
        status=status.HTTP_201_CREATED
    )


def map_invalid_post_response():
    """
    Creates an object of type JsonResponse that represents a failed transaction creation.

    Returns:
        JsonResponse:A JSON response object with status code 400.
    """
    return JsonResponse(
        {
            'aceito': 'false'
        },
        safe=False,
        status=status.HTTP_400_BAD_REQUEST
    )


def map_get_response(establishment_dictionary: EstablishmentSerializer, transactions_dictionary: TransactionSerializer):
    """
    Maps information about the establishment, all transactions on the site, and the sum total of transactions
    to a response in JSON format.

    Parameters:
        establishment_dictionary (EstablishmentSerializer):The dictionary with information about the related establishment.
        transactions_dictionary (TransactionSerializer):The dictionary with information about all transactions realized in establishment.

    Returns:
        JsonResponse:A JSON response object with status code 200.
    """
    transactions_total = calculate_transactions_total(transactions_dictionary.data)
    return JsonResponse(
        {
            'estabelecimento': establishment_dictionary.data[0],
            'recebimentos': transactions_dictionary.data,
            'total_recebidos': transactions_total
        },
        safe=False,
        status=status.HTTP_200_OK
    )


def calculate_transactions_total(transactions_list):
    transaction_total = 0
    for current_transaction in transactions_list:
        transaction_total = transaction_total + current_transaction.get('amount', 0)
    return transaction_total
