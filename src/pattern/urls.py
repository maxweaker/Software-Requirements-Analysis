from django.urls import path
from . import views


urlpatterns = [
    path('UserInfo', views.userinfor, name='UserInfo'),
]