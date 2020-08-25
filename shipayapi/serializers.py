from rest_framework import serializers

from shipayapi.models import Establishment, Transaction


class EstablishmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Establishment
        fields = ['name', 'cnpj', 'owner', 'phone']


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['establishment', 'description', 'amount', 'customer']
