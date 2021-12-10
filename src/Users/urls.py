from django.urls import path
from .views import *

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('chartLine', lineChart, name='chartLine'),
    path('chartPie', pieChart, name='chartPie'),
    path('UserInfo', userinfor, name='UserInfo'),
    path('emailcheck', authen_email.as_view(), name='checkemail'),
    path('test', mecTest, name='test'),

]
