from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Product
from . import validators

class ProductSerializer(serializers.ModelSerializer):
  product_discount = serializers.SerializerMethodField(read_only=True)
  edit_url =serializers.SerializerMethodField(read_only=True)
  url = serializers.HyperlinkedIdentityField(
    view_name='product-detail',
    lookup_field='pk'
  )
  title = serializers.CharField(validators=[validators.validate_title_no_hello, 
                                            validators.unique_product_title])
  # email = serializers.CharField(source='user.email', read_only=True)
  
  
  
  class Meta:
    model = Product
    fields = [
      'url',
      'edit_url',
      'pk',
      'title',
      # 'email',
      'content',
      'price',
      'sale_price',
      'product_discount'
    ]

  # def create(self, validated_data):
  #   email = validated_data.pop('email')
  #   title = validated_data.get('title')
  #   content = validated_data.get('content')
  #   if content is None:
  #     content = title
  #   obj = super().create(validated_data)
  #   print(email, obj.content)
  #   return obj

  # can be moved to validators and called here or basically validate in the models
  # def validate_title(self, value):
  #   qs = Product.objects.filter(title__iexact=value)
  #   if qs:
  #     raise serializers.ValidationError(f"{value} is already exists, Title must be Unique")
  #   return value

  def get_product_discount(self, obj):
    if not hasattr(obj, 'id'):
      return None
    if not isinstance(obj, Product):
      return None
    return obj.get_discount()
  
  def get_edit_url(self, obj):
    request = self.context.get("request")
    if request is None:
      None
    return reverse("product-edit", kwargs={"pk": obj.pk}, request=request)