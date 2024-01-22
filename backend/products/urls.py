from django.urls import path
from . import views


urlpatterns =[
  path('', views.product_list_create_view, name="product-list"),
  path('<int:pk>/update/', views.product_update_view, name="product-edit"),
  path('<int:pk>/delete/', views.product_delete_view, name="product-create"),
  path('<int:pk>/', views.product_detail_view, name="product-detail"),
  # path('', views.product_alt_view), # using function based view
  # path('<int:pk>/', views.product_alt_view)  # using function based view
]
