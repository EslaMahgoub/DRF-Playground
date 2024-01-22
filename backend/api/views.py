import json
from django.forms.models import model_to_dict
# from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.serializers import ProductSerializer

from products.models import Product

@api_view(['POST'])
def api_home(request, *args, **kwargs):
  # instance = Product.objects.all().order_by("?").first()
  # data = {}
  # if instance:
  #   # seriallization
  #   # data = model_to_dict(instance, fields=['id', 'title', 'price', 'sale_price'])
  #   data = ProductSerializer(instance).data
  serializer = ProductSerializer(data=request.data)
  if serializer.is_valid(raise_exception=True):
    # instance = serializer.save()
    print(serializer.data)
    return Response(serializer.data)
  return Response({"invalid": "Not valid"}, status=400)