from django.conf.urls import url
from CustomerManagement import views
from django.urls import path, include


app_name = 'customermanagement'
urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"), 
    path('customer/', views.display_customers, name="index"),
    path('customer/create/',views.create, name='create'),
    path('customer/delete/<int:id>/',views.delete, name='delete'),    
    
      
]