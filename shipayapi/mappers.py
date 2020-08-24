from django.http import JsonResponse
from rest_framework import status


def map_post_response():
    return JsonResponse(
        {
            'aceito': 'true'
        },
        safe=False,
        status=status.HTTP_201_CREATED
    )


def map_invalid_post_response():
    return JsonResponse(
        {
            'aceito': 'false'
        },
        safe=False,
        status=status.HTTP_400_BAD_REQUEST
    )


def map_get_response(establishment_dictionary, transactions_dictionary):
    transactions_total = calculate_transactions_total(transactions_dictionary.data)
    return JsonResponse(
        {
            'estabelecimento': establishment_dictionary.data,
            'recebimentos': transactions_dictionary.data,
            'total_recebidos': transactions_total
        },
        safe=False,
        status=status.HTTP_200_OK
    )


def calculate_transactions_total(transactions_list):
    transaction_total = 0.0
    for current_transaction in transactions_list:
        transaction_total = transaction_total + current_transaction.get('amount', 0.0)
    return transaction_total
