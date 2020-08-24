import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_condition import Or
from rest_framework import generics, status

# Create your views here.
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from shipaypdv.shipayapi.mappers import map_post_response, map_get_response, map_invalid_post_response
from shipaypdv.shipayapi.models import Post
from shipaypdv.shipayapi.persistency import create_transaction
from shipaypdv.shipayapi.serializers import TransactionSerializer
from shipaypdv.shipayapi.validations import validate_post_body


@api_view(["POST"])
def add_posts(request):
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
def retrieve_posts(request):
    user = request.user.id
    posts = Post.objects.filter(created_by_user=user)
    serializer_response = TransactionSerializer(posts, many=True)
    return map_get_response(serializer_response)
