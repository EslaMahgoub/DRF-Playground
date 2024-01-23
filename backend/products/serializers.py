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
  edit_url =serializers.SerializerMethodField(read_only=True)
  url = serializers.HyperlinkedIdentityField(
    view_name='product-detail',
    lookup_field='pk'
  )
  title = serializers.CharField(validators=[validators.validate_title_no_hello, 
                                            validators.unique_product_title])
  
  
  
  class Meta:
    model = Product
    fields = [
      'owner',
      'url',
      'edit_url',
      'pk',
      'title',
      'content',
      'price',
      'sale_price',
    ]

  def get_edit_url(self, obj):
    request = self.context.get("request")
    if request is None:
      None
    return reverse("product-edit", kwargs={"pk": obj.pk}, request=request)