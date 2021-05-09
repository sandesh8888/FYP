from django.conf.urls import url
from productmanagement import views
from django.urls import path, include

app_name='productmanagement'
urlpatterns = [
    path('products/', views.display_products, name="index"),
    path('products/create/',views.create, name='create'),
    path('products/delete/<int:id>/',views.delete, name='delete'),
    path('detail/<str:pk>/', views.product_detail, name="detail"),
    path('transactions/',views.transactions, name='transactions'),
    path('sellform/<str:pk>/', views.product_sell, name="sellform"),
    path('sell/<str:id>/', views.product_sell_to_customer, name="sellproduct"),
    path('receiptform/',views.receipt_form, name="receipt_form"),
    path('updateTransaction/<str:id>/',views.update_transaction, name="update_transaction"),
    path('update/<str:id>/', views.update, name="update"),
    path('updateCustomer/<str:id>', views.update_customer, name="update_customer"),
    path('updateCustomerTransaction/<str:id>/',views.update_customer_transaction, name="update_customer_transaction"),
]

