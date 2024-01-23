import random
from django.db import models
from django.conf import settings
from django.db.models import Q
from django.db.models.query import QuerySet
from django.urls import reverse

User = settings.AUTH_USER_MODEL # auth.User

#TODO: use ForeignKey model instead of list
TAGS_MODEL_VALUES = ['electronics', 'cars', 'boats', 'movies', 'cameras']

class ProductQuerySet(models.QuerySet):
  def is_public(self):
    return self.filter(public=True)
  
  def search(self, query, user=None):
    lookup = Q(title__icontains=query) | Q(content__icontains=query)
    qs = self.is_public().filter(lookup)
    if user is not None:
      qs2 = self.filter(user=user).filter(lookup) #user records that are not public
      qs = (qs | qs2).distinct()
    return qs

class ProductManager(models.Manager):
  def get_queryset(self, *args, **kwargs):
    return ProductQuerySet(self.model, using=self._db)
   
  def search(self, query, user=None):
    return self.get_queryset().search(query, user=user)

class Product(models.Model):

  user = models.ForeignKey(User, default=1, null=True, 
                           on_delete=models.SET_NULL)
  title = models.CharField(max_length=250)
  content = models.TextField(null=True, blank=True)
  price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)
  public = models.BooleanField(default=True)

  objects = ProductManager()

  @property
  def body(self):
    return self.content
  
  @property
  def path(self):
    return f"/products/{self.pk}"
  
  def get_absolute_url(self):
        return reverse("product-detail", kwargs={"pk": self.pk})
  
  @property
  def endpoint(self):
    return self.get_absolute_url()
    

  def is_public(self):
    return self.public
  
  def get_tags_list(self):
    return [random.choice(TAGS_MODEL_VALUES)]
  
  @property
  def sale_price(self):
    return "%.2f" %(float(self.price) * 0.8)
  
  def __str__(self):
    return self.title