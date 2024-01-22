from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateAPIView(generics.ListCreateAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer

  def perform_create(self, serializer):
    # serializer.save(user=self.request.user)
    print(serializer.validated_data)
    title = serializer.validated_data.get('title')
    content = serializer.validated_data.get('content')
    if content is None:
      content = title
    serializer.save(content=content)
    # send a Django Signal

product_list_create_view = ProductListCreateAPIView.as_view()

class ProductDetailAPIView(generics.RetrieveAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  # lookup_fields = 'pk'


product_detail_view = ProductDetailAPIView.as_view()


class ProductUpdateAPIView(generics.UpdateAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  lookup_fields = 'pk'

  def perform_update(self, serializer):
    instance = serializer.save()
    if not instance.content:
      instance.content = instance.title
      ## serializer.save()


product_update_view = ProductUpdateAPIView.as_view()

class ProductDestroyAPIView(generics.DestroyAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  lookup_fields = 'pk'

  def perform_destory(self, instance):
      # instance
      super().perform_destroy(instance)


product_delete_view = ProductDestroyAPIView.as_view()

# class ProductListAPIView(generics.ListAPIView):
#   """
#   Not Gonna use it because we can use ListCreateAPIViewe at the top
#   """
#   queryset = Product.objects.all()
#   serializer_class = ProductSerializer
#   # lookup_fields = 'pk'

# product_detail_view = ProductDetaiAPIView.as_view()

class ProductMixinView(
  mixins.CreateModelMixin,
  mixins.ListModelMixin,
  mixins.RetrieveModelMixin,
  mixins.UpdateModelMixin,
  mixins.DestroyModelMixin,
  generics.GenericAPIView
  ):

  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  lookup_fields = 'pk'

  
  def get(self, request, *args, **kwargs):
    pk = kwargs.get("pk")
    if pk is not None:
      return self.retrieve(request, *args, **kwargs)
    return self.list(request, *args, **kwargs)
  
  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)
  
  def perform_create(self, serializer):
    # serializer.save(user=self.request.user)
    print(serializer.validated_data)
    title = serializer.validated_data.get('title')
    content = serializer.validated_data.get('content')
    if content is None:
      content = title
    serializer.save(content=content)
  
  def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

  def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

product_mixin_view = ProductMixinView.as_view()

# combine list, detail and create in one method
# @api_view(['GET', 'POST'])
# def product_alt_view(request, pk=None, *args, **kwargs):
#   method = request.method # PUT -> update and DESTROY -> delete
#   if method == 'GET':
#     if pk is not None:
#       obj = get_object_or_404(Product, pk=pk)
#       data = ProductSerializer(obj, many=False).data
#       return Response(data)
#     queryset = Product.objects.all()
#     data = ProductSerializer(queryset, many=True).data
#     return Response(data)

#   if method == 'POST':
#     serializer = ProductSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#       title = serializer.validated_data.get('title')
#       content = serializer.validated_data.get('content')
#       if content is None:
#         content = title
#       serializer.save(content=content)
#       print(serializer.data)
#       return Response(serializer.data)
#     return Response({"invalid": "Not valid"}, status=400)
