from django.conf.urls import url
from dealers import views
from django.urls import path, include

app_name = 'dealers'
urlpatterns = [
    path('dealer/', views.display_dealers, name="index"),
    path('dealer/create/',views.create, name='create'),
    path('dealer/delete/<int:id>/',views.delete, name='delete'),  
]
