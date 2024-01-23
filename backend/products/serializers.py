from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Product
from . import validators
from api.serializers import UserPublicSerializer

class UserProductInlineSerializer(serializers.Serializer):
  url = serializers.HyperlinkedIdentityField(
    view_name='product-detail',
    lookup_field='pk',
    read_only=True
  )

  title = serializers.CharField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
  owner = UserPublicSerializer(source='user', read_only=True)
  title = serializers.CharField(validators=[validators.validate_title_no_hello, 
                                            validators.unique_product_title])
  
  body = serializers.CharField(source='content')
  class Meta:
    model = Product
    fields = [
      'owner',
      'pk',
      'title',
      'body',
      'price',
      'sale_price',
      'public',
      'path',
      'endpoint'
    ]
