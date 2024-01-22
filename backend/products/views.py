from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.mixins import (
  StaffEditorPermissionMixin,
  UserQuerySetMixin)

from .models import Product
from .serializers import ProductSerializer

class ProductListCreateAPIView(
  UserQuerySetMixin,
  StaffEditorPermissionMixin, 
  generics.ListCreateAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  # user_field = 'owner' use to override the user_field in the UserQuerySetMixin
  
  def perform_create(self, serializer):
    # serializer.save(user=self.request.user)
    print(serializer.validated_data)
    title = serializer.validated_data.get('title')
    content = serializer.validated_data.get('content')
    if content is None:
      content = title
    serializer.save(content=content, user=self.request.user)
  
  # moved to mixin to use it everywhere
  # def get_queryset(self):
  #   qs = super().get_queryset()
  #   request = self.request
  #   user = request.user
  #   if not user.is_authenticated:
  #     return Product.objects.none()
  #   return qs.filter(user=request.user)

product_list_create_view = ProductListCreateAPIView.as_view()

class ProductDetailAPIView(
  UserQuerySetMixin,
  StaffEditorPermissionMixin,
  generics.RetrieveAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  # lookup_fields = 'pk'

product_detail_view = ProductDetailAPIView.as_view()

class ProductUpdateAPIView(
  UserQuerySetMixin,
  StaffEditorPermissionMixin, 
  generics.UpdateAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  lookup_fields = 'pk'

  def perform_update(self, serializer):
    instance = serializer.save()
    if not instance.content:
      instance.content = instance.title
      ## serializer.save()

product_update_view = ProductUpdateAPIView.as_view()

class ProductDestroyAPIView(
  UserQuerySetMixin,
  StaffEditorPermissionMixin, 
  generics.DestroyAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  lookup_fields = 'pk'

  def perform_destory(self, instance):
      super().perform_destroy(instance)


product_delete_view = ProductDestroyAPIView.as_view()