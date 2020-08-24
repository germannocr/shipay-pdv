from rest_framework import serializers

from shipaypdv.shipayapi.models import User, Post


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'
