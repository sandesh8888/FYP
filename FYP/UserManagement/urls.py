from django.conf.urls import url
from django.urls import path,include
from UserManagement import views


app_name = 'usermanagement'
urlpatterns = [
    path('login/',views.user_login, name='user_login'),
    path('logout/',views.user_logout,name='user_logout'), 
    path('', views.display_home, name='home_page' ),  
]
