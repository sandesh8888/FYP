from django.conf.urls import url
from productmanagement import views
from django.urls import path, include

app_name='productmanagement'
urlpatterns = [
    path('products/', views.display_products, name="index"),
    path('products/create/',views.create, name='create'),
    path('products/delete/<int:id>/',views.delete, name='delete'),
    path('detail/<str:pk>/', views.product_detail, name="detail"),
]

